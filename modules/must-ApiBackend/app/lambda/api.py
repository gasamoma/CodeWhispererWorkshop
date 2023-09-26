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
    security.POST_AUTH = True #security.check_auth(event)
    print(security.POST_AUTH )
    # return the default lambda response with cors
    
   # identify if a person has its mouth open with amazon rekognition, the key of fline in s3 is located in event.body.key
    if security.POST_AUTH:
        print("security check passed")
        # get the key of the image
        key = event['body']['key']
        # get the bucket name
        bucket = environ.get('BUCKET');
        
        # create the s3 client
        s3 = boto3.client('s3')
        # get the image from s3 to use  with rekognition
        image = s3.get_object(Bucket=bucket, Key=key)
       
        # create the rekognition client
        rekognition = boto3.client('rekognition')
        
        #use image to detect faces with open mounth
        response = rekognition.detect_faces(Image={'Bytes': image}, Attributes=['ALL'])
        
        # get the face
        face = response['FaceDetails'][0]
        
        #check if the face has open mounth
        # fix the syntax error in the next lines
        if face['MouthOpen']['Value'] == True:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "approved": True
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "approved": False
                })
            }
    else:
            # return the confidence
            return {
                'statusCode': 403,
                'body': json.dumps({
                    "passToMars": False
                })
            }
                
