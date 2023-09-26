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
bucket = environ.get('BUCKET')

# a lambda handler for the api gateway post
def handler(event, context):
    ## SECURITY CHECK
    print(security.POST_AUTH )
    security.POST_AUTH = security.check_auth(event)
    print(security.POST_AUTH )
    
    # detect faces function
    result = detect_mouth_open(bucket, event['key'])

    # return the default lambda response with cors
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
        'body': json.dumps({'is_valid':result})
        }

# create a function that detect faces from an image uploaded to an s3 bucket
#def detect_faces(bucket, key):
#    rekognition = boto3.client('rekognition')
#   response = rekognition.detect_faces(
#        Image={
#            'S3Object': {
#                'Bucket': bucket,
#                'Name': key,
#                }
#        }
 #   )

# create a function that detects the mouth open on an image uploaded to an s3 bucket
def detect_mouth_open(bucket, key):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
                }
                },
                Attributes=['ALL']
                )
    # print all attributes
    print(response)
    # return the mouth open value
    return response['FaceDetails'][0]['MouthOpen']['Value']
