# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
import urllib3
import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
HT=0
smtpObj=smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.login('chatbot.sacet@gmail.com','m@keskilled')

ml_api='https://makeskilled.com/projects/chatbot/pull.php?roll_no='

a_time_table=[
                {'Mon':'DS,MS,ML,CPP,Project'},
                {'Tue':'ML,DS,MS,CPP,Project'},
                {'Wed':'DS,ML,DS,CPP,Project'},
                {'Thu':'MS,LIB,ML,CPP,Project'},
                {'Fri':'DS,ML,MS,CPP,Project'},
                {'Sat':'Project Project'}]

b_time_table=[
                {'Mon':'ML,CPP,MS,DS,Project'},
                {'Tue':'MS,CPP,ML,DS,Project'},
                {'Wed':'MS,CPP,DS,ML,Project'},
                {'Thu':'ML,CPP,LIB,DS,Project'},
                {'Fri':'MS,CPP,ML,DS,Project'},
                {'Sat':'Project Project'}]

c_time_table=[
                {'Mon':'Project,CPP,ML,MS,DS'},
                {'Tue':'Project,CPP,ML,MS,ML'},
                {'Wed':'Project,CPP,DS,MS,DS'},
                {'Thu':'Project,CPP,ML,DS,MS'},
                {'Fri':'Project,CPP,ML,DS,LIB'},
                {'Sat':'Project Project'}]

councellor_a='Seshasai sir'
councellor_b='Nagesh Babu sir'
councellor_c='Naga Srinivas sir'

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, please say your Roll Number to proceed"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HallTicketIntentHandler(AbstractRequestHandler):
    """Handler for Hall Ticket Intent"""
    
    def can_handle(self,handler_input):
        return ask_utils.is_intent_name('HallTicketIntent')(handler_input)
        
    def handle(self,handler_input):
        global HT
        slots = handler_input.request_envelope.request.intent.slots
        ht=slots['hallticket'].value
        HT=ht
        http=urllib3.PoolManager()
        r=http.request('GET',ml_api+HT)
        r=(r.data.decode('utf-8'))
        r=json.loads(r)
        try:
            k=r[0]['name']
            speak_output='Hey '+k +' you can check your academic and attendance percentage, and also you could check your time table'
        except:
            speak_output='Hey your data is not available'
        return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)

class AttendanceIntentHandler(AbstractRequestHandler):
    """ Handler for Attendance"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('AttendanceIntent')(handler_input)
    
    def handle(self, handler_input):
        http=urllib3.PoolManager()
        r=http.request('GET',ml_api+HT)
        r=(r.data.decode('utf-8'))
        r=json.loads(r)
        try:
            k=r[0]['attendance']
            e=r[0]['email_id']
            speak_output='Your Attendance so far: '+k+" %"
            msg = MIMEMultipart()
            msg['From'] = 'chatbot.sacet@gmail.com'
            msg['To'] = e
            msg['Subject']= 'Your Attendance from Chatbot'
            msg.attach(MIMEText(speak_output, 'plain'))
            text = msg.as_string()
            smtpObj.sendmail('chatbot.sacet@gmail.com',e,text)
        except:
            speak_output='Your Attendance is not available'
        return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)

class AcademicIntentHandler(AbstractRequestHandler):
    """ Handler for Attendance"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('AcademicIntent')(handler_input)
    
    def handle(self, handler_input):
        http=urllib3.PoolManager()
        r=http.request('GET',ml_api+HT)
        r=(r.data.decode('utf-8'))
        r=json.loads(r)
        try:
            k1=r[0]['btech_cgpa']
            k2=r[0]['btech_percentage']
            e=r[0]['email_id']
            speak_output='Your BTECH CGPA so far: '+k1+" and Your BTECH Percentage so far: "+k2
            msg = MIMEMultipart()
            msg['From'] = 'chatbot.sacet@gmail.com'
            msg['To'] = e
            msg['Subject']= 'Your Academic Details from Chatbot'
            msg.attach(MIMEText(speak_output, 'plain'))
            text = msg.as_string()
            smtpObj.sendmail('chatbot.sacet@gmail.com',e,text)
        except:
            speak_output='Your BTECH CGPA is not Available'
        return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)

class TimeTableIntentHandler(AbstractRequestHandler):
    """ Handler for Attendance"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('TimeTableIntent')(handler_input)
    
    def handle(self, handler_input):
        http=urllib3.PoolManager()
        r=http.request('GET',ml_api+HT)
        r=(r.data.decode('utf-8'))
        r=json.loads(r)
        try:
            k1=r[0]['section']
            e=r[0]['email_id']
            if(k1=='a'):
                time_table=a_time_table
            elif(k1=='b'):
                time_table=b_time_table
            elif(k1=='c'):
                time_table=c_time_table
            speak_output='Your Time Table: '+str(time_table)
            msg = MIMEMultipart()
            msg['From'] = 'chatbot.sacet@gmail.com'
            msg['To'] = e
            msg['Subject']= 'Your Academic Details from Chatbot'
            msg.attach(MIMEText(speak_output, 'plain'))
            text = msg.as_string()
            smtpObj.sendmail('chatbot.sacet@gmail.com',e,text)
        except:
            speak_output='Your Time Table: Not Available'
        return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)

class CouncellorIntentHandler(AbstractRequestHandler):
    """ Handler for Attendance"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('CouncellorIntent')(handler_input)
    
    def handle(self, handler_input):
        http=urllib3.PoolManager()
        r=http.request('GET',ml_api+HT)
        r=(r.data.decode('utf-8'))
        r=json.loads(r)
        try:
            k1=r[0]['section']
            e=r[0]['email_id']
            if(k1=='a'):
                councellor_name=councellor_a
            elif(k1=='b'):
                councellor_name=councellor_b
            elif(k1=='c'):
                councellor_name=councellor_c
            speak_output='Your Councellor: '+str(councellor_name)
            msg = MIMEMultipart()
            msg['From'] = 'chatbot.sacet@gmail.com'
            msg['To'] = e
            msg['Subject']= 'Your Councellor Details from Chatbot'
            msg.attach(MIMEText(speak_output, 'plain'))
            text = msg.as_string()
            smtpObj.sendmail('chatbot.sacet@gmail.com',e,text)
        except:
            speak_output='Your Councellor: Not Available'
        return (handler_input.response_builder.speak(speak_output).set_should_end_session(False).response)

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HallTicketIntentHandler())
sb.add_request_handler(AttendanceIntentHandler())
sb.add_request_handler(AcademicIntentHandler())
sb.add_request_handler(TimeTableIntentHandler())
sb.add_request_handler(CouncellorIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()