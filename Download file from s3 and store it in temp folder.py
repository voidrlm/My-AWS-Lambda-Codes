import json
import os
import boto3


def lambda_handler(event, context):
    try:
        bucket_name = ''  # bucket name here
        s3_object_key = ''  # s3 object key here
        s3 = boto3.client('s3')
        temp_dir = '/tmp'
        file_path = os.path.join(temp_dir, os.path.basename(s3_object_key))
        s3.download_file(bucket_name, s3_object_key, file_path)
        response = {
            'statusCode': 200,
            'body': json.dumps("Downloaded")
        }
    except Exception as e:
        response = {
            'statusCode': 500,  # Indicates a server error
            'body': json.dumps('Error: ' + str(e))
        }

    return response
