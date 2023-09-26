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
                            