# a basic lambda handler dor api gateway proxy
import json
import boto3
# run the security/security.py file
from security import security
import base64
import logging
from os import environ


# Set up logging.
logger = logging.getLogger(__name__)

# Get the confidence.
min_confidence = int(environ.get('CONFIDENCE', 70))
# a lambda handler for the api gateway post
def handler(event, context):
    ## SECURITY CHECK
    print(security.POST_AUTH )
    security.POST_AUTH = security.check_auth(event)
    print(security.POST_AUTH )
    # return the default lambda response with cors
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
        'body': json.dumps({'Hello':"from lambda"})
        }
