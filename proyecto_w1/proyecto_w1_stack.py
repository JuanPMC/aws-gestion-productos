from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as db,
    aws_apigateway as api,
    aws_sqs as sqs,
    aws_lambda as lambda_func,
    aws_sns as sns,
    RemovalPolicy,
    Duration
)
from constructs import Construct
from . import constants

class ProyectoW1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        database = db.Table(
            self, "order_table",
            table_name="OrderTable",
            partition_key=db.Attribute(
                name="OrderId",
                type=db.AttributeType.STRING
            ),
            billing_mode=db.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        entry_func = lambda_func.Function(scope=scope,id="lambda_entry",
                             runtime=lambda_func.Runtime.PYTHON_3_10,
                             function_name="lambda_entry",
                             code=lambda_func.Code.from_inline(constants.ENTRY_LAMBDA_CODE)
        )

        notify_func = lambda_func.Function(scope=scope,id="lambda_notify",
                             runtime=lambda_func.Runtime.PYTHON_3_10,
                             function_name="lambda_notify",
                             code=lambda_func.Code.from_inline(constants.ENTRY_LAMBDA_CODE)
        )

        queue = sqs.Queue(
            scope, "MyQueue",
            queue_name="MyQueue",
            fifo=False
        )

        topic = sns.Topic(
            self, "MyTopic",
            topic_name="MyTopic",
            display_name="My SNS Topic for Notifications"
        )