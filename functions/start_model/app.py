
import boto3
import os


def lambda_handler(event, context):
    # TODO implement
    rekog_client = boto3.client('rekognition')
    projectversionarn = os.environ['rekog_model_project_version_arn']
    projectarn = os.environ['rekog_model_project_arn']
    running_states = ['STARTING', 'RUNNING']
    # Check if already running
    # Call Custom Rekog
    isrunning_response = rekog_client.describe_project_versions(
        ProjectArn=projectarn
        )
    running_status = isrunning_response['ProjectVersionDescriptions'][0]['Status']
    if running_status in running_states:
        # Do nothing
        print('Model Start Status: %s' % running_status)
    else:
        # If not running - Start
        running_status = rekog_client.start_project_version(
            ProjectVersionArn=projectversionarn,                
            MinInferenceUnits=1 #Can be increased upto 5 for running multiple inference units
            )
        print('Model Start Status: %s' % running_status)
    return running_status
