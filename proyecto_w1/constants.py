ENTRY_LAMBDA_CODE="""import boto3, uuid

client = boto3.resource('dynamodb')
table = client.Table("orders")

def lambda_handler(event, context):
    for record in event['Records']:
        print("test")
        payload = record["body"]
        print(str(payload))
        table.put_item(Item= {'orderID': str(uuid.uuid4()),'order':  payload})
"""
NOTIFY_LAMBDA_CODE="""import boto3, json

client = boto3.client('sns')

def lambda_handler(event, context):

    for record in event["Records"]:

        if record['eventName'] == 'INSERT':
            new_record = record['dynamodb']['NewImage']    
            response = client.publish(
                TargetArn='<Enter Amazon SNS ARN for the POC-Topic>',
                Message=json.dumps({'default': json.dumps(new_record)}),
                MessageStructure='json'
            )
"""