import json
import os
import boto3


def lambda_handler(event, context):
    try:
        bucket_name = ''  # s3 bucket name
        objectKey = ''  # file in s3 name
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=objectKey)
        file = response['Body'].read()
        # use the file for further processing
        response = {
            'statusCode': 200,
            'body': json.dumps("OK")
        }
    except Exception as e:
        response = {
            'statusCode': 500,  # Indicates a server error
            'body': json.dumps('Error: ' + str(e))
        }

    return response
