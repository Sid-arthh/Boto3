# Boto3
## Handling Few real world use case of AWS using boto3

### CheckS3LifeCycleEnable
#### Python Script which checks if Any S3 bucket has LIFE CYCLE POLICY enabled
## Prerequisites

- AWS account with appropriate permissions to access S3 and retrieve bucket lifecycle configurations.
- Python 3.x installed on your local machine or Lambda environment.
- Boto3 library installed (`pip install boto3`).

## Usage

1. Clone the repository or download the Python script file.

2. Ensure that you have an IAM role with the necessary permissions:
   - Create an IAM role with the required permissions to access S3 and retrieve bucket lifecycle configurations. You can define these permissions using an IAM policy.
   - Attach the IAM role to the AWS Lambda function. This ensures that the Lambda function has the necessary permissions to access S3.

3. Update the AWS credentials and region in the script:
   - If running locally, configure your AWS credentials using the AWS CLI or provide credentials via environment variables.
   - If using AWS Lambda, ensure that the Lambda execution role has the necessary permissions to access S3 and retrieve bucket lifecycle configurations.

4. Execute the script:
   - If running locally, execute the script using Python: `python script_name.py`.
   - If using AWS Lambda, create a Lambda function and upload the script code as a ZIP package. Configure the function to trigger based on your requirements.

5. Check the output:
   - The script will iterate through each S3 bucket and display a message indicating if the bucket has lifecycle policies enabled or not.

## Code Explanation

The script consists of the following main components:
