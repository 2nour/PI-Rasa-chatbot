
from datetime import datetime
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import date
from mydatabase import *
import smtplib


class PossibleCreditAction(Action):
    def name(self) -> Text:
        return "action_possible_credit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salaire")
        duration = tracker.get_slot("duree")
        credit_type = tracker.get_slot("credit_type")
        if (credit_type =="personal credit"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "car credit"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        
        dispatcher.utter_message(text = "Le montant de credit possible est"+str(credit))
        return []

class CreateCreditAction(Action):
    def name(self) -> Text:
        return "action_create_credit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salaire")
        duration = tracker.get_slot("duree")
        credit_type = tracker.get_slot("credit_type")
        desired_amount = tracker.get_slot("credit_amount")
        today = date.today()
        date_sub = today.strftime("%Y-%m-%d")
        if (credit_type =="personal credit"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "car credit"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        account_id=1
        if (credit<int(desired_amount)): 
            dispatcher.utter_message(text = "Ce montant depasse le seuil de credit possible")
        else:
            create_credit(date_sub, int(duration), int(desired_amount), credit_type, account_id,0 , 1)
            dispatcher.utter_message(text = "Success, ce credit a etais ajouter dans votre solde")
        return []


class ValidateCreditForm(Action):
    def name(self) -> Text:
        return "validate_credit_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salaire")
        duration = tracker.get_slot("duree")
        credit_type = tracker.get_slot("credit_type")
        desired_amount = tracker.get_slot("credit_amount")
        today = date.today()
        date_sub = today.strftime("%Y-%m-%d")
        if (credit_type =="personal credit"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "car credit"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        account_id=1
        if (credit<int(desired_amount)): 
            dispatcher.utter_message(text = "Ce montant depasse le seuil de credit possible")
        else:
            create_credit(date_sub, int(duration), int(desired_amount), credit_type, account_id,0 , 1)
            dispatcher.utter_message(text = "Success, ce credit a etais ajouter dans votre solde")
        return []



class ActionEmail(Action):
  
    def name(self) -> Text:
        
          # Name of the action
        return "action_email"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
  
        # Getting the data stored in the
        # slots and storing them in variables.
        user_name = tracker.get_slot("name")
        email_id = tracker.get_slot("email")
          
        # Code to send email
        # Creating connection using smtplib module
        s = smtplib.SMTP('smtp.gmail.com',587)
          
        # Making connection secured
        s.starttls() 
          
        # Authentication
        s.login("bankingchatbot1@gmail.com", "bank123bank")
          
        # Message to be sent
        message = "Hello {} , This is a demo message".format('nour')
          
        # Sending the mail
        s.sendmail("bankingchatbot1@gmail.com",'bankingchatbot1@gmail.com', message)
          
        # Closing the connection
        s.quit()
          
        # Confirmation message
        dispatcher.utter_message(text="Email has been sent.")
        return []