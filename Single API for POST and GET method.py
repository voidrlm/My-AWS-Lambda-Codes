import json

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return {'body': 'GET METHOD'}
    elif event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        return {'body': 'This is a POST request with body: {}'.format(body)}
    else:
        return {'body': 'Unsupported'}


#notes
# Used for identification of post and get methods
# use request parameter if an post method is invoked
# eg:
# {
#     "ID": "123"
# }