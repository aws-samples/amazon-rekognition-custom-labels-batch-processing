# /*
#  * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  * SPDX-License-Identifier: MIT-0
#  *
#  * Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  * software and associated documentation files (the "Software"), to deal in the Software
#  * without restriction, including without limitation the rights to use, copy, modify,
#  * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  * permit persons to whom the Software is furnished to do so.
#  *
#  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#  */

import json
import os
import boto3
import logging
import string
import random
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Create s3 client
    s3_client = boto3.client('s3')
    #  Create Rekognition Client
    client = boto3.client('rekognition')
    model_arn = os.environ['rekognition_model_project_version_arn']

    for msg in event["Records"]:
        msg_payload = json.loads(msg["body"])
        print("msg_payload: ", msg_payload)
        if "Records" in msg_payload:
            bucket = msg_payload["Records"][0]["s3"]["bucket"]["name"]
            image = msg_payload["Records"][0]["s3"]["object"]["key"].replace("+", " ")
            response = client.detect_custom_labels(
                ProjectVersionArn = model_arn,
                Image={
                    'S3Object': {
                        'Bucket': bucket, 
                        'Name': image}
                    },
                MinConfidence = 70
            )
            # Get the custom labels
            labels = response['CustomLabels']
            # write image to final bucket and delete from incoming bucket
            s3 = boto3.resource('s3')
            finalbucket = os.environ['Final_S3_Bucket_Name']
            copy_source = {
                'Bucket': bucket,
                'Key': image
            }
            random_letters = ''.join(random.choice(string.ascii_letters) for i in range(10))
            put_image_name = random_letters+'-'+image
            s3.meta.client.copy(copy_source, finalbucket, put_image_name)

            # Dump json file with label data in final bucket
            json_object = json.dumps(labels)
            s3_client.put_object(
                Body = str(json_object),
                Bucket = finalbucket,
                Key = put_image_name+'.json'
            )

            # Delete file from incoming s3
            s3_client.delete_object(
                Bucket = bucket,
                Key = image,
            )

        else:
            # Invalid Message - To Be removed from Queue
            print("Invalid msg: ", msg)
            
    return {'status': '200'}
