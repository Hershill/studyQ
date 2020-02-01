from google.cloud import datastore
import json
from service import *
datastore_client = datastore.Client()


def store_json(key):
    entity = datastore.Entity(key=datastore_client.key(key))
    # with open("sampleData.json", 'r') as f:
    #     sample_data = json.load(f)
    
    # with open("userData.json", 'r') as f:
    #     user_data = json.load(f)

    entity.update(data)    
    datastore_client.put(entity)


def fetch_json(key, id=None):
    query = datastore_client.query(kind=key)
    query.add_filter("id", "=", id)
    # query.order = ['-timestamp']
    sample = query.fetch()

    return sample
