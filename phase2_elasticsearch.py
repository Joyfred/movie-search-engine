from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search, Q
import json
import logging

# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# print(es)

movie_mapping = {
    "properties": {
        "id": {
            "type": "text"
        },
        "title": {
            "type": "text"
        },
        "description": {
            "type": "text"
        },
        "year": {
            "type": "text"
        },
        "rating": {
            "type": "text"
        },
        "director": {
            "type": "text"
        },
        "genre": {
            "type": "text"
        },
        "stars": {
            "type": "text"
        }
    }
}

with open("movies.json", "r") as data_file:
    movies = json.load(data_file)

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected to elasticsearch')
    else:
        print('Not connected')
    return _es

if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": movie_mapping
    }

    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def insert_data_by_bulk(es_object, index, data):
    processed_data = []
    for datum in data:
        processed_data.append({
            "_index": index,
            "_id": datum["id"],
            "_source": datum
        })
    try:
        res = helpers.bulk(es, processed_data)
        print(res)
    except Exception as ex:
        print("Error in inserting bulk data")
        print(str(ex))

def create_search_instance(elastic_object, index):
    return Search(using=elastic_object)

es = connect_elasticsearch()
# create_index(es, "movies")
# insert_data_by_bulk(es, "movies", movies)
s = create_search_instance(es, "movies")
q = Q("query_string", query="downey")
s = s.query(q)
response = s.execute()
results = [{"score": hit["_score"], "movie": hit["_source"]} for hit in response.to_dict()["hits"]["hits"]]
# print(response.to_dict())

# es.indices.put_mapping(index=["movies"], doc_type="movies", body=movie_mapping)
