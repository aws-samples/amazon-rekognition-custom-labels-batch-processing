# Batch Image Processing with Amazon Rekognition Custom Labels 

Amazon Rekognition is a computer vision service that makes it easy to add image and video analysis to your applications using proven, highly scalable, deep learning technology that requires no machine expertise to use. With Amazon Rekognition, you can identify objects, people, text, scenes, and activities in images and videos, as well as detect any inappropriate content. Amazon Rekognition also provides highly accurate facial analysis and facial search capabilities that you can use to detect, analyze, and compare faces for a wide variety of use cases.

Amazon Rekognition Custom Labels allows you to identify the objects and scenes in images that are specific to your business needs. For example, you can find your logo in social media posts, identify your products on store shelves, classify machine parts in an assembly line, distinguish healthy and infected plants etc. Amazon Rekognition Custom Labels provides a very simple end-to-end experience where you start by labeling a dataset. Custom Labels then build a custom machine learning model for you by inspecting the data and selecting the right machine learning algorithm. Once your model is trained you can start using your model immediately for image analysis. If you expect to process images in batches (e.g. once a day or week, or at scheduled times during the day), you can provision your custom model at scheduled times.

In this post, we show how you can build cost-optimal batch solution with Amazon Rekognition Custom Labels which provision your custom model at scheduled times, process all your images, and then deprovision your resources to avoid incurring extra cost.

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI or using the Cloudformation links below. It includes the following files and folders:

- \functions - Code for the application's Lambda functions to check the presence of messages in a Queue, start or stop a Amazon Rekognition Custom Label Model, Analyse Images using a Custom Label Model.
- template.yaml - A template that defines the application's AWS resources.

This application creates a serverless Amazon Rekognition Custom Label Detection workflow which runs on a pre-defined schedule (note that the schedule is enabled by default at deployment). It demonstrates the power of Step Functions to orchestrate Lambda functions and other AWS resources to form complex and robust workflows, coupled with event-driven development using Amazon EventBridge.

Solution Architecture Diagram:
The following architecture diagram shows how you can design a serverless workflow to process images in batches with Amazon Rekognition Custom Labels.

<img width="814" alt="Architecture Diagram" src="docs/SA-Amazon Rekognition Custom Labels Batch Image Processing.png">

1. As an image is stored in Amazon S3 bucket, it triggers a message which gets stored in an Amazon SQS queue.
2. Amazon EventBridge is configured to trigger an AWS Step Function workflow at certain frequency (1 hour by default).
3. As the workflow runs it checks the number of items in the Amazon SQS queue. If there are no items to process in the queue, workflow ends. If there are items to process in the queue, workflow starts the Amazon Rekognition Custom Labels model and enables Amazon SQS integration with a Lambda function to process those images.
4. As integration between Amazon SQS queue and Lambda is enabled, Lambda start processing images using Amazon Rekognition Custom Labels.
5. Once all the images are processed, workflow stops the Amazon Rekognition Custom Labels model and disables integration between Amazon SQS queue and Lambda function.

The application uses several AWS resources, including Amazon Simple Storage Service, Amazon Simple Queue Service, Step Functions state machines, Lambda functions and an EventBridge rule trigger. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

Please note that this code is provided as a working sample. However, if you intend to use it in production, it is recommended that you implement production best practices including but not limited to error handling, message visibility settings, timeouts, storage lifecycle rules etc. 

### Usage

#### Prerequisites

1. To deploy the sample application, you will require an AWS account. If you don’t already have an AWS account, create one at <https://aws.amazon.com> by following the on-screen instructions. Your access to the AWS account must have IAM permissions to launch AWS CloudFormation templates that create IAM roles.

2. Please refer [here](https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/gs-introduction.html) for instructions on getting started with Amazon Rekognition Custom Labels. When deploying this application you will need to provide the following two parameters for your Custom Label Project.
   - Amazon Rekognition Model Project ARN: The Amazon Resource Name (ARN) of the Amazon Rekognition Custom Labels project that contains the models you want to use. 
   - Amazon Rekognition Model Project Version ARN: The Amazon Resource Name(ARN) of the model version that you want to use.


#### Deployment

The demo application is deployed as an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.

> **Note**  
> You are responsible for the cost of the AWS services used while running this sample deployment. There is no additional cost for using this sample. For full details, see the following pricing pages for each AWS service you will be using in this sample. Prices are subject to change.
>
> - [Amazon Rekognition Pricing](https://aws.amazon.com/rekognition/pricing/)
> - [Amazon Lookout for Vision Pricing](https://aws.amazon.com/lookout-for-vision/pricing/)
> - [Amazon S3 Pricing](https://aws.amazon.com/s3/pricing/)
> - [Amazon SQS Pricing](https://aws.amazon.com/sqs/pricing/)
> - [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
> - [AWS Step Functions Pricing](https://aws.amazon.com/step-functions/pricing/)

1. Deploy the latest CloudFormation template by following the link below for your preferred AWS region:

| Region                                | Launch Template                                                                                                                                                                                                                                                                                     |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **US East (N. Virginia)** (us-east-1) | [![Launch the LabelDetection Stack with CloudFormation](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=LabelDetection&templateURL=https://solution-builders-us-east-1.s3.us-east-1.amazonaws.com/serverless-computer-vision-label-detection/latest/template.yaml) |
| **US East (Ohio)** (us-east-2)        | [![Launch the LabelDetection Stack with CloudFormation](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=LabelDetection&templateURL=https://solution-builders-us-east-2.s3.us-east-2.amazonaws.com/serverless-computer-vision-label-detection/latest/template.yaml) |
| **US West (Oregon)** (us-west-2)      | [![Launch the LabelDetection Stack with CloudFormation](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=LabelDetection&templateURL=https://solution-builders-us-west-2.s3.us-west-2.amazonaws.com/serverless-computer-vision-label-detection/latest/template.yaml) |
| **EU (Ireland)** (eu-west-1)          | [![Launch the LabelDetection Stack with CloudFormation](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=LabelDetection&templateURL=https://solution-builders-eu-west-1.s3.eu-west-1.amazonaws.com/serverless-computer-vision-label-detection/latest/template.yaml) |

2. If prompted, login using your AWS account credentials.
3. You should see a screen titled "_Create Stack_" at the "_Specify template_" step. The fields specifying the CloudFormation template are pre-populated. Click the _Next_ button at the bottom of the page.
4. On the "_Specify stack details_" screen you may customize the following parameters of the CloudFormation stack:

   - **Stack Name:** (Default: LabelDetection) This is the name that is used to refer to this stack in CloudFormation once deployed.
   - **RekognitionModelProjectARN:** The Amazon Rekognition Model Project Arn
   - **RekognitionModelProjectVersionARN:** The Amazon Rekognition Model Project Version Arn

   When completed, click _Next_

5. [Configure stack options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html) if desired, then click _Next_.
6. On the review you screen, you must check the boxes for:

   - "_I acknowledge that AWS CloudFormation might create IAM resources_"
   - "_I acknowledge that AWS CloudFormation might create IAM resources with custom names_"
   - "_I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND_"

   These are required to allow CloudFormation to create a Role to allow access to resources needed by the stack and name the resources in a dynamic way.

7. Click _Create Change Set_
8. On the _Change Set_ screen, click _Execute_ to launch your stack.
   - You may need to wait for the _Execution status_ of the change set to become "_AVAILABLE_" before the "_Execute_" button becomes available.
9. Wait for the CloudFormation stack to launch. Completion is indicated when the "Stack status" is "_CREATE_COMPLETE_".
   - You can monitor the stack creation progress in the "Events" tab.
10. Note the _url_ displayed in the _Outputs_ tab for the stack. This is used to access the application.

#### Testing the workflow

To test your workflow, complete the following steps:
1. Upload sample images to the input S3 bucket that was created by the solution (Example: xxxx-sources3bucket-xxxx).
2. Go to AWS Step Function console and select the state machine created by the solution (Example: CustomCVStateMachine-xxxx). You will see an execution triggered by the EventBridge at every hour.
3. To test the solution, you can also manually start the workflow by clicking on the “Start execution” button.
4. As images are processed you can go to the output S3 bucket (Example: xxxx-finals3bucket-xxxx) to see the JSON output for each image. The Final S3 bucket holds the images that have been processed along with the inferenced custom label json. As the images get processed, they will be deleted from the source bucket.


### Removing the application

To remove the application open the AWS CloudFormation Console, click on the name of the project, right-click and select "_Delete Stack_". Your stack will take some time to be deleted. You can track its progress in the "Events" tab. When it is done, the status will change from "_DELETE_IN_PROGRESS_" to "_DELETE_COMPLETE_". It will then disappear from the list. 

**Note:** Please note that the provided configuration will ensure that the Amazon S3 buckets and their contents are retained when removing the application via the AWS Cloudformation console. This is to ensure that no data is accidently lost while removing the application. The buckets can be deleted from the S3 console.


## License
     
This library is licensed under the MIT-0 License. See the LICENSE file.
