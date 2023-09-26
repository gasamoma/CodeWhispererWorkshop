import os
import boto3
import time
from boto3.dynamodb.conditions import Key

#check if POST_AUTH is "1" or from the environ
if os.environ.get("POST_AUTH",None) == "1":
    POST_AUTH = True
    print("POST_AUTH is set to True")
else:
    POST_AUTH = False
    print("POST_AUTH is set to False")

# a function that get from the event the user email and scan a table in dynamodb using that email as partition key
def check_auth(event):
    # get the user email from the event which is an post authorization cognito event
    user_email = event['requestContext']['authorizer']['claims']['email']
    # scan the table using that email as partition key
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['POST_AUTHENTICATION_DYNAMO_TABLE_NAME']
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=Key('user-email').eq(user_email))
    # compare the timestamp from the response date field with the current time and evaluate if is less than 60 minutes
    return response['Items'][0]['date'] > (time.time() - 60*60)
