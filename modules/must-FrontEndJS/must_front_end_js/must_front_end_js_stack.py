from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_s3 as s3,
    aws_cloudfront as _cf,
    aws_s3_deployment as s3deploy,
    aws_cloudfront_origins as origins,
    # aws_sqs as sqs,
)
from constructs import Construct

class MustFrontEndJsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # an s3 bucket for the web page that uses the files in the web folder
        s3_website_bucket = s3.Bucket(
            self, "CW-worshop-WebsiteBucket"
            )
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./web/")],
            destination_bucket=s3_website_bucket
        )
        
        # create an origin access identity
        oin = _cf.OriginAccessIdentity(
            self, "CW-workshopOriginAccessIdentity",
            comment="CW-workshopOriginAccessIdentity")
        # give permisions to the origin_access_identity to access the s3_website_bucket
        s3_website_bucket.grant_read(oin)
        # a cloudfront distribution for the s3_website_bucket
        cloudfront_website = _cf.Distribution(
            self,
            "CW-workshopWebsiteDistribution",
            default_behavior=_cf.BehaviorOptions(
                allowed_methods=_cf.AllowedMethods.ALLOW_ALL,
                origin=origins.S3Origin(
                    s3_website_bucket,
                    origin_access_identity=oin)))