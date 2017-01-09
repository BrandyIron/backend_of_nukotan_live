# -*- coding: utf8 -*-
import json
import sys
from google.cloud import datastore
from prettyprint import pp

def load_json(fname):
    f = open(fname)
    
    return json.load(f)

def put_datastore(record):
    pp(record)
    datastore_client = datastore.Client()
    kind = 'NukotanLive'
    task_key = datastore_client.key(kind)
    task = datastore.Entity(key=task_key)

    task['tour'] = record['tour']
    task['place'] = record['place']
    task['date'] = record['date']
    task['song'] = record['song']
    # save into datastore
    datastore_client.put(task)

if __name__ == '__main__':
    argvs = sys.argv
    for record in load_json(argvs[1]):
        put_datastore(record)
    