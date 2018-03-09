import json
import boto3
import re
import os

dynamo_db = boto3.client('dynamodb')
cognito = boto3.client('cognito-idp')
sns = boto3.client('sns')

table_name = 'user_token'


# Get User from security context.
# May return null if user not found
def get_user(cognitoAuthenticationProvider):

    # cognito-idp.eu-west-2.amazonaws.com/eu-west-2_9Rfg3SRNy,cognito-idp.eu-west-2.amazonaws.com/eu-west-2_9Rfg3SRNy:CognitoSignIn:4b586b11-0e4d-4690-b30f-0b50ce31beda
    m = re.search(".*/(.+):CognitoSignIn:(.+)", cognitoAuthenticationProvider)
    if m is not None:
        userPoolId = m.group(1)
        sub = m.group(2)
    else:
        # Rethrow the exception, the input is actually bad.
        raise "Unable to extract user from security Provider"

    print("userPoolId" + userPoolId)

    cognito_filter = "sub='" + sub + "'"

    print("filter  " + cognito_filter)

    response = cognito.list_users(
        UserPoolId=userPoolId,
        AttributesToGet=["phone_number"],
        Limit=1,
        Filter=cognito_filter
    )
    if len(response["Users"]) > 0:
        user = response["Users"][0]
        # This is the default phone_number
        phone_number = None
        for attribute in user["Attributes"]:
            if attribute["Name"] == "phone_number":
                phone_number = attribute["Value"]
        if phone_number is None:
            return None, None
        return user["Username"], phone_number
    else:
        return None, None