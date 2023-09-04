from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda as _lambda,
    Duration,
    aws_cognito as _cognito,
    Fn,
    CfnOutput,
    aws_dynamodb as dynamodb,
    # aws_sqs as sqs,
)
from constructs import Construct

class MustCognitoSecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # a dinamoDb table with ondemand capacity 
        dynamoDbTable = dynamodb.Table(self, "MustCognitoSecurityTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
                ),
                # billing type ondemand
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)
        post_autentication_lambda = python.PythonFunction(self, "CognitoPostAuthTrigger",
            entry="app/lambda",
            index="post_auth.py",  
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                #"BUCKET_NAME": s3_bucket.bucket_name,
                "TABLE_NAME": dynamoDbTable.table_name,
                "PREFIX": "output/",
                },
            timeout=Duration.seconds(120),
            layers=[
                python.PythonLayerVersion(self, "cognito_layer",
                    entry="lib/python",
                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
                )
            ]
        )
        # CfnOutput the post_autentication_lambda arn
        CfnOutput(self, "post_autentication_lambda", value=post_autentication_lambda.function_arn, export_name="CW-workshop-post-autentication-lambda")
        
        