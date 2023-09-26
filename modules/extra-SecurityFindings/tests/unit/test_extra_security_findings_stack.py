import aws_cdk as core
import aws_cdk.assertions as assertions

from extra_security_findings.extra_security_findings_stack import ExtraSecurityFindingsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in extra_security_findings/extra_security_findings_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExtraSecurityFindingsStack(app, "extra-security-findings")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
