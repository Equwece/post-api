from .es_requests import *

def init_db():
    '''Convert posts.csv to json file,
    import json file to Elasticsearch index'''
    create_index()
    csv_to_json();
    with open(JSON_PATH, 'r') as f:
        json_file = json.load(f)
        import_json_to_index(json_file)

if __name__ == '__main__':
    init_db()
