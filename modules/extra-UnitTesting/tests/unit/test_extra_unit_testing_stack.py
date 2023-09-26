import aws_cdk as core
import aws_cdk.assertions as assertions

from extra_unit_testing.extra_unit_testing_stack import ExtraUnitTestingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in extra_unit_testing/extra_unit_testing_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExtraUnitTestingStack(app, "extra-unit-testing")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
