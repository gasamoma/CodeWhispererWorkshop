import aws_cdk as core
import aws_cdk.assertions as assertions

from extra_log_forensis.extra_log_forensis_stack import ExtraLogForensisStack

# example tests. To run these tests, uncomment this file along with the example
# resource in extra_log_forensis/extra_log_forensis_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExtraLogForensisStack(app, "extra-log-forensis")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
