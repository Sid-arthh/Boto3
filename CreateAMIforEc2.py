import boto3

def lambda_handler(event, context):
    # Specify the tag key and value to filter the EC2 instance
    tag_key = 'tag'
    tag_value = 'AMI'
    print(tag_key)
    # Create a session using your AWS credentials
    session = boto3.Session(
        aws_access_key_id='AKIAW7EMKJZ*******',
        aws_secret_access_key='FwI1X2iKOQd+uBU0r1w2nYiYWLO********',
        region_name='us-east-1'
    )

    # Create an EC2 client using the session
    ec2_client = session.client('ec2')

    # Get the EC2 instances based on the specified tag
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:' + tag_key,
            'Values': [tag_value]
        }
    ])

    # Extract the instance ID
    instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

    # Create an AMI of the instance
    response = ec2_client.create_image(
        InstanceId=instance_id,
        Name='AMI backup ' + instance_id,
        Description='Automated AMI backup of ' + instance_id,
        NoReboot=True
    )

    # Print the newly created AMI ID
    ami_id = response['ImageId']
    print('AMI created with ID:', ami_id)
