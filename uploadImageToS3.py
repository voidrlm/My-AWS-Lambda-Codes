import boto3
import json
import base64
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucketName = 'voidawsbucket' #define bucket nam3e

    try:
        request_body = json.loads(event['body']) #request body
        base64_data = request_body.get('image', '') #image from request
        filename = request_body.get('filename') #filename from request

        if not base64_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'base64_missing'})
            }

        formattedBase64 = base64_data.split(',')[1]
        imageData = base64.b64decode(formattedBase64)
        filePath = 'uploaded-images/' + filename
        s3_client.put_object(Bucket=bucketName, Key=filePath, Body=imageData)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': e})
        }