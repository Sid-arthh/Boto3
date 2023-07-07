import boto3


def lambda_handler(event, context):
    check_s3_lifecycle_policies()
    
def check_s3_lifecycle_policies():
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get the list of all S3 buckets
    response = s3_client.list_buckets()

    # Iterate through each bucket
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        # Get the lifecycle configuration for the bucket
        try:
            response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            lifecycle_configuration = response['Rules']

            # Check if the bucket has any lifecycle policies
            if lifecycle_configuration:
                print(f"Bucket: {bucket_name} has lifecycle policies.")
            else:
                print(f"Bucket: {bucket_name} does not have any lifecycle policies.")
        except s3_client.exceptions.NoSuchLifecycleConfiguration:
            print(f"Bucket: {bucket_name} does not have any lifecycle policies.")
