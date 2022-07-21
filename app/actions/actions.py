# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

from datetime import datetime

# For regex expressions
import re

# Transfer to Human Agent
class Agent_Transfer_Check(Action):

    def name(self) -> Text:
        return "action_agent_transfer_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # monday starts from 1
        current_day = datetime.today().isoweekday()

        # connect to callback if on sunday
        # TODO: PUBLIC HOLIDAY?
        if current_day == 7:
            # dispatcher.utter_message(text="I'm sorry our office is closed now. Our live chat hours are 9am - 10pm Monday to Friday and 9am - 1pm on Saturday, excluding Sundays and public holidays.")
            return[SlotSet("activate_agent_form", value = "false")]

        # check time if it is on monday - saturday
        else: 
            # check time
            current_time = datetime.now()
            
            if current_day == 6:
                working_hours_start = datetime.strptime("09:00:00", "%H:%M:%S")
                working_hours_end = datetime.strptime("22:00:00", "%H:%M:%S")
            else:
                working_hours_start = datetime.strptime("09:00:00", "%H:%M:%S")
                working_hours_end = datetime.strptime("13:00:00", "%H:%M:%S")

        # connect to live agent if within working hours
        if working_hours_start < current_time < working_hours_end:
            # dispatcher.utter_message(text="Sure! We will require some details from you before connecting you to a Live Agent.")
            return[SlotSet("activate_agent_form", value = True)]

        else:
            # dispatcher.utter_message(text="I'm sorry our office is closed now. Our live chat hours are 9am - 10pm Monday to Friday and 9am - 1pm on Saturday, excluding Sundays and public holidays.")
            return[SlotSet("activate_agent_form", value = False)]

# Validate Agent Form Inputs
class ValidateAgentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agent_form"

    def validate_agent_form_user_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email address"""
        rgx_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(rgx_email, slot_value):
            return {"callback_form_user_email": slot_value}
        else:
            dispatcher.utter_message(text = "Please enter a valid email address.")
            return {"callback_form_user_email": None}

# Validate Callback Form Inputs
class ValidateCallbackForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agent_callback_form"

    def validate_callback_form_user_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email address"""
        rgx_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(rgx_email, slot_value):
            return {"callback_form_user_email": slot_value}
        else:
            dispatcher.utter_message(text = "Please enter a valid email address.")
            return {"callback_form_user_email": None}
    
    def validate_callback_form_user_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone number"""
        if len(slot_value) < 8 or len(slot_value) > 8:
            dispatcher.utter_message(text = "Please enter a 8-digit phone number that starts with 6, 8 or 9.")
            return {"callback_form_user_number": None}
        
        rgx_phone = re.compile(r"[6,8-9][0-9]{7}")

        if re.fullmatch(rgx_phone, slot_value):
            return {"callback_form_user_number": slot_value}
        else:
            dispatcher.utter_message(text = "Please enter a 8-digit phone number that starts with 6, 8 or 9.")
            return {"callback_form_user_number": None}