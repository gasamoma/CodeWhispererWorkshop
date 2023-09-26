#!/usr/bin/env python3
import os

import aws_cdk as cdk

from must_cognito_security.must_cognito_security_stack import MustCognitoSecurityStack


app = cdk.App()
MustCognitoSecurityStack(app, "MustCognitoSecurityStack-78e52dcb-30dd-447f-bcc3-da13985e7c24",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
