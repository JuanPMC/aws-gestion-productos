from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as db,
    aws_apigateway as api,
    aws_sqs as sqs,
    aws_lambda as lambda_func,
    aws_sns as sns,
    RemovalPolicy,
    aws_apigatewayv2 as gateway,
    aws_lambda_event_sources as event_sources,
    aws_sns_subscriptions as sns_actions
    )
from constructs import Construct
from . import constants

class ProyectoW1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app_gateway = gateway.HttpApi(
            self, "http_api",
            api_name="MyHttpApi"
        )
        

        queue = sqs.Queue(
            self, "MyQueue",
            queue_name="MyQueue",
            fifo=False,
            
        )

        # Obtener ARN de integración para SQS
        integration_uri = f"arn:aws:apigateway:{self.region}:sqs:path/{self.account}/{queue.queue_name}"
        
        join_gateway_sqs = gateway.HttpIntegration(self,"join_gateway_sqs",
            http_api=app_gateway,
            integration_type=gateway.HttpIntegrationType.HTTP_PROXY,
            integration_uri=integration_uri,
            method=gateway.HttpMethod.POST
        )

        entry_func = lambda_func.Function(scope=self,id="lambda_entry",
                             runtime=lambda_func.Runtime.PYTHON_3_10,
                             function_name="lambda_entry",
                             handler="index.lambda_handler",
                             code=lambda_func.Code.from_inline(constants.ENTRY_LAMBDA_CODE)
        )
         # Grant Lambda permission to read from SQS
        queue.grant_consume_messages(entry_func)
        
        # Configure SQS as an event source for Lambda
        event_source_lamda1 = event_sources.SqsEventSource(queue)
        entry_func.add_event_source(event_source_lamda1)

        database = db.Table(
            self, "order_table",
            table_name="OrderTable",
            partition_key=db.Attribute(
                name="OrderId",
                type=db.AttributeType.STRING
            ),
            billing_mode=db.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            stream=db.StreamViewType.NEW_IMAGE
        )

        notify_func = lambda_func.Function(scope=self,id="lambda_notify",
                             runtime=lambda_func.Runtime.PYTHON_3_10,
                             function_name="lambda_notify",
                             handler="index.lambda_handler",
                             code=lambda_func.Code.from_inline(constants.ENTRY_LAMBDA_CODE)
        )

        # Grant permissions to the function
        database.grant_read_data(notify_func)
        # Configure function trigger
        event_source_lamda2 = event_sources.DynamoEventSource(database, starting_position=lambda_func.StartingPosition.LATEST)
        notify_func.add_event_source(event_source_lamda2)

        topic = sns.Topic(
            self, "MyTopic",
            topic_name="MyTopic",
            display_name="My SNS Topic for Notifications"
        )

        # Creant priviledges
        topic.grant_publish(notify_func)
        topic.add_subscription(sns_actions.EmailSubscription("fake@email.com"))
