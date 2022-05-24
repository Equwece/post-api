'''Working with Elasticsearch API using requests'''
from decouple import config
import requests
import uuid
from .json_db import *

ES_HOST = config('ES_HOST')
ES_PORT = int(config('ES_PORT'))
ES_ADDR = f'http://{ES_HOST}:{ES_PORT}/'

def create_index(index='posts'):
    return requests.put(ES_ADDR + index)

def is_index_created(index='posts'):
    return requests.get(ES_ADDR + index).status_code != 404

def post_doc(json_doc, doc_id='', index='posts'):
    return requests.post(ES_ADDR + index + '/_doc/' + doc_id, json=json_doc)

def get_doc(doc_id, index='posts'):
    return requests.get(ES_ADDR + index + '/_doc/' + str(doc_id))

def delete_doc(doc_id, index='posts'):
    return requests.delete(ES_ADDR + index + '/_doc/' + str(doc_id))

def search_index(query=None, index='posts'):
    params = {
        "size": 20,
    }
    if query:
        params['q'] = query
    return requests.get(ES_ADDR + index + '/_search', params=params)

def import_json_to_index(json_list, index='posts'):
    for obj in json_list:
        json_doc = {
            'text': obj['text'], 
        }
        post_doc(json_doc, obj['id'])
