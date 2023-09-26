import aws_cdk as core
import aws_cdk.assertions as assertions

from must_api_backend.must_api_backend_stack import MustApiBackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in must_api_backend/must_api_backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MustApiBackendStack(app, "must-api-backend")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
