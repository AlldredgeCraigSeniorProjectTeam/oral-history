# This is the source for the lambda that will be invoked when the user requests
# a story to be told.

import json

def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
