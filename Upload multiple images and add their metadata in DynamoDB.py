import boto3
import json
import base64
import time
import uuid

s3_client = boto3.client('s3')

def lambda_handler(event, context):

    bucketName = 'voidawsbucket' #define bucket nam3e

    try:
        request_body = json.loads(event['body']) #request body
        #Validation for request
        required_fields = ['images', 'uploaderId']
        missing_fields = [field for field in required_fields if field not in request_body]   
        if missing_fields:
            return {
                'statusCode': 400,
                'body':json.dumps({'message': f'The following fields are missing: {", ".join(missing_fields)}'})
            }
        uploaderId = request_body.get('uploaderId', '') #uploaderId from request
        imagesFromRequest = request_body.get('images', []) 
        for imageData in imagesFromRequest:
            base64_data = imageData.get('image', '') #image from request
            formattedBase64 = base64_data.split(',')[1]
            current_timestamp = int(time.time())
            extension = base64_data.split(',')[0].split('/')[-1].split(';')[0]
            base64Image = base64.b64decode(formattedBase64)
            fileName = str(uuid.uuid4())
            filePath = "uploadedImages/"+fileName+"."+extension
            s3_client.put_object(Bucket=bucketName, Key=filePath, Body=base64Image)
            dynamodb = boto3.resource('dynamodb')
            dataToDynamoDB = {
            'fileName': fileName,
            'filePath': filePath,
            'uploadedOn': current_timestamp,
            'uploaderId': uploaderId
            }
            dynamo_table = dynamodb.Table('uploaded-images')
            dynamo_table.put_item(Item=dataToDynamoDB)
        return {
            'statusCode': 200,
            'body': json.dumps({"message": 'success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': e})
        }
    


#Request
#     {
#     "uploaderId": "cp01",
#     "images": [
#         {
#             "image": "data:image/png;base64,iVBOR..."
#         },
#         {
#             "image": "data:image/png;base64,iVBOR..."
#         }
#     ]
# }