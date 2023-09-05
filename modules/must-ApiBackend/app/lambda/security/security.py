import os
import boto3

#check if POST_AUTH is "1" or from the environ
if os.environ.get("POST_AUTH",None) == "1":
    POST_AUTH = True
    print("POST_AUTH is set to True")
else:
    POST_AUTH = False
    print("POST_AUTH is set to False")

def check_auth(event):
    print(event)
    if POST_AUTH:
        # get the POST_AUTHENTICATION_DYNAMO_TABLE_NAME
        table_name = os.environ.get("POST_AUTHENTICATION_DYNAMO_TABLE_NAME")
        # get the dynamo db client
        dynamodb = boto3.resource('dynamodb')
        # get the table
        table = dynamodb.Table(table_name)
        # get the user email from the cognito in the event
        user_email = event['requestContext']['authorizer']['claims']['email']
        # check if uuid exists on the table as id
        response = table.get_item(Key={'user-email': user_email})
        print(response)
        # if the response is empty
        if not response:
            return False
        # if the response is not empty
        else:
            return True
    else:
        return False