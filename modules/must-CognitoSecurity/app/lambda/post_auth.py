# a basic lambda handler dor api gateway proxy
import json
import boto3
from security import *


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