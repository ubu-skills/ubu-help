import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler  # type: ignore
from mycroft.audio import wait_while_speaking
from fuzzywuzzy import fuzz, process
sys.path.append("/usr/lib/UBUVoiceAssistant")  # type: ignore
from UBUVoiceAssistant.util import util  # type: ignore


class UbuHelpSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("HelpIntent").require("Help"))
    def help(self, message):
        self.speak_dialog("help")
        wait_while_speaking()
        self.actionsList(message)

    @intent_handler(IntentBuilder("HowDoIIntent").require("Accion"))
    def howDoI(self, message):
        accion = message.data.get("Accion")
        translated = self.translate_list("actionslist")
        action_dialog = {}
        it = iter(translated)
        try:
            for dialog in [
                "send.messages",
                "forums",
                "calendar.events",
                "receive.messages",
                "course.changes",
                "grades"
            ]:
                action_dialog[dialog] = next(it)
                action_dialog[dialog+" "] = next(it)
        except StopIteration:
            pass
        dialog = process.extractOne(accion, action_dialog, scorer=fuzz.ratio, score_cutoff=60)
        self.speak_dialog(str(dialog[2]).strip())


    @intent_handler(IntentBuilder("ActionsIntent").require("WhatCanYouDo"))
    def actionsList(self, message):
        self.speak_dialog("actions")


def create_skill():
    return UbuHelpSkill()
