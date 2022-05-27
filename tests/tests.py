import pytest
from app.app import *
from pathlib import Path
import asyncio

test_folder = Path(__file__)

def test_search_all():
    with app.test_client() as test_client:
        response = test_client.get('/search')
        assert response.status_code == 200
        assert b'"id":' in response.data
        assert b'"rubrics":' in response.data
        assert b'"created_date":' in response.data
        assert b'"text":' in response.data
        json_list = json.loads(response.data)
        assert len(json_list) == 20

def test_search_query():
    with app.test_client() as test_client:
        q = 'погода'
        response = test_client.get(f'/search?q={q}')
        assert response.status_code == 200
        json_list = json.loads(response.data)
        for obj in json_list:
            assert q.lower() in obj['text'].lower()

def test_delete_entry():
    with app.test_client() as test_client:
        q = 'снег'
        response = test_client.get(f'/search?q={q}')
        assert response.status_code == 200
        random_post = json.loads(response.data)[0]
        delete_response = test_client.delete(f'/post/{random_post["id"]}')
        assert delete_response.status_code == 204
        assert test_client.get(f'/post/{random_post["id"]}').status_code == 404
