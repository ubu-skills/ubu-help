import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler  # type: ignore
sys.path.append("/usr/lib/UBUVoiceAssistant")  # type: ignore
from util import util  # type: ignore


class UbuHelpSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()


def create_skill():
    return UbuHelpSkill()
