# Boto3
## Handling Few real world use case of AWS using boto3

# CheckS3LifeCycleEnable
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
   - If running locally, execute the script using Python: `python script_name.py`.
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

