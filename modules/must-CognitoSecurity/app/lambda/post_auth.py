# a basic lambda handler for Amazon cognito post authorization
import json
import boto3
import os
import time


def handler(event, context):
    # load the dynamodb table name from os
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    #get the user-email fron the cognito event
    user_email = event['request']['userAttributes']['email']
    
    # write the user-email to the table with the range key of the current timestamp
    table.put_item(
        Item={
            'user-email': user_email,
            'date': str(int(time.time()))
        })
    # add the uuid to the response 
    #event['uuid'] = uuid
    return event
                            