from __future__ import print_function
from random import randint as rand

import os
import requests

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.response_helper import get_plain_text_content

from familySearchAPIDecorator import FSDecorator
from customExceptions import httpError401Exception, httpErrorUnhandledException

import boto3
from botocore.client import Config

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            #'text': output
            'ssml': '<speak>'+output+'</speak>'
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_link_account_response():
    return {
        "outputSpeech": {"type":"PlainText","text":"Welcome to Family History! To get the most out of this Skill, please link your account."},
        "card": {
            "type": "LinkAccount"
        }
    }

def build_reauthenticate_response():
    return {
        "outputSpeech": {"type":"PlainText","text":"Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."},
        "card": {
            "type": "LinkAccount"
        }
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Helper that handles logging ------------------
def log(event):
    print('Logged event: {}'.format(event))

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Family History! Try saying 'tell me a story'"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_link_account_response():
    session_attributes = {}
    return build_response(session_attributes, build_link_account_response())

def get_reauthenticate_response():
    session_attributes = {}
    return build_response(session_attributes, build_reauthenticate_response())

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = 'Goodbye!'
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    try:
        access_token = session['user']['accessToken']
        return get_welcome_response()
    except KeyError, e:
        return get_link_account_response()

def gen_file_name():
    '''Use to create unique entry?'''
    return 'filename'

def record_history(intent, session):

    # grab the slots
    # slots = event['request']['intent']['slots']
    story = intent['slots']['story']['value']

    file = open('/tmp/filename.txt', 'w')
    # file.write("Hello, World! You have uploaded to s3!")
    file.write(story)
    file.close()

    file = open('/tmp/filename.txt', 'r')
    s3 = boto3.resource(
    's3'
    , aws_access_key_id=os.environ['ACCESS_KEY']
    , aws_secret_access_key=os.environ['SECRET_ACCESS_KEY']
    , config=Config(signature_version='s3v4'))
    s3.Bucket(os.environ['BUCKET_NAME']).put_object(Key='speechTest/testfile.txt', Body=file)
    file.close()

    session_attributes = {}
    reprompt_text = None
    card_title = "Record History"

    speech_output = "Thanks for invoking Record History"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def read_history(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = "Read History"
    should_end_session = False

    id = "751321"
    FS = FSDecorator(session).getInstance()

    try:
        speech_output = FS.getMemory(id)
    except httpError401Exception, e:
        # This is where you reauthenticate.
        return get_reauthenticate_response()

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "record_history":
        return record_history(intent, session)
    elif intent_name == "read_history":
        return read_history(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    # This call is strictly for logging purposes
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
