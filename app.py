from flask import Flask, request
from flask_restful import Resource, Api
from es_requests import *

app = Flask(__name__)
api = Api(app)

class PostList(Resource):
    def get(self):
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
        return db_posts

class PostDetail(Resource):
    def get(self, post_id):
        post = get_entry(post_id)
        return post

    def delete(self, post_id):
        status = delete_entry(post_id)
        if status:
            delete_doc(post_id)
            return '', 204
        return '', 404

api.add_resource(PostList, '/')
api.add_resource(PostDetail, '/<string:post_id>')

if __name__ == '__main__':
    app.run(debug=True)
