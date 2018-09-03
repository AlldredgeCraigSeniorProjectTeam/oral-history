# This is the source for the lambda that will prompt the user for a story and 
# which will transcribe their answer.

import json

def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
