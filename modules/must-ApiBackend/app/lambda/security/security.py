import os
import boto3
#check if POST_AUTH is "1" or from the environ
if os.environ.get("POST_AUTH") == "1":
    POST_AUTH = True
    print("POST_AUTH is set to True")
else:
    POST_AUTH = False
    print("POST_AUTH is set to False")
