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
import boto3
import os


def lambda_handler(event, context):

    lambda_client = boto3.client('lambda')
    try:
        uuid_response = lambda_client.list_event_source_mappings(
            FunctionName=os.environ['analyze_lambda_arn']
        )
    except Exception as e:
        print(e)

    mylist = uuid_response['EventSourceMappings']
    uuiddata = mylist[0]['UUID']
    analyse_lambda_uuid = uuiddata

    try:
        response = lambda_client.get_event_source_mapping(
            UUID=analyse_lambda_uuid
        )
    except Exception as e:
        print(e)

    # State (string) -- The state of the event source mapping. It can be one of the following: Creating , Enabling , Enabled , Disabling , Disabled , Updating , or Deleting .
    disabled_states = ["Disabled", "Disabling"]
    enabled_states = ["Enabling", "Enabled"]
    
    # Disable
    if (event[0]['Action'] == 'disable'):
        if (response['State'] in disabled_states):
            # Do Nothing
            return 'Already disabled'
        else:
            try:
                response = lambda_client.update_event_source_mapping(
                    UUID=analyse_lambda_uuid,
                    Enabled=False
                )
            except Exception as e:
                print(e)
    else:
        # Enable
        if (event[0]['Action'] == 'enable'):
            if (response['State'] in enabled_states):
                # Do Nothing
                return 'Already_Running'
            else:
                try:
                    response = lambda_client.update_event_source_mapping(
                        UUID=analyse_lambda_uuid,
                        Enabled=True
                    )
                except Exception as e:
                    print(e)
    
    print("Current state is:", response['State'])
    return response['State']
