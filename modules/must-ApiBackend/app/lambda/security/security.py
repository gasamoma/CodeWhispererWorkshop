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

# a function that ...
def check_auth(event):
    return False