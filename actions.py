
import os, sys
import django
from django.core.wsgi import get_wsgi_application
from typing import Text, List, Any, Dict
from urllib import request
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import date
from mydatabase import *
from my_project.my_app.views import getID
import smtplib
from debugpy import connect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.my_project.settings')
django.setup()

application = get_wsgi_application()

#sys.path.append('/Users/Nour/Desktop/Pi Project french/my_project/my_project')


id_costumer =''
print(getID)

    


#motrer le montant possible de credit
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
# ajouter un credit
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
            # Getting the data stored in the database
            info =get_userinfo(1)
            user_name = info.name
            email=info.email         
            # Code to send email
            # Creating connection using smtplib module
            s = smtplib.SMTP('smtp.gmail.com',587)
            # Making connection secured
            s.starttls()     
            # Authentication
            s.login("bankingchatbot1@gmail.com", "bank123bank")
        
            # Message to be sent
            message = "Subject:Demande de credit acceptée Bonjour {}, votre demande d'un credit etait accepter. la somme de votre credit est {} a payer durant {} ans. merci pour votre confiance dans notre service. à bientot".format(user_name,credit,duration)
            
            # Sending the mail
            s.sendmail("bankingchatbot1@gmail.com",email, message)
            
            # Closing the connection
            s.quit()
            
        return []

class CartCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_car_credit_duration"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "5 years", "payload":'/get_duration5{"duration":"5"}'})
        buttons.append({"title": "7 years", "payload":'/get_duration7{"duration":"7"}'})
        buttons.append({"title": "10 years", "payload":'/get_duration10{"duration":"10"}'})
 
        dispatcher.utter_message(text="Please select the credit duration you desire", buttons = buttons)
    
        return []

class PersonalCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_personal_credit_duration"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "5 years", "payload":'/get_duration5{"duration":"5"}'})
        buttons.append({"title": "7 years", "payload":'/get_duration7{"duration":"7"}'})
 
        dispatcher.utter_message(text="Please select the personal credit duration you desire", buttons = buttons)
    
        return []

class RealCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_real_estate_credit_duration"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "7 years", "payload":'/get_duration7{"duration":"7"}'})
        buttons.append({"title": "10 years", "payload":'/get_duration10{"duration":"10"}'})
        buttons.append({"title": "15 years", "payload":'/get_duration15{"duration":"15"}'})
        buttons.append({"title": "20 years", "payload":'/get_duration20{"duration":"20"}'})
 
        dispatcher.utter_message(text="Please select the credit duration you desire", buttons = buttons)
    
        return []

class CreditTypeAction(Action):
    def name(self) -> Text:
        return "action_credit_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Personal credit", "payload":'/personal_credit{"credit_type":"personal credit"}'})
        buttons.append({"title": "Car credit", "payload":'/car_credit{"credit_type":"car credit"}'})
        buttons.append({"title": "Real estate credit", "payload":'/real_estate_credit{"credit_type":"real estate credit"}'})
    
        dispatcher.utter_message(text="Please select the account type you desire", buttons = buttons)
    
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