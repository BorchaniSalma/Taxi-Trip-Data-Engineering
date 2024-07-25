# Apache Beam Pipeline for NYC Taxi Data

## Prerequisites
- Docker installed on your machine.

## Instructions to Run the Pipeline
1. **Build the Docker image:**
   ```sh
   docker-compose -f docker/docker-compose.yml build
   ```

2. **Run the Docker containers:**
   ```sh
   docker-compose -f docker/docker-compose.yml up
   ```



## Apache Beam Transformations
The pipeline performs the following transformations on the dataset:

- Filters out trips where the trip distance is less than 0.1 miles.
- Calculates the total fare amount for each trip (sum of fare amount and tip amount).
- Groups the data by pickup location and calculates the average total fare amount.
- Groups the data by dropoff location and calculates the average trip distance.


The transformed data will be saved to an Elasticsearch index named `nyc_taxi_trip`.
