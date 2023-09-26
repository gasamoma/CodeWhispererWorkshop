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

    # send an image to Amazon Recokgnition for face detection
    if security.POST_AUTH:
        # download image from s3
        s3 = boto3.client('s3')
        # get the bucket name from the BUCKET env var
        bucket = environ.get('BUCKET')
        # get the key
        key = event['body']['key']
        # get object from s3 to variable
        image = s3.get_object(Bucket=bucket, Key=key)
        # create a rekognition client
        rekognition = boto3.client('rekognition')
        # detect faces in the image
        response = rekognition.detect_faces(Image={'Bytes': image}, Attributes=['ALL'])
        # get the confidence
        confidence = response['FaceDetails'][0]['Confidence']
        # check if the confidence is high enough
        if confidence > min_confidence and response['FaceDetails'][0]['MouthOpen']['Value']:
            # return the default lambda response with cors
            response = {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                'body': json.dumps({'Hello':"from lambda"})
                }
        else:
            # return the default lambda response with cors
            response = {
                "statusCode": 401,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                'body': json.dumps({'Hello':"from lambda"})
                }
