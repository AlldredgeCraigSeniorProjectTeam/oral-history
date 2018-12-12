from __future__ import print_function
from random import randint as rand

import os, requests, logging, datetime

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from familySearchAPIDecorator import FSDecorator
from customExceptions import httpError401Exception, httpError403Exception, httpErrorUnhandledException

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import LinkAccountCard
from ask_sdk_model import Response, dialog

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """ Handler for the skill launch. Called when the user launches the skill without specifying what they want """

    # Grab the session 
    session = handler_input.request_envelope.session

    try:
        # Try getting the access token, as a test of whether the user has linked the account
        access_token = handler_input.request_envelope.session.user.access_token
    
        speech_text = "Welcome to Family History! Try saying 'tell me a story'"

        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Family History", speech_text)).set_should_end_session(
            False).response
        
    except KeyError, e:
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."

        return handler_input.response_builder.speak().set_card(
            SimpleCard("Family History", speech_text)).response

@sb.request_handler(can_handle_func=is_intent_name("record_history"))
def record_history_intent_handler(handler_input):
    """ Grab raw user text from AMAZON.custom_slot and write it to generic file.
       Then push story to FS as a memory. """

    # Grab the access token
    access_token = handler_input.request_envelope.session.user.access_token
    
    # Grab the intent
    intent = handler_input.request_envelope.request.intent

    # Grab the slots
    story = intent.slots['story'].value

    FS = FSDecorator(access_token).getInstance()

    try:
        speech_text = FS.postMemory(story)
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except TypeError, e:
        # This is where we authenticate because a brand new user has no access token whatsoever, so he got a type error.
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    # Once again, we are intentionally not catching httpErrorUnhandledException

    # If there are no exceptions, read the response back to the user.
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("read_history"))
def read_history_intent_handler(handler_input):
    """ Read a story from FamilySearch """

    # Grab the session attributes
    # session_attributes = handler_input.attributes_manager.session_attributes

    # Grab the access token
    access_token = handler_input.request_envelope.session.user.access_token
    
    FS = FSDecorator(access_token).getInstance()

    try:
        speech_text = FS.getMemory()
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).set_card(
            LinkAccountCard()).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).set_card(
            LinkAccountCard()).response
    except TypeError, e:
        # This is where we authenticate because a brand new user has no access token whatsoever, so he got a type error.
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).set_card(
            LinkAccountCard()).response
    # We are intentionally not catching httpErrorUnhandledException

    # If there are no exceptions, read the story to the user.
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(False).response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("interview_me") and
        handler_input.request_envelope.request.dialog_state.value == "STARTED")
def before_starting_interview_me_intent_handler(handler_input):

   # Grab the access token
    access_token = handler_input.request_envelope.session.user.access_token
    
    FS = FSDecorator(access_token).getInstance()

    try:
        speech_text = FS.getMemory()
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except TypeError, e:
        # This is where we authenticate because a brand new user has no access token whatsoever, so he got a type error.
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    # We are intentionally not catching httpErrorUnhandledException

    my_delegate_directive = dialog.delegate_directive.DelegateDirective()
    return handler_input.response_builder.add_directive(my_delegate_directive).set_should_end_session(False).response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("interview_me") and
        handler_input.request_envelope.request.dialog_state.value == "IN_PROGRESS")
def in_progress_interview_me_intent_handler(handler_input):
    current_intent = handler_input.request_envelope.request.intent.name
    my_delegate_directive = dialog.delegate_directive.DelegateDirective()

    return handler_input.response_builder.add_directive(my_delegate_directive).set_should_end_session(False).response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("interview_me") and
        handler_input.request_envelope.request.dialog_state.value == "COMPLETED")
def completed_interview_me_intent_handler(handler_input):
    speech_text = "Thanks for the interview!"

    # Grab the access token
    access_token = handler_input.request_envelope.session.user.access_token
    
    interview_text = "Interview with Family History Skill, " + datetime.datetime.now().strftime("%A, %x") + ":\n"

    slot_questions = {'grandmas_house_color': 'What color was your grandmother\'s house?',
        'grandmas_favorite_game': 'What was your grandmother\'s favorite game?', 
        'grandmas_favorite_dessert': 'What was your grandma\'s favorite dessert?'}

    for slot in handler_input.request_envelope.request.intent.slots:
        interview_text += "Family History: " 
        interview_text += slot_questions[slot] + "\n"
        interview_text += "User: "
        interview_text += str(handler_input.request_envelope.request.intent.slots[slot].value + "\n\n")

    FS = FSDecorator(access_token).getInstance()

    try:
        speech_text = FS.postMemory(interview_text)
    except httpError401Exception, e:
        # This is where we reauthenticate because we got a 401 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except httpError403Exception, e:
        # This is where we reauthenticate because we got a 403 response.
        speech_text = "Your session has expired.  Please proceed to the Alexa app to sign in again using the Link Account button."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    except TypeError, e:
        # This is where we authenticate because a brand new user has no access token whatsoever, so he got a type error.
        speech_text = "Welcome to Family History! To get the most out of this Skill, please link your account."
        return handler_input.response_builder.speak(speech_text).set_card(
            LinkAccountCard()).set_should_end_session(False).response
    # Once again, we are intentionally not catching httpErrorUnhandledException

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    speech_text = "Welcome to Family History! Try saying 'tell me a story'"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(False).response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""

    speech_text = "Goodbye!  Come back soon!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Family History", speech_text)).set_should_end_session(True).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """ The fallback handler """
    speech = ("Try saying 'tell me a story'.")
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

    speech = "There was a problem. Goodbye!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.set_should_end_session(True).response

handler = sb.lambda_handler()
