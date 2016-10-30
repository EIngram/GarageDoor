# This code should be deployed on AWS Lambda
# Has no effect on the Raspberry Pi
# Create a skill to utilize this code in developer mode for free
# Requires APP id on row 11
# Requires IP Address on row 10

from __future__ import print_function
import requests, json
result = ""
ip_address = "XXX"  # address of the raspberry pi & flask port
skill_id = "XXX"  # from developer.amazon.com

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "GarageDoor - " + title,
            'content': "GarageDoor - " + output
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():


    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Garage Door Monitor. " \
                    "use this to see if your door is open or closed."\
                    "Ask Garage, Is the door Open?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Garage Door. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_status():
    global result
    try:
        data = requests.get(ip_address)  # Your public IP here, set above
        status = json.loads(data.text)
        result = status['Door'][0]['Status']
        return result
    except requests.exceptions.ConnectionError as e:
        result = "Hmm... The Garage seems to have a connection error "\
                "please try again"
        return result


def make_response(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    speech_output = ""\
                    "Eric figures shit out! " + result

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, should_end_session))

# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "DoorStatus":
        get_status()
        return make_response(intent, session)  # Edited here to return results
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

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != skill_id):  # Edit this Line with your Skill ID or Remove
        raise ValueError("Invalid Application ID")
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
