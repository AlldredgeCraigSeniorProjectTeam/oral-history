from __future__ import print_function
from random import randint as rand

import os, requests, logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from familySearchAPIDecorator import FSDecorator
from customExceptions import httpError401Exception, httpError403Exception, httpErrorUnhandledException

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import LinkAccountCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_intent_name("record_history"))
def record_history_intent_handler(handler_input):
    """ Grab raw user text from AMAZON.custom_slot and write it to generic file
       connect to s3 bucket using env variables in lambda and push it to
       AWS using a unique name to prevent overwrite.
       Additionally attempts to push story to FS as a memory. """

    # Grab the session
    session = handler_input.request_envelope.session

    # Grab the intent
    intent = handler_input.request_envelope.request.intent

    # Grab the slots
    story = intent['slots']['story']['value']

    FS = FSDecorator(session).getInstance()

    try:
        speech_text = FS.postMemory(story)
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(
            True).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(
            True).response
    # Once again, we are intentionally not catching httpErrorUnhandledException

    # If there are no exceptions, read the response back to the user.
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("read_history"))
def read_history_intent_handler(handler_input):
    """ Read a story from FamilySearch """
    session = handler_input.request_envelope.session

    FS = FSDecorator(session).getInstance()

    try:
        speech_text = FS.getMemory()
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(
            True).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(
            True).response
    # We are intentionally not catching httpErrorUnhandledException

    # If there are no exceptions, read the story to the user.
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """ Handler for the skill launch. Called when the user launches the skill without specifying what they want """

    # Grab the session
    session = handler_input.request_envelope.session

    # Grab the request ID 
    requestId = handler_input.request_envelope.request.requestId

    print("on_launch requestId=" + requestId + ", sessionId=" + session['sessionId'])

    try:
        # Try getting the access token, as a test of whether the user has linked the account
        access_token = session['user']['accessToken']
        
        speech_text = "Welcome to Family History! Try saying 'tell me a story'"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Family History", speech_text)).set_should_end_session(
            False).response
        
    except KeyError, e:
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."

        return handler_input.response_builder.speak().set_card(
            SimpleCard("Family History", speech_text)).set_should_end_session(
            True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    speech_text = "Welcome to Family History! Try saying 'tell me a story'"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""

    speech_text = "Goodbye!  Come back soon!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """ The fallback handler """
    speech = (
        "Try saying 'tell me a story'.")
    reprompt = "I'm sorry, please try to speak more clearly!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    logger.error(exception, exc_info=True)

    speech = "There was a problem. Please try again!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response

handler = sb.lambda_handler()
