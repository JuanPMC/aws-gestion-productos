import aws_cdk as core
import aws_cdk.assertions as assertions

from proyecto_w1.proyecto_w1_stack import ProyectoW1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in proyecto_w1/proyecto_w1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProyectoW1Stack(app, "proyecto-w1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
