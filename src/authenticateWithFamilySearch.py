# This is source for the lambda that will be invoked when the skill needs to 
# authenticate with FamilySearch.

import json

def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
    