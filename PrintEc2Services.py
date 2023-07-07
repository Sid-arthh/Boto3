import boto3

def lambda_handler(event, context):
    # EC2 instance details
    ec2_instance_id = 'i-01dd11a73247326***'
    command = 'systemctl list-units --type=service'

    # SSM client
    ssm_client = boto3.client('ssm')

    try:
        # Execute command on EC2 instance using SSM Run Command
        response = ssm_client.send_command(
            InstanceIds=[ec2_instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [command]},
        )

        command_id = response['Command']['CommandId']

        # Wait for the command to complete
        waiter = ssm_client.get_waiter('command_executed')
        waiter.wait(CommandId=command_id, InstanceId=ec2_instance_id)

        # Get the command invocation details
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
