import time
from elasticsearch import Elasticsearch

# Create an Elasticsearch client
es = Elasticsearch(['http://localhost:9200'])

# Retry connection to Elasticsearch
for _ in range(30):  # Retry for 30 times
    if es.ping():
        break
    print("Elasticsearch not available yet, retrying in 5 seconds...")
    time.sleep(5)
else:
    raise ValueError("Connection failed")

# Define the index settings and mappings
index_name = 'nyc_taxi_trip_data'
index_settings = {
    "settings": {
        "number_of_shards": 1,  # Number of primary shards
        "number_of_replicas": 0  # Number of replica shards
    },
    "mappings": {
        "properties": {
            "pickup_location_id": {"type": "integer"},
            "dropoff_location_id": {"type": "integer"},
            "trip_distance": {"type": "float"},
            "total_fare_amount": {"type": "float"},
            "average_total_fare": {"type": "float"},
            "average_trip_distance": {"type": "float"}
        }
    }
}

# Create the index if it does not exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_settings)
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")
