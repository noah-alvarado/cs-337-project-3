# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from asyncore import dispatcher
from typing import Any, Text, Dict, List
from recipe import Recipe
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class Global_Vars():
    recipe = None


class ActionAcceptUrl(Action):

    def name(self) -> Text:
        return "action_accept_url"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        Global_Vars.recipe = Recipe((tracker.latest_message)['text'])
        dispatcher.utter_message(text="Cool, let's get started with " + Global_Vars.recipe.recipe_name + "!")
        dispatcher.utter_message(text="Cool, let's get started with " + Global_Vars.recipe.recipe_name + "!")

        return []
