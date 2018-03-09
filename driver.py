import json
import boto3

_dynamo_db = boto3.resource('dynamodb', region_name='eu-west-1')
driver_code_table=_dynamo_db.Table('driver_code')

def save_registration_code(event,context):

    print json.dumps(event,  encoding='ascii')
    body= json.loads(event['body'])
    code=body['code']
    drivername=body['drivername']

    response = driver_code_table.get_item(
        Key={
            'username': drivername,
        }
    )
    print json.dumps(response,  encoding='ascii')
    print (len(response))
    if len(response)== 2:
     print('list is not empty')
     response = {
         "statusCode": 500,
         "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
         "body": "user already exist"
     }

     return  response
    else:
     print ('list is empty')
     driver_code_table.put_item(
        Item={
            'username': drivername,
            'code':code
        }
      )

     response = {
        "statusCode": 201,
        "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
        "body": json.dumps({})
     }

    return response