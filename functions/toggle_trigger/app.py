import json
import boto3
import os


def lambda_handler(event, context):
    # TODO implement
    lambda_client = boto3.client('lambda')
    # lambda_uuid = uuid_analyze_lambda
    uuid_response = lambda_client.list_event_source_mappings(
        FunctionName = os.environ['analyze_lambda_arn']
        )
    
    # print('UUID response: %s' % uuid_response)
    # print('UUID responseEventSourceMappings: %s' % uuid_response['EventSourceMappings'])
    mylist = uuid_response['EventSourceMappings']
    uuiddata = mylist[0]['UUID']
    analyse_lambda_uuid = uuiddata
    response = lambda_client.get_event_source_mapping(
        UUID = analyse_lambda_uuid
        )
    # State (string) -- The state of the event source mapping. It can be one of the following: Creating , Enabling , Enabled , Disabling , Disabled , Updating , or Deleting .
    running_states = ["Enabling", "Enabled"]
    if response['State'] in running_states:
        # Disable
        response = lambda_client.update_event_source_mapping(
           UUID = analyse_lambda_uuid,
            Enabled = False
        )
    else:
        # Enable
        response = lambda_client.update_event_source_mapping(
            UUID = analyse_lambda_uuid,
            Enabled = True
        )
    return response['State']
