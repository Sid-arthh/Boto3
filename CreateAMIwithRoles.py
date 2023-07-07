import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Specify the tag key and value to filter the EC2 instance
    tag_key = 'your-tag-key'
    tag_value = 'your-tag-value'

    # Create an EC2 client using the credentials from the IAM role
    ec2_client = boto3.client('ec2')

    # Get the EC2 instances based on the specified tag
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:' + tag_key,
            'Values': [tag_value]
        }
    ])

    # Check if instances were found
    if 'Reservations' in response and response['Reservations']:
        # Extract the instance ID
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

        # Create an AMI of the instance with a unique name using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        ami_name = 'AMI backup ' + instance_id + ' ' + timestamp

        response = ec2_client.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            Description='Automated AMI backup of ' + instance_id,
            NoReboot=True
        )

        # Print the newly created AMI ID
        ami_id = response['ImageId']
        print('AMI created with ID:', ami_id)
    else:
        print('No instances found based on the specified tag')
