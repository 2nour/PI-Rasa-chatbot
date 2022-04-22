
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import smtplib



class ValidateCreditForm(Action):
    def name(self) -> Text:
        return "validate_credit_form"

    @staticmethod
    def credit(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        ## somme totale : salaire + 0.25 * 12 
        salaire = tracker.get_slot('salaire')
        duree = tracker.get_slot('duree')
        creditPossible = int(salaire) *0.25/12 - 12 * int(duree)
    
        return dispatcher.utter_message(text = "Montant de credit est " + str(creditPossible) + "par mois" )

    def validate_salary(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate salary value."""
        salary_int = tracker.get_slot('salaire')
        if int(salary_int) > 450 :
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"salaire": salary_int}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(template = "utter_wrong_salary")
            return {"salaire": None}
    
    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate duration value."""
        duration_int = tracker.get_slot('duree')
        if int(duration_int) > 1 and duration_int < 25 :
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"duree": duration_int}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(template = "utter_wrong_duration")
            return {"duree": None}



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
        s.login("lovelovern12@gmail.com", "Nn2121997")
          
        # Message to be sent
        message = "Hello {} , This is a demo message".format('nour')
          
        # Sending the mail
        s.sendmail("lovelovern12@gmail.com",'lovelovern12@gmail.com', message)
          
        # Closing the connection
        s.quit()
          
        # Confirmation message
        dispatcher.utter_message(text="Email has been sent.")
        return []