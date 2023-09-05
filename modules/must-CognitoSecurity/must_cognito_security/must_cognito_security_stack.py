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
    aws_ssm as ssm,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct

class MustCognitoSecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # a dinamoDb table with ondemand capacity 
        dynamoDbTable = dynamodb.Table(self, "MustCognitoSecurityTable",
            partition_key=dynamodb.Attribute(
                name="user-email",
                type=dynamodb.AttributeType.STRING
                ),
                # add date as range key
                sort_key=dynamodb.Attribute(
                    name="date",
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
                "DYNAMODB_TABLE": dynamoDbTable.table_name,
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
        # add permisions to the post_autentication_lambda to put items in teh dyanmo table
        post_autentication_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem"],
                resources=[dynamoDbTable.table_arn]
                ))
        # an ssm parameter with the post_autentication_lambda arn
        ssm.StringParameter(self, "post_autentication_lambda_arn",
            parameter_name="CW-workshop-post-autentication-lambda",
            string_value=post_autentication_lambda.function_arn)
        # an ssm parameter for post_autentication_dynamo
        ssm.StringParameter(self, "post_autentication_dynamo_table_name",
            parameter_name="CW-workshop-post-autentication-dynamo",
            string_value=dynamoDbTable.table_name)
            
        
        
        