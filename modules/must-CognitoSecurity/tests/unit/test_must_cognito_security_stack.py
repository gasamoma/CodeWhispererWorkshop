import aws_cdk as core
import aws_cdk.assertions as assertions

from must_cognito_security.must_cognito_security_stack import MustCognitoSecurityStack

# example tests. To run these tests, uncomment this file along with the example
# resource in must_cognito_security/must_cognito_security_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MustCognitoSecurityStack(app, "must-cognito-security")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
