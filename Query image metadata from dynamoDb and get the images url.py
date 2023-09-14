import boto3
import json

def lambda_handler(event, context):
    try:
        # Define your table name and non-primary key column here
        table_name = 'uploaded-images'
        non_primary_key_column = 'uploaderId'

        # Initialize DynamoDB client
        dynamodb = boto3.client('dynamodb')

        # Parse the request body as JSON
        request_body = json.loads(event['body'])

        # Specify your S3 bucket name
        bucket_name = 'voidawsbucket'
        
        # Initialize S3 client
        s3 = boto3.client('s3')

        # Query DynamoDB using the specified non-primary key column
        response = dynamodb.query(
            TableName=table_name,
            IndexName='uploaderId-index',  # Replace with the secondary index name
            KeyConditionExpression=f'{non_primary_key_column} = :value',
            ExpressionAttributeValues={
                ':value': {'S': request_body['uploaderId']}
            }
        )

        # Get the items from the DynamoDB response
        items = response.get('Items', [])
        output = []

        # Iterate through DynamoDB items
        for imageData in items:
            path = imageData['filePath']['S']
            
            # Generate a pre-signed URL for the S3 object
            fileData = {
                "imageUrl": s3.generate_presigned_url(
                    'get_object', Params={'Bucket': bucket_name, 'Key': path}, ExpiresIn=86400),
                "filePath": imageData['filePath']['S'],
                "fileName": imageData['fileName']['S'],
                "uploadedOn": imageData['uploadedOn']['N']
                
                
            }
            output.append(fileData)

        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }


# Request
# {uploaderId:"123"}