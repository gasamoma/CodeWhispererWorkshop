import os
import boto3
import time
from boto3.dynamodb.conditions import Key

# Create client from DynamoDB
dynamodb = boto3.resource('dynamodb')

#check if POST_AUTH is "1" or from the environ
if os.environ.get("POST_AUTH",None) == "1":
    POST_AUTH = True
    print("POST_AUTH is set to True")
else:
    POST_AUTH = False
    print("POST_AUTH is set to False")

# a function that ...
def check_auth(event):
    # Get user from Cognito Post Auth Event using API Gateway Proxy as entry
    user = event['requestContext']['authorizer']['claims']['email']
    
    # Get POST_AUTHENTICATION_DYNAMO_TABLE_NAME environment variable
    table_name = os.environ['POST_AUTHENTICATION_DYNAMO_TABLE_NAME']
    
    # Initiate dynamodb table using table_name variable
    table = dynamodb.Table(table_name)
    
    # Query dynamodb table using 'user-email' as column and 'user' variable as value
    records = table.query(KeyConditionExpression=Key('user-email').eq(user))
    
    # Validate if records variable has values
    if records['Items']:
        # Get 'date' from records variable and convert into epoch timestamp
        date = int(records['Items'][0]['date'])
        
        # Get current timestamp
        current_time = time.time()
        
        # Get difference between current_time variable and date
        difference = current_time - date
        
        # Validate if difference is less than 1 hour in epoch format then return true
        if difference < 3600:
            return True
    return False
