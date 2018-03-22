import boto3
import json
import user_push

cognito = boto3.client('cognito-idp')

def create_group(event,context):

    print json.dumps(event,  encoding='ascii')
    user_name= event["userName"]
    type=event["request"]["userAttributes"]["custom:type"]

    if type == "company":
     cognito.create_group(
     GroupName=user_name,
     UserPoolId='eu-west-1_w2rC3VeKI',
     Description="Company group"
     )
    else:
      print("type is not company")

    return event


def check_if_company(event,context):

    print json.dumps(event, encoding='ascii')
    type=event['requestContext']['authorizer']['claims']['custom:type']

    response = {
        "statusCode": 201,
        "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
        "body": json.dumps(type)
    }
    return response

def assign_user(event,context):

    print json.dumps(event,  encoding='ascii')

    body= json.loads(event['body'])
    email=body['email']
    group_name=body['group_name']

    addUser = cognito.admin_add_user_to_group(
        UserPoolId='eu-west-1_w2rC3VeKI',
        Username=email,
        GroupName=group_name
    )

    response = {
        "statusCode": 201,
        "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
        "body": json.dumps({})
    }
    return response

def delete_user(event,context):
    print json.dumps(event,  encoding='ascii')

    body= json.loads(event['body'])
    email=body['email']
    group_name=body['group_name']

    cognito.admin_remove_user_from_group(
        UserPoolId='eu-west-1_w2rC3VeKI',
        Username=email,
        GroupName=group_name
    )

    response = {
        "statusCode": 201,
        "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
        "body": json.dumps({})
    }
    return response

def get_all_users_in_group_cognito(event,context):

    print json.dumps(event,  encoding='ascii')

    group_name=event['requestContext']['authorizer']['claims']['name']

    response = cognito.list_users_in_group(
        UserPoolId='eu-west-1_w2rC3VeKI',
        GroupName=group_name
    )

    list_of_user=[]

    if len(response["Users"]) > 0:
        users=response['Users']
        for user in users:
            username=user['Username']
            phone=user['Attributes'][4]['Value']
            email=user['Attributes'][7]['Value']
            _user=username+","+phone+","+email
            list_of_user.append(_user)

        data = dict()

        data['users_list'] = list_of_user

        if len(data) > 0:
            response = {
                "statusCode": 201,
                "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
                "body":json.dumps(data)
            }
        else:
            response = {
                "statusCode":400,
                "headers" : { "Access-Control-Allow-Origin" : "*" },  # Required for CORS support to work
                "body":"no users found in this group"
            }
        return response