import aws_cdk as core
import aws_cdk.assertions as assertions

from extra_proactive_log_analisys.extra_proactive_log_analisys_stack import ExtraProactiveLogAnalisysStack

# example tests. To run these tests, uncomment this file along with the example
# resource in extra_proactive_log_analisys/extra_proactive_log_analisys_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExtraProactiveLogAnalisysStack(app, "extra-proactive-log-analisys")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
