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
 
import boto3
import os


def lambda_handler(event, context):
    
    rekog_client = boto3.client('rekognition')
    projectversionarn = os.environ['rekog_model_project_version_arn']
    projectarn = os.environ['rekog_model_project_arn']
    # running_states = ['STARTING', 'RUNNING']
    projectversionname = projectversionarn.split("/")[3]
    # Check if already running
    # Call Custom Rekognition project version
    try:
        isrunning_response = rekog_client.describe_project_versions(
            ProjectArn=projectarn,
            VersionNames=[projectversionname]
        )
    except Exception as e:
        print(e)
        
    running_status = isrunning_response['ProjectVersionDescriptions'][0]['Status']
    if running_status == 'RUNNING':
        # Do nothing
        print('Model Start Status: %s' % running_status)
        return 'RUNNING'
    if running_status == 'STARTING':
        # Do nothing
        print('Model Start Status: %s' % running_status)
        return 'STARTING'
    else:
        # If not running - Start
        try:
            running_status = rekog_client.start_project_version(
                ProjectVersionArn = projectversionarn,                
                MinInferenceUnits = 1 #Can be increased upto 5 for running multiple inference units
            )
        except Exception as e:
            print(e)
        return running_status

