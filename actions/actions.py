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
from collections.abc import Iterable
from .bookings import booking

class ActionCustomCuisine(Action):

    def name(self) -> Text:
        return "action_custom_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.get_slot("cuisine"))
        print(tracker.get_slot("location"))
        print(tracker.get_slot("radius"))
        print(tracker.get_slot("category"))
        print(tracker.get_slot("establishment"))
        print(tracker.get_intent_of_latest_message())
        entity_cuisine=tracker.get_slot("cuisine")
        loc=tracker.get_slot("location")
        radius=tracker.get_slot("radius")
        category=tracker.get_slot("category")
        establishment=tracker.get_slot("establishment")
        if not(loc):
            
            return [SlotSet("restaurants",None)]
        entity_id,entity_type=check_location(loc)
        print(entity_id,entity_type)
        if not(entity_id) and not(entity_type):
            
            return [SlotSet("cuisine",None)]
        else:
            if not(entity_cuisine):
                
                entity_cuisnie=find_cuisine(entity_id,entity_type)
                dispatcher.utter_message(text=f"{entity_cuisnie} is the top cuisine at your area.I will find restaurants according to it.")
                SlotSet("cuisine",entity_cuisnie)
                restaurants=restaurant_search(entity_id,entity_type,entity_cuisnie)
                return [SlotSet("restaurants",restaurants)]
            else:

                cuisine_id=check_cuisine(entity_id,entity_cuisine)
                if not(cuisine_id):
                    
                    return [SlotSet("cuisine",None)]
                else:
                    if not(radius):
                        radius=2000
                    if not(establishment):
                        establishment="Casual Dining"
                    if not(category):
                        category="Delivery"
                    restaurants=restaurant_search(entity_id,entity_type,entity_cuisine,radius,establishment,category)
                    dispatcher.utter_message(text = f"Let me find some restaurants for {entity_cuisine} cuisine for you in {loc}.")
                    return [SlotSet("restaurants",restaurants)]



class ActionFindRestaurants(Action):

    def name(self) -> Text:
        return "action_find_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurants= tracker.get_slot("restaurants")
        print(restaurants)
        
        if not(restaurants) or not(isinstance(restaurants, Iterable)) :

            dispatcher.utter_message(response="utter_dont_know_location")
            return [SlotSet("cuisine",None)]

        restaurants= ",".join(i for i in restaurants)
        dispatcher.utter_message(text = f"These are some restaurants I found \n {restaurants}")

        return [SlotSet("cuisine",None)]



class ActionCheckBooking(Action):

    def name(self) -> Text:
        return "action_check_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone_num= tracker.get_slot("phone_num")
        print(phone_num)        
        if not(phone_num) or (phone_num not in booking.keys()):
            dispatcher.utter_message(response="utter_no_booking")
            return[]
        dispatcher.utter_message(text= f"Booking confirmed for {booking[phone_num]} to the number {phone_num}.")
        return []
