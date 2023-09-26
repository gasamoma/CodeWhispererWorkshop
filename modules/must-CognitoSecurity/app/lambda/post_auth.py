# a basic lambda handler for Amazon cognito post authorization
import json
import boto3
import os
import time

# a function that ...
def handler(event, context):

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
        'body': json.dumps({'Hello':"from lambda"})
        }

#Create a function to recieve a post authorization event from cognito and store email user in dynamo db table with timestamp
def post_auth(event, context): 
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    table.put_item(Item={
        'user-email': event['request']['userAttributes']['email'],
        'date': str(time.time())
    })
    return event   