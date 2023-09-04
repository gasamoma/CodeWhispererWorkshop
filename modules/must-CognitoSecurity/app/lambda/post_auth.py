# a basic lambda handler for Amazon cognito post authorization
import json
import boto3
import uuid

def lambda_handler(event, context):
    # create a UUID 8 digit string
    uuid = str(uuid4())[:8]
    # load the dynamodb table name from os
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # write the UUID to the table
    table.put_item(
        Item={
            'uuid': uuid
            })
    # add the uuid to the response 
    event['uuid'] = uuid
    return event
                            