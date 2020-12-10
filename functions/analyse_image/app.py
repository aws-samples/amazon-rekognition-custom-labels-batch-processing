import json
import os
import boto3
import logging
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Create s3 client
    s3_client = boto3.client('s3')
    #  Create Rekognition Client
    client = boto3.client('rekognition')
    model_arn = os.environ['rekognition_model_project_version_arn']
    # print('model_arn: %s' % model_arn)
    # print('Event: %s' % event)
    data2 = json.loads(event['Records'][0]['body'])
    # print('Bucket: %s' % data2["Records"][0]["s3"]['bucket']['name'])
    # print('Key: %s' % data2["Records"][0]["s3"]
    #       ["object"]["key"].replace("+", " "))
    bucket = data2["Records"][0]["s3"]['bucket']['name']
    image = data2["Records"][0]["s3"]["object"]["key"].replace("+", " ")
    # print('Bucket: %s' % bucket)
    # print('Image: %s' % image)
    # process using S3 object
    response = client.detect_custom_labels(
        ProjectVersionArn = model_arn,
        Image={
            'S3Object': {
                'Bucket': bucket, 
                'Name': image}
            },
        MinConfidence = 70
    )
    print('Labels Response: %s' % response)
    # Get the custom labels
    labels = response['CustomLabels']
    print('Labels: %s' % labels)
    # write image to final bucket and delete from incoming bucket
    s3 = boto3.resource('s3')
    finalbucket = os.environ['Final_S3_Bucket_Name']
    copy_source = {
        'Bucket': bucket,
        'Key': image
    }
    s3.meta.client.copy(copy_source, finalbucket, image)
    # Delete file from incoming s3 - #TODO
    # #TODO
    # Dump json file with label data in final bucket
    json_object = json.dumps(labels)
    s3_client.put_object(
        Body=str(json_object),
        Bucket=finalbucket,
        Key=image+'.json'
    )
    return {'status': '200'}
