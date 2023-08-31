from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda_python_alpha as python,
    aws_lambda as _lambda,
    Duration,
    Fn,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
    aws_athena as athena,
    # aws_sqs as sqs,
)
import os
from constructs import Construct

class ExtraLogForensisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        etl_lambda = python.PythonFunction(self, "LambdaETL",
            entry="app/lambda",
            index="etl.py",  
            handler="handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                #"BUCKET_NAME": s3_bucket.bucket_name,
                "PREFIX": "output/",
                },
            timeout=Duration.seconds(120),
            layers=[
                python.PythonLayerVersion(self, "etl_layer",
                    entry="lib/python",
                    compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
                )
            ]
        )
        bucket_name = os.environ.get("BUCKET_NAME", "athena-results-bucket")
        if not bucket_name:
            raise ValueError("BUCKET_NAME environment variable is not set")
        
        # s3 bucket for athena query results
        s3_bucket = s3.Bucket(self, bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN
            )
        # create a ResultConfigurationProperty
        result_configuration = athena.CfnWorkGroup.ResultConfigurationProperty(
            # outptput_location  the s3 path
            output_location='s3://' + s3_bucket.bucket_name + "/queryResults/",)
        # create a WorkGroupConfigurationProperty
        work_group_configuration = athena.CfnWorkGroup.WorkGroupConfigurationProperty(
            enforce_work_group_configuration=True,
            result_configuration=result_configuration,
            # add maximum bytesScannedCutoffPerQuery to 1 Gb
            bytes_scanned_cutoff_per_query=104857600)
        
        # use a CfnAthenaWorkGroup
        athena_work_group = athena.CfnWorkGroup(self, "AthenaWorkGroup",
            name="AthenaLogWorkgroup",
            description="Athena query to get logs from CloudTrail",
            state="ENABLED",
            work_group_configuration=work_group_configuration)
                    
        
        # use a CfnNamedQuery
        # athena_query = athena.CfnNamedQuery(self, "AthenaQuery",
        #     database=athena_database.database_name,
        #     description="Athena query to get logs from CloudTrail",
        #     name=athena_query_name,
        #     query_string=athena_query_string,
        #     work_group=athena_work_group.name
        # )
        
        
        # CfnOutput the post_autentication_lambda arn
        CfnOutput(self, "etl_lambda", value=etl_lambda.function_arn, export_name="CW-workshop-etl-lambda")
