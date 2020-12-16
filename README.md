# serverless-computer-vision-label-detection 

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. The application can be used for Computer Vision inferencing using Amazon Rekognition or Amazon Lookout for Vision. It includes the following files and folders:

- functions - Code for the application's Lambda functions to check the presence of messages in a Queue, start or stop a Amazon Rekognition Custom Label Model, Analyse Images using a Custom Label Model.
- statemachine - Definition for the state machine that orchestrates the workflow and acts as the control plane.
- template.yaml - A template that defines the application's AWS resources.

This application creates a serverless Amazon Rekognition Custom Label Detection workflow which runs on a pre-defined schedule (note that the schedule is disabled by default at deployment to avoid incurring charges). It demonstrates the power of Step Functions to orchestrate Lambda functions and other AWS resources to form complex and robust workflows, coupled with event-driven development using Amazon EventBridge.

This application can also be used for creating a serverless image label inferencing pipeline for Amazon Lookout for Vision.

The application uses several AWS resources, including Amazon Simple Storage Service, Amazon Simple Queue Service, Step Functions state machines, Lambda functions and an EventBridge rule trigger. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

Please note that this code is provided as a working sample. However, if you intend to use it in production, it is recommended that you implement production best practices including but not limited to error handling, message visibility settings, timeouts, storage lifecycle rules etc. 

When deployoing this application you will need to provide the following two parameters for your Custom Label Project.
1. Amazon Rekognition Model Project ARN
2. Amazon Rekognition Model Project Version ARN

## License
     
This library is licensed under the MIT-0 License. See the LICENSE file.
