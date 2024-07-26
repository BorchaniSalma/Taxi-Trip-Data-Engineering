import warnings
from elasticsearch import Elasticsearch

# Suppress specific warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning,
                        message='Elasticsearch built-in security features are not enabled.')


def read_from_index(es_index):
    es = Elasticsearch(['http://localhost:9200'])

    # Query to match all documents with size parameter included in the body
    query = {
        "size": 1000,
        "query": {
            "match_all": {}
        }
    }

    # Search the index
    response = es.search(index=es_index, body=query)

    # Print the results
    if 'hits' in response and 'hits' in response['hits']:
        for hit in response['hits']['hits']:
            print(hit['_source'])
    else:
        print("No documents found in the index.")


if __name__ == "__main__":
    es_index = 'nyc_taxi_trip_data'
    read_from_index(es_index)
