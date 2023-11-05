import boto3
import json
def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    table_name = 'users'
    query_value = 'ab'

    try:
        response = dynamodb.scan(TableName=table_name)
        items = response['Items']
        filtered_items = []

        for item in items:
            # Check each attribute for the query value
            for attribute_name, attribute_value in item.items():
                if 'S' in attribute_value and query_value in attribute_value['S']:
                    filtered_items.append(item)
                    break  
        return {
            'statusCode': 200,
            'body': json.dumps(filtered_items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
