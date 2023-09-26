# a basic lambda handler for Amazon cognito post authorization
import json
import boto3
import os
import time

# Create client for DynamoDB
dynamodb = boto3.resource('dynamodb')

# a function that ...
def handler(event, context):
    # Get email from Cognito Post Auth Event from parameter called 'event'
    email = event['request']['userAttributes']['email']
    # Get current timestamp
    timestamp = str(time.time())
    
    dynamodb_table = os.environ["DYNAMODB_TABLE"]
    
    # Reference dynamodb table using the 'dynamodb_table' variable 
    table = dynamodb.Table(dynamodb_table)
    
    # Insert record into 'table' with record user-email using 'email' as value and date using 'timestamp' as value
    response = table.put_item(
        Item={
            'user-email': email,
            'date': timestamp
        }
    )
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
        'body': json.dumps({'Hello':"from lambda"})
        }
                            
