import boto3
import os


def lambda_handler(event, context):
    # TODO implement
    # Create SQS client
    sqs = boto3.client('sqs')
    src_queue_url = os.environ['SQS_Queue_URL']
    # Check message available in Incoming Queue
    response = sqs.get_queue_attributes(
         QueueUrl=src_queue_url,
         AttributeNames=[
              'ApproximateNumberOfMessages'
              ]
         )
    count = response['Attributes']['ApproximateNumberOfMessages'][0]
    print('Message Count in Incoming Queue: %s' % count)
    if (int(count) > 0):
        return 'incoming'
    else:
        return 'stop'
