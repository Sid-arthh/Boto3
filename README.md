# Boto3
## Handling Few real world use case of AWS using boto3

# 1.CheckS3LifeCycleEnable
### Python Script which checks if Any S3 bucket has LIFE CYCLE POLICY enabled
### Prerequisites

- AWS account with appropriate permissions to access S3 and retrieve bucket lifecycle configurations.
- Python 3.x installed on your local machine or Lambda environment.
- Boto3 library installed (`pip install boto3`).

### Usage

1. Clone the repository or download the Python script file.

2. Ensure that you have an IAM role with the necessary permissions:
   - Create an IAM role with the required permissions to access S3 and retrieve bucket lifecycle configurations. You can define these permissions using an IAM policy.
   - Attach the IAM role to the AWS Lambda function. This ensures that the Lambda function has the necessary permissions to access S3.

3. Update the AWS credentials and region in the script:
   - If running locally, configure your AWS credentials using the AWS CLI or provide credentials via environment variables.
   - If using AWS Lambda, ensure that the Lambda execution role has the necessary permissions to access S3 and retrieve bucket lifecycle configurations.

4. Execute the script:
   - If running locally, execute the script using Python: `checkS3LifeCycleEnable.py`.
   - If using AWS Lambda, create a Lambda function and upload the script code as a ZIP package. Configure the function to trigger based on your requirements.

5. Check the output:
   - The script will iterate through each S3 bucket and display a message indicating if the bucket has lifecycle policies enabled or not.

### Code Explanation

#### The script consists of the following main components:
This line imports the boto3 library, which is the AWS SDK for Python. It provides the necessary functions to interact with AWS services
      
    import boto3

This is the entry point of the Lambda function. The lambda_handler function is the function that AWS Lambda invokes when the function is triggered. In this case, it calls the check_s3_lifecycle_policies function.
   
    def lambda_handler(event, context):
       check_s3_lifecycle_policies()

The check_s3_lifecycle_policies function is defined to perform the check for lifecycle policies on S3 buckets. It creates an S3 client using the boto3.client function.

    def check_s3_lifecycle_policies():
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get the list of all S3 buckets
    response = s3_client.list_buckets()

    # Iterate through each bucket
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

Inside the loop, it attempts to retrieve the lifecycle configuration for the current bucket using the get_bucket_lifecycle_configuration method. It passes the bucket name as a parameter and assigns the response to the lifecycle_configuration variable.
    
    try:
            response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            lifecycle_configuration = response['Rules']

It then checks if the lifecycle_configuration variable contains any rules, indicating that the bucket has lifecycle policies. If there are rules, it prints a message indicating that the bucket has lifecycle policies. If there are no rules, it prints a message indicating that the bucket does not have any lifecycle policies.

            if lifecycle_configuration:
                print(f"Bucket: {bucket_name} has lifecycle policies.")
            else:
                print(f"Bucket: {bucket_name} does not have any lifecycle policies.")

In case of an exception where there is no lifecycle configuration for the bucket, the script catches the NoSuchLifecycleConfiguration exception and prints a message indicating that the bucket does not have any lifecycle policies.

    except s3_client.exceptions.NoSuchLifecycleConfiguration:
            print(f"Bucket: {bucket_name} does not have any lifecycle policies.")

# 2.CreateAMIwithEc2Tag

This Script Creates an AMI image of an Instance with Using the Tags for that specific Instance.

IAM Role for Lambda Function:

Create an IAM role for your Lambda function that allows it to access the necessary AWS services. This role should have the following permissions:
        
        ec2:DescribeInstances - to retrieve information about EC2 instances.
        ec2:CreateImage - to create an AMI of the EC2 instance.
        ec2:CreateTags - to add tags to the newly created AMI.
        ec2:DescribeTags - to retrieve information about tags on EC2 resources.
Ensure that you attach this IAM role to your Lambda function during its configuration.

### Code Explanation

These lines import the necessary libraries. boto3 is the AWS SDK for Python, and datetime is used to generate a timestamp for the AMI name.

      import boto3
      from datetime import datetime

The lambda_handler function is the entry point of the AWS Lambda function. It takes in the event and context parameters, but they are not used in this script. You need to specify the tag_key and tag_value variables with the appropriate values to filter the EC2 instance you want to create an AMI backup for.

      def lambda_handler(event, context):
          # Specify the tag key and value to filter the EC2 instance
          tag_key = 'your-tag-key'
          tag_value = 'your-tag-value'

This line creates an EC2 client using the boto3.client function. It uses the default credentials available to the Lambda function, which are provided by the IAM role assigned to the Lambda function.

      ec2_client = boto3.client('ec2')


The script uses the describe_instances method of the EC2 client to retrieve information about EC2 instances that match the specified tag key and value. It sends a request to AWS and stores the response in the response variable.

      response = ec2_client.describe_instances(Filters=[
           {
               'Name': 'tag:' + tag_key,
               'Values': [tag_value]
           }
       ])

This if condition checks if any instances were found based on the specified tag. It verifies if the 'Reservations' key is present in the response and if there are any items in the 'Reservations' list.


      if 'Reservations' in response and response['Reservations']:

If instances were found, this line extracts the instance ID from the response. It assumes that there is only one instance matching the specified tag, so it uses the first instance in the list.

      instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

This section generates a timestamp using the current date and time, and then creates a unique AMI name by combining the instance ID and timestamp. The AMI name will be in the format: "AMI backup {instance_id} {timestamp}".

      timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
      ami_name = 'AMI backup ' + instance_id + ' ' + timestamp

The script uses the create_image method of the EC2 client to create an AMI of the specified instance. It provides the instance ID, AMI name, description, and sets NoReboot to True to ensure that the instance doesn't need to be rebooted during the AMI creation process. The response is stored in the response variable.

      response = ec2_client.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            Description='Automated AMI backup of ' + instance_id,
            NoReboot=True
        )


If instances were found, the script extracts the newly created AMI ID from the response and prints it. If no instances were found, it prints a message indicating that no instances were found based on the specified tag.

           ami_id = response['ImageId']
           print('AMI created with ID:', ami_id)
      else:
           print('No instances found based on the specified tag')

# 3.ListEc2Services

## This Python script Interact with AWS services and List all the services Running inside a specific Instance . It utilizes the AWS SDK for Python (Boto3) to interact with AWS services.

## Prerequisites

- AWS account with appropriate permissions to use SSM Run Command and access EC2 instances.
- Python 3.x installed on your local machine or Lambda environment.
- Boto3 library installed (`pip install boto3`).

## Usage

1. Clone the repository or download the Python script file.

2. Update the script with the following information:
   - Specify the EC2 instance ID (`ec2_instance_id`) of the target instance where you want to execute the command.
   - Specify the command (`command`) that you want to run on the EC2 instance.

         command = 'systemctl list-units --type=service'

3. Configure your AWS credentials:
   - If running locally, configure your AWS credentials using the AWS CLI or by setting environment variables.
   - If using AWS Lambda, ensure that the Lambda execution role has the necessary permissions to access SSM and execute commands on EC2 instances.

4. Execute the script:
   - If running locally, execute the script using Python: `ListEc2Services.py`.
   - If using AWS Lambda, create a Lambda function and upload the script code as a ZIP package. Configure the function to trigger based on your requirements.

5. Check the output:
   - The script sends the command to the specified EC2 instance using SSM Run Command.
   - It waits for the command execution to complete and retrieves the command invocation details.
   - If the command execution is successful, it prints the command output (stdout) of the EC2 instance.
   - If the command execution fails, it prints an error message with the command execution status.

## Permission defined In the Policy Used

      {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeAssociation",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ssm:GetDocument",
                "ssm:DescribeDocument",
                "ssm:GetManifest",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:ListAssociations",
                "ssm:ListInstanceAssociations",
                "ssm:PutInventory",
                "ssm:PutComplianceItems",
                "ssm:PutConfigurePackageResult",
                "ssm:UpdateAssociationStatus",
                "ssm:UpdateInstanceAssociationStatus",
                "ssm:UpdateInstanceInformation",
                "ssm:SendCommand",
                "ssm:ListCommands",
                "ssm:GetCommandInvocation"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply"
            ],
            "Resource": "*"
        }
    ]
      }


### Code Explanation

This is the entry point of the AWS Lambda function. The lambda_handler function is triggered when the Lambda function is invoked. It takes in the event and context parameters, but they are not used in this script.

      def lambda_handler(event, context):

These lines specify the EC2 instance ID (ec2_instance_id) of the target instance on which the command will be executed. The command variable holds the command that will be run on the EC2 instance.

      ec2_instance_id = 'i-01dd11a73247326***'
      command = 'systemctl list-units --type=service'

This line creates an SSM client using the boto3.client function. It uses the default credentials available to the Lambda function or the credentials configured on your local machine.

      ssm_client = boto3.client('ssm')

This section sends the command to the specified EC2 instance using SSM Run Command. The send_command method is used to execute the command. It takes the following parameters:

    InstanceIds: A list of EC2 instance IDs on which the command will be executed.
    DocumentName: The name of the SSM document to use. In this case, 'AWS-RunShellScript' is used to run shell commands on the EC2 instance.
    Parameters: A dictionary containing the command to be executed. The command is provided as a list of commands within the 'commands' key.

The response from the send_command method is stored in the response variable.

    try:
        # Execute command on EC2 instance using SSM Run Command
        response = ssm_client.send_command(
            InstanceIds=[ec2_instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [command]},
        )

These lines retrieve the command ID from the response and create a waiter object using the get_waiter method. The wait method is called on the waiter object to wait for the command execution to complete. It takes the CommandId and InstanceId parameters.

        command_id = response['Command']['CommandId']
        waiter = ssm_client.get_waiter('command_executed')
        waiter.wait(CommandId=command_id, InstanceId=ec2_instance_id)

This section retrieves the command invocation details using the get_command_invocation method. It takes the CommandId and InstanceId parameters. The command status is checked, and if it is 'Success', the command output (stored in StandardOutputContent) is printed. If the command execution fails, an error message with the command execution status is printed

        command_invocation = ssm_client.get_command_invocation(CommandId=command_id, InstanceId=ec2_instance_id)

        if command_invocation['Status'] == 'Success':
            # Get the command output
            command_output = command_invocation['StandardOutputContent']
            print(command_output)
        else:
            # Command execution failed
            print(f"Command execution failed. Status: {command_invocation['Status']}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

