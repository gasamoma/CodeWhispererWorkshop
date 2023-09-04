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

# Get the model ARN and confidence.
min_confidence = int(environ.get('CONFIDENCE', 70))

#function that gets an image from an s3 bucket and calls rekognition detect_faces api to get the face attributes
#returns the response
def detect_faces(bucket, key):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': key}}, Attributes=['ALL'])
    return response
    
#from response get EyesOpen, MouthOpen attributes and store them in variables
def get_eyes_mouth_open(response):
    eyes_open = response['FaceDetails'][0]['EyesOpen']
    mouth_open = response['FaceDetails'][0]['MouthOpen']
    return eyes_open, mouth_open

#from response get EyeDirection yaw attribute and store it in a variable
def get_eye_direction(response):
    eye_direction = response['FaceDetails'][0]['EyeDirection']['Yaw']
    return eye_direction
    
#sum confidence value from eyes_open and mouth_open attributes
def sum_confidence(eyes_open, mouth_open):
    confidence = eyes_open['Confidence'] + mouth_open['Confidence']
    return confidence
    
#if return confidence higher than 70, eye_direction higher than 150 and POST_AUTH variable exist print "you are invited to visit Mars"
#else print "you are not invited to visit Mars"
def check_if_authorized(confidence, eye_direction, POST_AUTH):
    if confidence > min_confidence and eye_direction > 150 and POST_AUTH:
        print("Congratulations! You are invited to visit Mars on the new GlueOrigin rocket!")
    else:
        print("you are not invited to visit Mars")

    


        
        
