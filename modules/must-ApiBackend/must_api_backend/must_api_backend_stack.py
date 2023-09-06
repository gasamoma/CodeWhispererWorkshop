from aws_cdk import (
    # Duration,
    Stack,
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
        post_autentication_dynamo_table_name = ssm.StringParameter.value_for_string_parameter(self, "CW-workshop-post-autentication-dynamo")
        
        try:
            test_post_autentication_lambda_arn = Fn.import_value("CW-test-workshop-post-autentication-lambda")
            post_auth_exists =  "1"
        # if import_value does not work continue
        except:
            pass
        # a cognito user pool that uses cognito managed login sign up and password recovery
        user_pool = _cognito.UserPool(
            self, "IdpUserPool0",
            user_pool_name="IdpUserPool0",
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
                domain_prefix="cw-workshop-demo-domain"
            )
        )
        
        
        redirect_uri = Fn.import_value("RedirectUri")
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
        method_api_backend = api_backend_resource.add_method(
            "POST", api_backend_integration,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=apigateway.CognitoUserPoolsAuthorizer(
                self, "IdpAuthorizer",
                cognito_user_pools=[user_pool])
                )
        method_api_backend_get = api_backend_resource.add_method(
            "GET", api_backend_get_integration,
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=apigateway.CognitoUserPoolsAuthorizer(
                self, "api_backend_method_get",
                cognito_user_pools=[user_pool])
                )
        deployment = apigateway.Deployment(self, "Deployment",
            api=api_gateway,
            description="This is the CodeWhisperer API Gateway Deployment")
            
        # create an apigateway stage deployment called prod
        # api_backend_stage = api_gateway.Stage(
        #     "prod",
        #     stage_name="prod")
        
        # get the ssm parameter for CW-workshop-post-autentication-lambda
        post_autentication_lambda_arn = ssm.StringParameter.value_for_string_parameter(self, "CW-workshop-post-autentication-lambda")
        # reference the post_autentication_lambda
        post_autentication_lambda = _lambda.Function.from_function_arn(self, "post_autentication_lambda_ref", post_autentication_lambda_arn)
        user_pool.add_trigger(_cognito.UserPoolOperation.POST_AUTHENTICATION, post_autentication_lambda)
        # create a resurce based polocy for the post_autentication_lambda allows cognito service to invoke it
        post_autentication_lambda.add_permission("post_autentication_lambda_permission",
            source_arn=post_autentication_lambda_arn,
            principal=iam.ServicePrincipal("cognito-idp.amazonaws.com"))
        
            
        
        
        # CfnOutput the user_pool login url
        CfnOutput(self, "UserPoolLoginUrl", value=sign_in_url)