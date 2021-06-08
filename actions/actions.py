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
from .cuisine_restaurants import check_location,check_cuisine,find_cuisine,restaurant_search

class ActionCustomCuisine(Action):

    def name(self) -> Text:
        return "action_custom_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.get_slot("cuisine"))
        print(tracker.get_slot("location"))
        print(tracker.get_intent_of_latest_message())
        entity_cuisnie=tracker.get_slot("cuisine")
        loc=tracker.get_slot("location")
        if(loc==None):
            return [SlotSet("restaurants",None)]
        entity_id,entity_type=check_location(loc)
        print(entity_id,entity_type)
        if entity_id==None and entity_type==None:
            return [SlotSet("cuisine",None)]
        else:
            if entity_cuisnie==None:
                entity_cuisnie=find_cuisine(entity_id,entity_type)
                dispatcher.utter_message(text=f"{entity_cuisnie} is the top cusinie at your area.I will find restaurants according to it.")
                SlotSet("cuisine",entity_cuisnie)
                restaurants=restaurant_search(entity_id,entity_type,entity_cuisnie)
                return [SlotSet("restaurants",restaurants)]
            else:
                cuisine_id=check_cuisine(entity_id,entity_cuisnie)
                if cuisine_id ==None:
                    return [SlotSet("cuisine",None)]
                else:
                    restaurants=restaurant_search(entity_id,entity_type,entity_cuisnie)
                    dispatcher.utter_message(text = f"Let me find some restaurants for {entity_cuisnie} cuisine for you in {loc}.")
                    return [SlotSet("restaurants",restaurants)]



class ActionFindRestaurants(Action):

    def name(self) -> Text:
        return "action_find_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurants= tracker.get_slot("restaurants")
        if restaurants is None:
            dispatcher.utter_message(text="Sorry i cannot find the result for the preferences you mentioned.")
            dispatcher.utter_message(text="May be you can check zomato website for further information")
            return [SlotSet("cuisine",None)]
        restaurants= ",".join(i for i in restaurants)
        dispatcher.utter_message(text = f"These are some restaurants I found {restaurants}")

        return [SlotSet("cuisine",None)]

