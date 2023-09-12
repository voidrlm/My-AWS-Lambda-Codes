import json

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return {'body': 'GET METHOD'}
    elif event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        return {'body': 'This is a POST request with body: {}'.format(body)}
    else:
        return {'body': 'Unsupported'}
