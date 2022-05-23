import csv 
import json 
import uuid

def csv_to_json(csv_path, json_path):
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

def delete_entry(entry_id, json_path):
    f = open('test.json', 'r')
    json_list = json.load(f)
    f.close()
    for obj in json_list:
        if obj['id'] == entry_id:
            del obj['id']
    with open('db.json', 'w') as f:
        json.dump(json_list, f)


if __name__ == '__main__':
    csv_path = 'posts.csv'
    json_path = 'db.json'
    csv_to_json(csv_path, json_path)
