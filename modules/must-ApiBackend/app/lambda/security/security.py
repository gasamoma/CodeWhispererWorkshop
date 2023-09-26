import os
import boto3
import time
from boto3.dynamodb.conditions import Key
from datetime import date
#import timedelta
from datetime import timedelta


POST_AUTHENTICATION_DYNAMO_TABLE_NAME =  os.environ.get("POST_AUTHENTICATION_DYNAMO_TABLE_NAME",None)
                                                        
#check if POST_AUTH is “1" or from the environ
if os.environ.get("POST_AUTH",None) == "1":
    POST_AUTH = True
    print("POST_AUTH is set to True")
else:
    POST_AUTH = False
    print("POST_AUTH is set to False")
<<<<<<< Updated upstream

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
=======
# a function that ...
def check_auth(event):
    # ... checks if the request is authorized
    # ... returns True if authorized
    # ... returns False if not authorized
    # ... returns False if POST_AUTH is not set
# get user-email of api post event trigger the lambda function from apigateway cognito authentication
    user_email = event["requestContext"]["authorizer"]["claims"]["email"]
    #get item of dynamo db POST_AUTHENTICATION_DYNAMO_TABLE_NAME from user_email
    items = get_item_from_dynamo(user_email)
    #print(items)
#    #check if the date is within last hour
    if check_date(items["date"]):
        if POST_AUTH: # and signing dynamo db < 1hr
            return True
    return False
#get item of dynamo db POST_AUTHENTICATION_DYNAMO_TABLE_NAME from user_email
def get_item_from_dynamo(user_email):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(POST_AUTHENTICATION_DYNAMO_TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key("user-email").eq(user_email)
    )
    return response["Items"]

#function to valid if the date is within last hour
def check_date(date):
    #check if date is within last hour
    if date > date.today() - timedelta(hours=1):
        return True
    else:
        return False
    












>>>>>>> Stashed changes
