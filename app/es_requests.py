'''Working with Elasticsearch API using requests'''
from decouple import config
import requests
import uuid
from .json_db import *
import aiohttp
import asyncio

ES_HOST = config('ES_HOST')
ES_PORT = int(config('ES_PORT'))
ES_ADDR = f'http://{ES_HOST}:{ES_PORT}/'

async def create_index(index='posts'):
    return requests.put(ES_ADDR + index)
    async with aiohttp.ClientSession() as session:
        async with session.put(ES_ADDR + index) as resp:
            status_code = resp.status
            return status_code

async def delete_index(index='posts'):
    async with aiohttp.ClientSession() as session:
        async with session.delete(ES_ADDR + index) as resp:
            status_code = resp.status
            return status_code

async def is_index_created(index='posts'):
    async with aiohttp.ClientSession() as session:
        async with session.get(ES_ADDR + index) as resp:
            status_code = resp.status
            return status_code == 200

async def post_doc(json_doc, doc_id='', index='posts'):
    async with aiohttp.ClientSession() as session:
        async with session.post(ES_ADDR + index + '/_doc/' + str(doc_id), json=json_doc) as resp:
            json_data = await resp.json()
            return json_data

async def get_doc(doc_id, index='posts'):
    async with aiohttp.ClientSession() as session:
        async with session.get(ES_ADDR + index + '/_doc/' + str(doc_id)) as resp:
            json_data = await resp.json()
            return json_data

async def delete_doc(doc_id, index='posts'):
    async with aiohttp.ClientSession() as session:
        async with session.delete(ES_ADDR + index + '/_doc/' + str(doc_id)) as resp:
            json_data = await resp.json()
            return json_data

async def search_index(query=None, index='posts'):
    async with aiohttp.ClientSession() as session:
        params = {
            "size": 20,
        }
        if query:
            params['q'] = query
        async with session.get(ES_ADDR + index + '/_search/', params=params) as resp:
            json_data = await resp.json()
            return json_data
            

def import_json_to_index(json_list, index='posts'):
    for obj in json_list:
        json_doc = {
            'text': obj['text'], 
        }
        asyncio.run(post_doc(json_doc, obj['id']))
