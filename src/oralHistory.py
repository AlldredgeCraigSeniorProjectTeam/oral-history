from __future__ import print_function
from random import randint as rand

import os
import requests

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.response_helper import get_plain_text_content

from familySearchAPIDecorator import FSDecorator

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

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = 'Goodbye!'
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


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

    file = open('/tmp/filename.txt', 'w')
    file.write("Hello, World! You have uploaded to s3!")
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
    speech_output = "Thanks for invoking Read History"
    should_end_session = False

    id = "751321"
    x = FSDecorator(session).getInstance()
    response = x.getMemory(id)
    if response.status_code == 401:
        # You need to reauthenticate
        speech_output = "The session has expired.  Please reauthenticate."
    if response.status_code == 200:
        speech_output = response.text
    else:
        # Unhandled status code
        speech_output = "Your request to FamilySearch returned with an error code of" + str(response.status_code)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def random_history(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = "Random History"

    speech_output = "<prosody rate='slow'>The captain called a meeting in the saloon.  He told us that " + \
    "we were off Frenchman's Bay and that we would remain at anchor there until " + \
    "the next morning when he would try to enter Cockburn Town Harbor. He said " + \
    "this might be difficult, as there was a long reef about 1000 feet off the " + \
    "mouth of the harbor, running parallel with the shore.  Then he said, \"Tonight " + \
    "we will 'ave a masquerade, with prizes for the best costumes.\"</prosody>"

    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
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
    elif intent_name == "random_history":
        return random_history(intent, session)
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
