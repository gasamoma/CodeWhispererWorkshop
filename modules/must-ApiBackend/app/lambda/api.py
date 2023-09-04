# a basic lambda handler dor api gateway proxy
import json
import boto3
# run the security/security.py file
from security import security


def lambda_handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }