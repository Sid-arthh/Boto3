import boto3
import json
import logging

# Configure the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Initialize the Auto Scaling and EC2 clients
        autoscaling_client = boto3.client('autoscaling')
        ec2_client = boto3.client('ec2')
        
        # Get the Auto Scaling Group name from the CloudWatch event
        event_details = json.loads(event['Records'][0]['Sns']['Message'])
        auto_scaling_group_name = event_details['AutoScalingGroupName']
        
        # Describe the Auto Scaling Group to get launch template details
        response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[auto_scaling_group_name])
        asg_details = response['AutoScalingGroups'][0]
        
        # Get the launch template ID from the Auto Scaling Group details
        launch_template_id = asg_details['LaunchTemplate']['LaunchTemplateId']
        
        # Describe the launch template to get its details
        launch_template_response = ec2_client.describe_launch_template_versions(LaunchTemplateIds=[launch_template_id])
        launch_template_details = launch_template_response['LaunchTemplateVersions'][0]
        
        # Print the launch template details to CloudWatch Logs
        logger.info(f"Launch Template Details for Auto Scaling Group {auto_scaling_group_name}:")
        logger.info(json.dumps(launch_template_details, indent=2))
        
        return "Success"
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

