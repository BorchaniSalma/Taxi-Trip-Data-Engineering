import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from elasticsearch import Elasticsearch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the headers for the CSV file
headers = [
    "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count",
    "trip_distance", "rate_code", "store_and_fwd_flag", "pu_location_id",
    "do_location_id", "payment_type", "fare_amount", "extra", "mta_tax",
    "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount",
    "congestion_surcharge", "airport_fee"
]


class ParseCSV(beam.DoFn):
    """
    A DoFn to parse each line of CSV into a dictionary.
    """

    def process(self, element):
        import csv
        from io import StringIO

        reader = csv.DictReader(StringIO(element), fieldnames=headers)

        for row in reader:
            if row:
                yield row
            else:
                logger.error(f"Failed to parse row: {element}")


class FilterShortTrips(beam.DoFn):
    """
    A DoFn to filter out trips with a distance less than 0.1 miles.
    """

    def process(self, element):
        if element:
            try:
                trip_distance = float(element.get('trip_distance', 0))
                if trip_distance >= 0.1:
                    yield element
            except Exception as e:
                logger.error(f"Error processing row: {element}, Error: {e}")
        else:
            logger.error(f"Received None element: {element}")


class CalculateTotalFare(beam.DoFn):
    """
    A DoFn to calculate the total fare amount by adding fare_amount and tip_amount.
    """

    def process(self, element):
        if element:
            try:
                fare_amount = float(element.get('fare_amount', 0))
                tip_amount = float(element.get('tip_amount', 0))
                element['total_fare_amount'] = fare_amount + tip_amount
                yield element
            except Exception as e:
                logger.error(f"Error calculating fare: {element}, Error: {e}")
        else:
            logger.error(f"Received None element: {element}")


class WriteToElasticsearch(beam.DoFn):
    """
    A DoFn to write processed data to Elasticsearch.
    """

    def __init__(self, es_index):
        self.es_index = es_index
        self.es = None

    def start_bundle(self):
        self.es = Elasticsearch(['http://elasticsearch:9200'])

    def process(self, element):
        if element:
            try:
                self.es.index(index=self.es_index, body=element)
            except Exception as e:
                logger.error(f"Error indexing document: {element}, Error: {e}")
        else:
            logger.error(f"Received None element: {element}")


def run_pipeline(input_file, es_index):
    """
    Run the Apache Beam pipeline to process NYC taxi trip data and write results to Elasticsearch.

    Args:
        input_file (str): Path to the input CSV file.
        es_index (str): Name of the Elasticsearch index to write data to.
    """
    options = PipelineOptions()
    with beam.Pipeline(options=options) as p:
        # Read lines from the CSV
        lines = (
            p
            | 'Read CSV' >> beam.io.ReadFromText(input_file, skip_header_lines=1)
        )

        # Parse CSV and log rows
        rows = (
            lines
            | 'Parse CSV' >> beam.ParDo(ParseCSV())
        )

        # Filter out any None elements
        valid_rows = (
            rows
            | 'Filter None Rows' >> beam.Filter(lambda x: x is not None)
        )

        # Filter short trips
        filtered_trips = (
            valid_rows
            | 'Filter Short Trips' >> beam.ParDo(FilterShortTrips())
        )

        # Calculate total fare amount
        calculated_fare = (
            filtered_trips
            | 'Calculate Total Fare' >> beam.ParDo(CalculateTotalFare())
        )

        # Group by pickup location and calculate average total fare amount
        pickup_location_fare = (
            calculated_fare
            | 'Map to Pickup Location' >> beam.Map(lambda x: (x['pu_location_id'], x))
            | 'Group by Pickup Location' >> beam.GroupByKey()
            | 'Calculate Average Fare' >> beam.Map(lambda x: {
                'pickup_location_id': x[0],
                'average_total_fare': sum([trip['total_fare_amount'] for trip in x[1]]) / len(x[1])
            })
        )

        # Group by dropoff location and calculate average trip distance
        dropoff_location_distance = (
            calculated_fare
            | 'Map to Dropoff Location' >> beam.Map(lambda x: (x['do_location_id'], x))
            | 'Group by Dropoff Location' >> beam.GroupByKey()
            | 'Calculate Average Distance' >> beam.Map(lambda x: {
                'dropoff_location_id': x[0],
                'average_trip_distance': sum([float(trip['trip_distance']) for trip in x[1]]) / len(x[1])
            })
        )

        # Write results to Elasticsearch
        (
            pickup_location_fare
            | 'Write Pickup Fare to Elasticsearch' >> beam.ParDo(WriteToElasticsearch(es_index))
        )

        (
            dropoff_location_distance
            | 'Write Dropoff Distance to Elasticsearch' >> beam.ParDo(WriteToElasticsearch(es_index))
        )


if __name__ == "__main__":
    input_file = '/home/salma/Desktop/Taxi-Trip-Data-Engineering/data/yellow_tripdata_2022-01.csv'
    es_index = 'nyc_taxi_trip_data'  # Elasticsearch index name
    logger.info("Starting pipeline")
    run_pipeline(input_file, es_index)
    logger.info("Pipeline finished")
