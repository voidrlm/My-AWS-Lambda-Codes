import boto3
import json

def lambda_handler(event, context):
    table_name = 'table-name' #table name here
    non_primary_key_column = 'id' # non primary key column here
    dynamodb = boto3.client('dynamodb')
    request_body = json.loads(event['body'])
    try:
        # uploader = str(event['uploaderId'])
        response = dynamodb.query(
            TableName=table_name,
            IndexName='id-index',  # replace with secoondary index name
            KeyConditionExpression=f'{non_primary_key_column} = :value',
            ExpressionAttributeValues={
                ':value': {'S': request_body['id']}
            }
        )
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
