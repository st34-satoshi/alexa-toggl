# -*- coding: utf-8 -*-

# Alexa Skill Lambda function
# Use toggl

import logging
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type, get_slot_value

from ask_sdk_model import Response

from alexa import data

from toggl import TogglDriver

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import constants

token = constants.toggl_token
email_address = constants.toggl_email_address
togglDriver = TogglDriver(_token=token)


# Request Handler classes
# 具体的なリクエストなしの時
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        # logger.info(_("This is an untranslated message"))

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class MorningIntentHandler(AbstractRequestHandler):
    """Handler for morning intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("morningIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In MorningHandler")

        _ = handler_input.attributes_manager.request_attributes["_"]

        # set title and project value
        title_value = "morning"
        project_value = "Life"

        # start timer
        togglDriver.start(title_value, project_value)

        handler_input.response_builder.speak(_(data.START_TIMER).format(project_value, title_value))
        return handler_input.response_builder.response


class StartTimerIntentHandler(AbstractRequestHandler):
    """Handler for start timer intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("startTimerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartTimerIntentHandler")

        project_value = get_slot_value(handler_input=handler_input, slot_name="project")
        print(project_value)
        logger.info(project_value)
        title_value = get_slot_value(handler_input=handler_input, slot_name="title")
        print(title_value)
        _ = handler_input.attributes_manager.request_attributes["_"]
        if project_value is None:
            handler_input.response_builder.speak(_(data.NO_PROJECT))
            return handler_input.response_builder.response
        if title_value is None:
            handler_input.response_builder.speak(_(data.NO_TITLE))
            return handler_input.response_builder.response

        # start timer
        togglDriver.start(title_value, project_value)

        handler_input.response_builder.speak(_(data.START_TIMER).format(project_value, title_value))
        return handler_input.response_builder.response


class StopTimerIntentHandler(AbstractRequestHandler):
    """Handler for stop timer intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("stopTimerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StopTimerIntentHandler")

        # logger.info(project_value)
        print("stop Timer")
        _ = handler_input.attributes_manager.request_attributes["_"]
        id = togglDriver.get_running_time_entry()
        if id is not None:
            r = togglDriver.stop(id)
            if r.status_code == 200:
                handler_input.response_builder.speak(_(data.SUCCESS_STOP_TIMER))
            else:
                handler_input.response_builder.speak(_(data.FAILURE_STOP_TIMER))
        else:
            handler_input.response_builder.speak(_(data.NO_TIMER))

        return handler_input.response_builder.response


class ReviewOneDayIntentHandler(AbstractRequestHandler):
    """Handler for review One Day Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("reviewOneDayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ReviewOneDayIntentHandler")

        print("reviewOneDayIntent")

        day_value = get_slot_value(handler_input=handler_input, slot_name="day")
        print(day_value)
        logger.info(day_value)

        _ = handler_input.attributes_manager.request_attributes["_"]
        if day_value is None:
            handler_input.response_builder.speak(_(data.NO_DATE_REVIEW))
            return handler_input.response_builder.response
        # TODO it is bad code. alexa translate 9/10 to 2020/9/20. but now it is 2019!
        day_value_str = str(day_value)
        if '2020' in day_value_str:
            day_value = day_value_str.replace('2020', '2019')
        if '2021' in day_value_str:
            day_value = day_value_str.replace('2021', '2020')

        # get each project total time
        project_list = ['Life', 'University', 'Moving', 'Hobby', 'Play', 'Communication']
        project_name_list = ['生活', '大学', '移動', '趣味', '遊び', 'コミュニケーション']
        each_project_time_list = togglDriver.get_reports(email_address, project_list, str(day_value))
        if each_project_time_list is None:
            handler_input.response_builder.speak(_(data.ERROR_REVIEW))
            return handler_input.response_builder.response
        answer_str = "{}を振り返ります．".format(day_value)
        print(answer_str)
        # answer_str = "{0}を振り返ります．".format(day_value)
        for i, project in enumerate(project_list):
            hour = each_project_time_list[i] // 60
            minute = each_project_time_list[i] % 60
            answer_str += "{0}は{1}時間{2}分, ".format(project_name_list[i], str(hour), str(minute))
        answer_str += "です．"
        print(answer_str)
        # handler_input.response_builder.speak(_(data.START_TIMER).format(project_value, title_value))
        # handler_input.response_builder.speak("{}ですね．".format(day_value))
        handler_input.response_builder.speak(answer_str)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent or Yes/No without
    restaurant info intent.
     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.FallbackIntent")(handler_input) or
                ("restaurant" not in session_attr and (
                    is_intent_name("AMAZON.YesIntent")(handler_input) or
                    is_intent_name("AMAZON.NoIntent")(handler_input))
                 ))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.FALLBACK).format(data.SKILL_NAME)).ask(_(
            data.FALLBACK).format(data.SKILL_NAME))

        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartTimerIntentHandler())
sb.add_request_handler(StopTimerIntentHandler())
sb.add_request_handler(ReviewOneDayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(MorningIntentHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
