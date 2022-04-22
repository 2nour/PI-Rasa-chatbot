import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker  
from rasa_sdk.executor import CollectingDispatcher
from datetime import date

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import *



class PossibleCreditAction(Action):
    def name(self) -> Text:
        return "action_possible_credit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salary")
        duration = tracker.get_slot("duration")
        credit_type = tracker.get_slot("credit_type")
        if (credit_type =="personal credit"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "car credit"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        
        dispatcher.utter_message(text = "your possible credit amount is"+str(credit))
        return []

class CreateAccountAction(Action):
    def name(self) -> Text:
        return "action_create_account"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        idd = tracker.get_slot("id")
        cin= int(idd)
        email = tracker.get_slot("email")
        birthdate = tracker.get_slot("birthdate")
        number = tracker.get_slot("number")
        num = int(number)
        address= tracker.get_slot("address")
        login = tracker.get_slot("login")
        password = tracker.get_slot("password")
        account_type = tracker.get_slot("account_type")
        today = date.today()
        date_open = today.strftime("%Y-%m-%d")
        balance = 0.0
        RIB = get_rib()+1
        a = verif_cin(cin)
        b = verif_login(login)
        c = verif_mail(email)
        if(len(idd)!=8):
            dispatcher.utter_message(text = "your id number is invalid ")
        elif(len(a)!=0):
            dispatcher.utter_message(text = "the id is allready used")
        elif(len(b)!=0):
            dispatcher.utter_message(text = "the login is allready used")
        elif(len(c)!=0):
            dispatcher.utter_message(text = "the login is allready used")
        else:
            #create_account(name, cin, email, birthdate, num, address, login, password, RIB, date_open , balance, account_type) 

            dispatcher.utter_message(text = "your account is added successfully ")
        return []

class AccountTypeAction(Action):
    def name(self) -> Text:
        return "action_account_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Savings account", "payload":'/savings_account_ty{"account_type":"savings account"}'})
        buttons.append({"title": "Current account", "payload":'/current_account_ty{"account_type":"current account"}'})
        buttons.append({"title": "Salary account", "payload":'/salary_account_ty{"account_type":"salary account"}'})
    
        dispatcher.utter_message(text="Please select the account type you desire", buttons = buttons)
    
        return []

class CarCreditDurationAction(Action):
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

class CreateCreditAction(Action):
    def name(self) -> Text:
        return "action_create_credit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salary")
        duration = tracker.get_slot("duration")
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
            dispatcher.utter_message(text = "the desired credit amount is greater than the possible amount ")
        else:
            create_credit(date_sub, int(duration), int(desired_amount), credit_type, account_id,0 , 1)
            dispatcher.utter_message(text = "operation done , the credit amount was addes to your balance")
        return []

class ShowBalanceAction(Action):
    def name(self) -> Text:
        return "action_show_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id =1
        balance = show_balance(account_id)
        dispatcher.utter_message(text = "Your current balance is: "+balance)
        return []

class CheckEarningsAction(Action):
    def name(self) -> Text:
        return "action_check_earnings"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id =1                                      
        cur = check_earnings(account_id)
        for i in cur :
            dispatcher.utter_message(text = i)
        return []

class TransferMOneyAction(Action):
    def name(self) -> Text:
        return "action_transfer_money"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        name = tracker.get_slot("reciever_name")
        rib = tracker.get_slot("RIB")
        amount = tracker.get_slot("transf_amount")
        a = verif_transfer_info(name,rib)
        b = verif_amount(amount,account_id)
        account_id=1
        if(len(a)==0):
            dispatcher.utter_message(text = "wrong customer name or RIB")
        elif(b==0):
            dispatcher.utter_message(text = "insufficient balance")
        else:
            transfer_money(rib , amount, account_id)
            dispatcher.utter_message(text = "Transaction went successfully")

        return []

class CloseAccountAction(Action):
    def name(self) -> Text:
        return "action_delete"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        today = date.today()
        date_closed = today.strftime("%Y-%m-%d")
        account_id=1
        close_account(date_closed, account_id)
        dispatcher.utter_message(text = "Your account was closed successfully")
        return []

class AskWhyAction(Action):
    def name(self) -> Text:
        return "action_ask_why"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Switching Bank", "payload":'/swittching_bank{"reason":"swaitching bank "}'})
        buttons.append({"title": "Poor Customer Services", "payload":'/poor_services{"reason":"poor customer services"}'})
        buttons.append({"title": " High Charges and Fees", "payload":'/high_charges{"reason":"high charges and fees"}'})
    
        dispatcher.utter_message(text="Please select the reason why you want to delete your account", buttons = buttons)
    
        return []


class TransactionsTypoeAction(Action):
    def name(self) -> Text:
        return "action_transactions_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Last 5", "payload":'/last_five_trans{"transactions_type":"last five"}'})
        buttons.append({"title": "All", "payload":'/all_trans{"transactions_type":"All "}'})
    
        dispatcher.utter_message(text="Please select the trasnactions you want to get", buttons = buttons)
    
        return []

class ComplaintTypoeAction(Action):
    def name(self) -> Text:
        return "action_complaint_type"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Server crash problem", "payload":'/transactions_typee{"complaint_type":"server crash problem}'})
        buttons.append({"title": "Transactions problem", "payload":'/transactions_typee{"complaint_type":"transactions problem}'})
        buttons.append({"title": "Sign_in problem", "payload":'/transactions_typee{"complaint_type":"sign_in problem}'})
        buttons.append({"title": "Other problem", "payload":'/transactions_typee{"complaint_type":"other problem}'})
    
        dispatcher.utter_message(text="Please select the trasnactions you want to get", buttons = buttons)
    
        return []

class CreateComplaintAction(Action):
    def name(self) -> Text:
        return "action_create_complaint"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        desc = tracker.get_slot("complaint_type")
        rib = tracker.get_slot("rib")
        problem = tracker.get_slot("problem")
        ref = random.randint(367,5246)
        if(len(verif_rib(int(rib)))==0):
            dispatcher.utter_message(text = "Invalid RIB")
        elif(desc == "other prtoblem"):
            create_complaint(problem, int(rib), ref)
            dispatcher.utter_message(text = "Complaint stored succesffully")
        else:
            create_complaint(desc, int(rib), ref)
            dispatcher.utter_message(text = "Complaint stored succesffully")
        return []

class CheckComplaintAction(Action):
    def name(self) -> Text:
        return "action_check_complaint_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        rib = tracker.get_slot("rib")
        stat = complaint_status(rib)
        if(len(verif_rib(int(rib)))==0):
            dispatcher.utter_message(text = "Invalid RIB")
        else:
            dispatcher.utter_message(text = "Your complaint is+"+stat)
        return []