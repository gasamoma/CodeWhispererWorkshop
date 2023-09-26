# a basic lambda handler for Amazon cognito post authorization
import json
import boto3
import os
import time

# a function that ...
def handler(event, context):

    resource_db = boto3.resource('dynamodb')
    table = resource_db.Table(os.environ['DYNAMODB_TABLE'])

    key = {}
    key['user-email'] = event['request']['userAttributes']['email']
    key['date'] = str(int(time.time()))

    table.put_item(Item=key)

   return 1



