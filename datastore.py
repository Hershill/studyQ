from google.cloud import datastore
import json
datastore_client = datastore.Client()


def store_json(data, key):
    entity = datastore.Entity(key=datastore_client.key(key))
    # with open("sampleData.json", 'r') as f:
    #     sample_data = json.load(f)
    
    # with open("user2.json", 'r') as f:
    #     data = json.load(f)

    entity.update(data)    
    datastore_client.put(entity)


def fetch_json(key, filter=None):
    query = datastore_client.query(kind=key)
    if filter:
        query.add_filter(filter['type'], "=", filter['key'])
    # query.order = ['-timestamp']
    sample = list(query.fetch())
    if sample:
        return sample[0]
    return sample


def delete(key, filter):
    query = datastore_client.query(kind=key)
    if filter:
        query.add_filter(filter['type'], "=", filter['key'])
    entity = query.fetch()
    datastore_client.delete(entity)
