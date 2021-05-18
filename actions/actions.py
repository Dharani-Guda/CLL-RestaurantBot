# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .cuisine_restaurants import Restaurant_List

class ActionCustomCuisine(Action):

    def name(self) -> Text:
        return "action_custom_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.get_slot("cuisine"))
        print(tracker.get_intent_of_latest_message())
        entity=tracker.get_slot("cuisine")
        if entity not in Restaurant_List.keys():
            dispatcher.utter_message(response="utter_sorry_cuisine")
            return [SlotSet("cuisine",None)]
        else:
            restaurants=Restaurant_List[entity]
            dispatcher.utter_message(text = f"Let me find some restaurants for {entity} cuisine for you")
            return [SlotSet("restaurants",restaurants)]



class ActionFindRestaurants(Action):

    def name(self) -> Text:
        return "action_find_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurants= tracker.get_slot("restaurants")
        restaurants= ",".join(i for i in restaurants)
        dispatcher.utter_message(text = f"These are some restaurants I found {restaurants}")

        return [SlotSet("cuisine",None)]

