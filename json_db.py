import csv 
import json 
import uuid

JSON_PATH = 'db.json'

def csv_to_json(csv_path, json_path=JSON_PATH):
    csvfile = open(csv_path, 'r')
    jsonfile = open(json_path, 'w')
    reader = csv.DictReader(csvfile)
    reader = list(reader)
    length = len(reader)
    jsonfile.write('[')
    for i in range(len(reader)):
        post_id = str(uuid.uuid4())
        reader[i]['id'] = post_id
        json.dump(reader[i], jsonfile)
        if i != length - 1:
            jsonfile.write(',')
            jsonfile.write('\n')

    csvfile.close()
    jsonfile.write(']\n')
    jsonfile.close()

def delete_entry(entry_id, json_path=JSON_PATH):
    status = False
    f = open(json_path, 'r')
    json_list = json.load(f)
    f.close()
    for obj in json_list:
        if obj['id'] == entry_id:
            json_list.remove(obj)
            status = True
            break
    with open(json_path, 'w') as f:
        json.dump(json_list, f)
    return status

def get_entry(entry_id, json_path=JSON_PATH):
    f = open(json_path, 'r')
    json_list = json.load(f)
    f.close()
    for obj in json_list:
        # print(obj)
        if obj['id'] == entry_id:
            return obj
    return None


if __name__ == '__main__':
    csv_path = 'posts.csv'
    csv_to_json(csv_path, json_path=JSON_PATH)
