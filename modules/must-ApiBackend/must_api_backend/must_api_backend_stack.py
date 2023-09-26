from aws_cdk import (
    # Duration,
    Stack,
    Token,
    aws_lambda_python_alpha as python,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_cognito as _cognito,
    Duration,
    RemovalPolicy,
    CfnOutput,
    Fn,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_s3 as s3,
    # aws_sqs as sqs,
)
from constructs import Construct

class MustApiBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        post_auth_exists = "0"
        # get the CW-workshop-post-autentication-dynamo ssm parameter
        try:
            post_autentication_dynamo_table_name = ssm.StringParameter.value_for_string_parameter(self, "CW-workshop-post-autentication-dynamo"+construct_id.replace("MustApiBackendStack","MustCognitoSecurityStack"))
        except:
            post_autentication_dynamo_table_name = "CW-workshop-post-autentication-dynamo"
            pass;
        
        try:
            test_post_autentication_lambda_arn = Fn.import_value("CW-test-workshop-post-autentication-lambda")
            post_auth_exists =  "1"
        # if import_value does not work continue
        except:
            pass
        # a cognito user pool that uses cognito managed login sign up and password recovery
        user_pool = _cognito.UserPool(
            self, "CW-UserPool",
            self_sign_up_enabled=True,
            # removal policy destroy
            removal_policy=RemovalPolicy.DESTROY,
            # add email as a standard attribute
            standard_attributes=_cognito.StandardAttributes(
                email=_cognito.StandardAttribute(
                    required=True,
                    mutable=False)),
            user_verification=_cognito.UserVerificationConfig(
                email_subject="Verify your email for our awesome app!",
                email_body="Thanks for signing up to our awesome app! Your verification code is {####}",
                email_style=_cognito.VerificationEmailStyle.CODE,
                sms_message="Thanks for signing up to our awesome app! Your verification code is {####}"
            ),
            sign_in_aliases=_cognito.SignInAliases(
                email=True,
                phone=False,
                username=False))
        # create the bucket
        s3_file_bucket = s3.Bucket(
            self, "cw-workshop-image-store",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.KMS_MANAGED
            )
        # add cors to the put method from everywhere
        s3_file_bucket.add_cors_rule(allowed_origins=['*'],
            allowed_methods=[s3.HttpMethods.PUT],
            allowed_headers=['*'])
        
        # a lambda function called api_backend
        api_backend = python.PythonFunction(self, "ApiBackend",
            entry="app/lambda",
            index="api.py",  
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                #"BUCKET_NAME": s3_bucket.bucket_name,
                # post_autentication_dynamo_table_name
                "POST_AUTHENTICATION_DYNAMO_TABLE_NAME": post_autentication_dynamo_table_name,
                "POST_AUTH": post_auth_exists,
                "BUCKET": s3_file_bucket.bucket_name,
                },
            timeout=Duration.seconds(120),
            layers=[
                python.PythonLayerVersion(self, "api_layer",
                    entry="lib/python",
                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
                )
            ]
        )
        # add permisions to api_backend AmazonS3ReadOnlyAccess
        s3_file_bucket.grant_read(api_backend)
        # add alpermisions to api_backend to lsi s3_file_bucket
        api_backend.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:ListBucket"],
            resources=[s3_file_bucket.bucket_arn]
            ))
        # create dynamo db arn
        post_autentication_dynamo_table_arn = "arn:aws:dynamodb:" + self.region + ":" + self.account + ":table/" + post_autentication_dynamo_table_name
        # add permisions to access the dynamo db table
        api_backend.add_to_role_policy(iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Scan", "dynamodb:Query", "dynamodb:UpdateItem", "dynamodb:DeleteItem"],
            resources=[ post_autentication_dynamo_table_arn ]
            ))
        # add permisions to api_backend to rekognition full access
        api_backend.add_to_role_policy(iam.PolicyStatement(
            actions=["rekognition:*"],
            resources=["*"]
            ))
        # a lambda function called api_backend
        api_back_get = python.PythonFunction(self, "ApiBackendGet",
            entry="app/lambda",
            index="api_get.py",
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                    "BUCKET": s3_file_bucket.bucket_name,
                },
            timeout=Duration.seconds(120),
            layers=[
                python.PythonLayerVersion(self, "api_layer_get",
                    entry="lib/python",
                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
                )
            ]
        )
        # add permisions to api_back_get to presing urls from s3 to put
        s3_file_bucket.grant_put(api_back_get)
        # add permisions to api_back_get to presing urls from s3 to write
        s3_file_bucket.grant_write(api_back_get)
        s3_file_bucket.grant_read(api_back_get)
        # add permisions to rekognition service to read from s3_file_bucket

        
        # an API gateway that with cors for the cloudfront
        api_gateway = apigateway.RestApi(
            self, "ApiGWBackend",
            rest_api_name="CWApiGateway",
            description="This is the CodeWhisperer API Gateway",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=["*"],
                # TODO allow the cloufront distribution
                allow_origins=["*"],
                allow_headers=["*"])
                )
        
        domain = user_pool.add_domain("CognitoDomain",
            cognito_domain=_cognito.CognitoDomainOptions(
                domain_prefix="cw-ws-78e52dcb-30dd-447f-bcc3-da13985e7c24"
            )
        )
        
        
        try:
            redirect_uri = ssm.StringParameter.value_for_string_parameter(self, "CW-workshop-redirect_uri"+construct_id.replace("MustApiBackendStack","MustFrontEndJsStack"))
        except:
            redirect_uri = "https://www.amazon.com/"
            pass;
        # a cognito client with callback to the cloudfront_website
        client = user_pool.add_client("app-client",
            o_auth=_cognito.OAuthSettings(
                flows=_cognito.OAuthFlows(
                    implicit_code_grant=True
                ),
                # the cloudfront distribution root url
                callback_urls=[redirect_uri]
            ),
            auth_flows=_cognito.AuthFlow(
                user_password=True,
                user_srp=True
            )
        )
        sign_in_url = domain.sign_in_url(client,
            redirect_uri=redirect_uri
        )
        
        # a method for the api that calls the bedrock lambda function
        api_backend_integration = apigateway.LambdaIntegration(api_backend,
                request_templates={"application/json": '{ "statusCode": "200" }'})
        api_backend_get_integration = apigateway.LambdaIntegration( api_back_get,
                request_templates={"application/json": '{ "statusCode": "200" }'})
        
        # add the  LambdaIntegration to the api gateway using user_pool as the authorization
        api_backend_resource = api_gateway.root.add_resource("api_backend")
        autorizer=apigateway.CognitoUserPoolsAuthorizer(
                self, "IdpAuthorizer",
                cognito_user_pools=[user_pool])
        method_api_backend = api_backend_resource.add_method(
            "POST", api_backend_integration,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=autorizer)
        method_api_backend_get = api_backend_resource.add_method(
            "GET", api_backend_get_integration,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=autorizer)
        deployment = apigateway.Deployment(self, "Deployment",
            api=api_gateway,
            description="This is the CodeWhisperer API Gateway Deployment")
            
        # create an apigateway stage deployment called prod
        # api_backend_stage = api_gateway.Stage(
        #     "prod",
        #     stage_name="prod")
        
        # get the ssm parameter for CW-workshop-post-autentication-lambda
        try:
            post_autentication_lambda_arn = ssm.StringParameter.value_for_string_parameter(self, "CW-workshop-post-autentication-lambda"+construct_id.replace("MustApiBackendStack","MustCognitoSecurityStack"))
        except:
            # a "arn:" and have at least 6 components
            post_autentication_lambda_arn = "arn:aws:lambda:us-east-1:776590830345:function:MustCognitoSecurityStack-CognitoPostAuthTrigger501-C26V35ZeD2tq"
            pass;
        # reference the post_autentication_lambda from_function_attributes
        post_autentication_lambda = _lambda.Function.from_function_attributes(self, "post_autentication_lambda_ref", 
            function_arn=post_autentication_lambda_arn,
            same_environment=True,
        )
        user_pool.add_trigger(_cognito.UserPoolOperation.POST_AUTHENTICATION, post_autentication_lambda)
            
        ssm.StringParameter(self, "user_pool_login_url",
            parameter_name="user_pool_login_url"+construct_id,
            string_value=sign_in_url)
        # CfnOutput the user_pool login url
        CfnOutput(self, "UserPoolLoginUrl", value=sign_in_url)