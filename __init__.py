import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler  # type: ignore
from mycroft.audio import wait_while_speaking
sys.path.append("/usr/lib/UBUVoiceAssistant")  # type: ignore
from UBUVoiceAssistant.util import util  # type: ignore


class UbuHelpSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("HelpIntent").require("Help"))
    def help(self, message):
        self.speak_dialog("help.dialog")
        wait_while_speaking()
        self.actionsList(message)

    @intent_handler(IntentBuilder("HowDoIIntent").require("Accion"))
    def howDoI(self, message):
        accion = message.data.get("Accion")
        accion_dialog = {
            "enviar un mensaje": "send.messages.dialog",
            "envío un mensaje": "send.messages.dialog",
            "consultar los foros": "forums.dialog",
            "leer los foros": "forums.dialog",
            "consulto los foros": "forums.dialog",
            "leo los foros": "forums.dialog",
            "consulto el calendario": "calendar.events.dialog",
            "consulto los eventos": "calendar.events.dialog",
            "leo los mensajes": "receive.messages.dialog",
            "veo los cambios": "course.changes.dialog",
            "consulto las notas": "grades.dialog",
            "veo mis notas": "grades.dialog",
            "veo mis calificaciones": "grades.dialog",
        }

    @intent_handler(IntentBuilder("ActionsIntent").require("WhatCanYouDo"))
    def actionsList(self, message):
        self.speak_dialog("actions.dialog")


def create_skill():
    return UbuHelpSkill()
