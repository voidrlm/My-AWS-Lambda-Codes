import boto3
import json

def lambda_handler(event, context):
    table_name = 'tableName'
    dynamodb = boto3.client('dynamodb')



    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'uploaderId': {'S': str(event.get('id'))}
            }
        )
        item = response.get('Item', {})

        return {
            'statusCode': 200,
            'body': json.dumps({"query":str(event.get('id')),"result":item})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
