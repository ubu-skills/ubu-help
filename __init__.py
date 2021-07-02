"""Module for the ubu-help skill
"""
import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler  # type: ignore
from mycroft.audio import wait_while_speaking
from fuzzywuzzy import fuzz, process
sys.path.append("/usr/lib/UBUVoiceAssistant")  # type: ignore
from UBUVoiceAssistant.util import util  # type: ignore


class UbuHelpSkill(MycroftSkill):
    """Class for the ubu-help skill
    """

    def __init__(self) -> None:
        super().__init__()
        self.webservice = None

    def initialize(self):
        """Initializes the skill
        """
        self.webservice = util.get_data_from_server()

    @intent_handler(IntentBuilder("HelpIntent").require("Help"))
    def help(self, message):
        """Reads the help text

        Args:
            message ([type]): Mycroft message data
        """
        self.speak_dialog("help")
        wait_while_speaking()
        self.actionsList(message)

    @intent_handler(IntentBuilder("HowDoIIntent").require("Accion"))
    def howDoI(self, message):
        """Says how to invoke some skill

        Args:
            message: Mycroft message data
        """
        accion = message.data.get("Accion")
        translated = self.translate_list("actionslist")
        action_dialog = {}
        iterator = iter(translated)
        try:
            for dialog in [
                "send.messages",
                "forums",
                "calendar.events",
                "receive.messages",
                "course.changes",
                "grades"
            ]:
                action_dialog[dialog] = next(iterator)
                action_dialog[dialog+" "] = next(iterator)
        except StopIteration:
            pass
        dialog = process.extractOne(accion, action_dialog, scorer=fuzz.ratio, score_cutoff=60)
        if dialog is None:
            self.speak_dialog("action.not.found")
        else:
            self.speak_dialog(str(dialog[2]).strip())


    @intent_handler(IntentBuilder("ActionsIntent").require("WhatCanYouDo"))
    def actionsList(self, _):
        """Reads the action list

        Args:
            _: Mycroft message data
        """
        self.speak_dialog("actions")


def create_skill():
    """Creates the ubu-help skill

    Returns:
        UbuHelpSkill: The skill to show help to the user
    """
    return UbuHelpSkill()
