from flask import Flask, request
from flask_restful import Resource, Api
from .es_requests import *
from .init_db import *
from datetime import datetime
from flasgger import Swagger

template = {
  "swagger": "2.0",
  "info": {
    "title": "Post API",
    "description": "Post API for vacansy task",
    "version": "0.0.1"
  },
  "host": "localhost",
  "basePath": "/",
  "schemes": [
    "http",
    "https"
  ],
}

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template=template)

@app.before_first_request
def init_db_if_necessary():
    '''Init json db and import data to 
    Elasticsearch, if index is not created'''
    if not is_index_created():
        init_db()

class PostList(Resource):
    def get(self):
        """
        Search posts by text query
        ---
        tags:
        - "post"
        parameters:
        - name: q
          in: query
          type: string
          description: Text query for search
        responses:
          200:
            description: Posts suitable for query
            schema:
              id: Post
              properties:
                id:
                  type: string
                  description: UUID of post
                text:
                  type: string
                  description: Post text
                created_date:
                  type: string
                  description: Post date
                rubrics:
                  type: string
                  description: Post rubrics
        """
        args = dict(request.args)
        q = None
        if 'q' in args:
            q = args['q']
        r = search_index(q) 
        es_posts = r.json()['hits']['hits'][:20]
        db_posts = []
        for es_post in es_posts:
            post = get_entry(es_post['_id']) 
            db_posts.append(post)
        db_posts.sort(key=lambda elem: elem['created_date'], reverse=True)
        return db_posts

class PostDetail(Resource):
    def get(self, post_id):
        """
        Get Post by id
        ---
        tags:
        - "post"
        responses:
          200:
            description: Post
            schema:
              id: Post
        """
        post = get_entry(post_id)
        if post:
            return post
        else:
            return '', 404

    def delete(self, post_id):
        """
        Delete post by id
        ---
        tags:
        - "post"
        responses:
          204:
            description: Post was deleted
          404:
            description: Post not found

        """
        delete_doc(post_id)
        status = delete_entry(post_id)
        if status:
            return '', 204
        return '', 404

api.add_resource(PostList, '/search')
api.add_resource(PostDetail, '/post/<string:post_id>')

if __name__ == '__main__':
    app.run(debug=True)
