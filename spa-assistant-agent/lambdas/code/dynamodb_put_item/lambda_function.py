###############################################################
## This function is to populate a dynamoDB table with a CSV ###
###############################################################

import json
import csv
import boto3
import os
import time

BASE_PATH = '/tmp/'
CSV_SEPARATOR = ';'

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['TABLE_NAME'])
key = os.environ['ENV_KEY_NAME']

def save_item_ddb(table,item):
    response = table.put_item(Item=item)
    return response


def lambda_handler(event, contex):
    print(event)

    item = event['prompt']
    item_value = json.loads(item)
    item_value["phone_number"] = item_value["phone_number"].replace("+","")
    
    response = save_item_ddb(table,item_value)
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return "Done"
    else:
        return "error"
 

