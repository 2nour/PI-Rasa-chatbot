from os import link
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker  
from rasa_sdk.executor import CollectingDispatcher
from datetime import date
import pandas as pd
from typing import Text, List, Any, Dict
from pdf.table_class import *
from typing import Text, List, Any, Dict
import smtplib
import imghdr
from email.message import EmailMessage
from currency.currency import *
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import *
import webbrowser
from nearest_agency import *
import googletrans
from googletrans import *
import pyttsx3
from image_ocr.ocr_process import *
from difflib import SequenceMatcher




class currency(Action):
     def name(self) -> Text:
        return "action_currency_calculator"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        amnt = tracker.get_slot("amount-of-money")
        frm = tracker.get_slot("currency_dep")
        to = tracker.get_slot("currency_arriv")
        msg=currencyConversion (int(amnt),frm,to)
        dispatcher.utter_message(text=msg)

        return []


class extrait_bnk(Action):
     def name(self) -> Text:
        return "action_extrait_bnk"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            extrait()
            rep="file:///C:/Users/medez/Desktop/pi/extrait.pdf"
            dispatcher.utter_message(rep)
            email = getMail_by_AccountId(account_id)
            msg = EmailMessage()
            msg['Subject'] = 'You got your bank statement!'
            msg['From'] = 'bankingchatbot1@gmail.com'
            msg['To'] = str(email)
            

            msg.set_content('This is your bank statement')

            file ="C:/Users/medez/Desktop/pi/extrait.pdf"
            with open(file,'rb') as f :
                file_data= f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data,maintype='application',subtype='octet-stram',filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                smtp.send_message(msg)
            dispatcher.utter_message(text="Email has been sent.")
        
            #attachment = {"document": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
            #dispatcher.utter_custom_json(attachment)
        
        return []


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
        if(int(salary)< 450): 
            dispatcher.utter_message(text = "your salary is less than the minimum threshhold")
        elif(credit_type =="personal credit"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "car credit"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        
        dispatcher.utter_message(text = "your possible credit amount is "+str(credit))
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
        f_name = tracker.get_slot("first_name")
        l_name = tracker.get_slot("last_name")
        email = tracker.get_slot("email")
        birthdate = tracker.get_slot("birthdate")
        number = tracker.get_slot("number")
        num = int(number)
        address= tracker.get_slot("address")
        account_type = tracker.get_slot("account_type")
        today = date.today()
        date_open = today.strftime("%Y-%m-%d")
        #dispatcher.utter_message(text = "your name is : "+f_name+" "+l_name+"\nyour email is : "+email+"\nyour birthdate is: "+birthdate+"\nyour phone number is :"+number+"\nyour address is : "+address+"\nthe desired account type : "+account_type)
        #dispatcher.utter_message(text = "now we'll proceed to verification using identity card , the camera will be open , To take a picture press S key then Z to quit")
        name = str(f_name)+" "+str(l_name )
        name="mohamed amine zarrouki"
        f_name="mohamed amine"
        login = f_name+""+str(number)
        
        c = verif_mail(email)
        RIB = get_rib()+1

        cin_ocr,last_n,name_ocr = ocr_pross(RIB)
        cin_ocr =   cin_ocr[0]
        print(name_ocr)
        if (len(name_ocr)==1):
            name_tt = name_ocr[0]
            print("name_tt : "+name_tt)
        if (len(name_ocr)>1 ):
            name_tt = name_ocr[0]+' '+name_ocr[1]
            print("name_tt : "+name_tt)   
        
        translator = googletrans.Translator()
        translate = translator.translate(name_tt, dest='english')
        print("txt   ;   "+translator.translate(name_tt, dest='english').text)
        name_tt=translate.text
        
        print("name_tt : "+name_tt)
        print("cin_tt: "+str(cin_ocr))

        f_name = f_name.replace(" ", "")
        name_tt = name_tt.replace(" ", "")

        rat = SequenceMatcher(None, f_name, name_tt).ratio()
        print(rat)
        cin = cin_ocr
        password = cin
        a = verif_cin(cin)
        if(len(cin)!=8):
            dispatcher.utter_message(text = "your id number is invalid ")
        elif(cin.isalnum()==False):
            dispatcher.utter_message(text = "your id number must conttain only numbers ")
        elif(a!=0):
            dispatcher.utter_message(text = "this id is allready used")
        elif(c!=0):
            dispatcher.utter_message(text = "this email is allready used")
        elif(rat<0.5 and (cin != cin_ocr)):
            print("data non valid")
            dispatcher.utter_message(text = "data non valid ")
        else:
            
            balance = 0.0
            create_account(name, cin, email, birthdate, num, address, login, password, RIB, date_open , balance, account_type) 
            dispatcher.utter_message(text = "your request was stored, you'll be directed to scan your id ")
            msg = EmailMessage()
            msg['Subject'] = 'Account created'
            msg['From'] = 'bankingchatbot1@gmail.com'
            #msg['To'] = str(email)
            msg['To'] = 'bankingchatbot1@gmail.com'
            msg.set_content("Your account was added successfully")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                smtp.send_message(msg)
        dispatcher.utter_message(text="Email has been sent.")
     
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
    
        dispatcher.utter_message(text="Please select the credit type you desire", buttons = buttons)
    
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
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            salary = tracker.get_slot("salary")
            duration = tracker.get_slot("duration")
            credit_type = tracker.get_slot("credit_type")
            desired_amount = tracker.get_slot("amount-of-money")
            today = date.today()
            date_sub = today.strftime("%Y-%m-%d")
            if(int(salary)<450):
                dispatcher.utter_message(text = "your salary is less than the minimum threshhold")
            elif (credit_type =="personal credit"):
                credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
            elif (credit_type == "car credit"):
                credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
            else:
                credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
            if (credit<int(desired_amount)): 
                dispatcher.utter_message(text = "the desired credit amount is greater than the possible amount ")
            else:
                create_credit(date_sub, int(duration), float(desired_amount), credit_type, account_id,0 , 1)
                dispatcher.utter_message(text = "operation done , credit accepted")
                email = getMail_by_AccountId(account_id)
                msg = EmailMessage()
                msg['Subject'] = 'Credit accepted'
                msg['From'] = 'bankingchatbot1@gmail.com'
                msg['To'] = str(email)
                msg.set_content('Congratulations your credit applicatio has been accepted')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                    smtp.send_message(msg)
                dispatcher.utter_message(text="Email has been sent.")
            
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
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            balance = show_balance(account_id)
            dispatcher.utter_message(text = "Your balance is: "+balance)
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
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:                             
            cur = check_earnings(account_id)
            for i in cur :
                print(i)
                dispatcher.utter_message(text = ""+str(i[0])+" "+str(i[1])+" "+str(i[2])+" "+str(i[3]))
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
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            rib = tracker.get_slot("rib")
            amount = tracker.get_slot("amount-of-money")
            b = verif_amount(float(amount),account_id)
            if(b==0):
                dispatcher.utter_message(text = "insufficient balance")
            else:
                transfer_money(rib , float(amount), account_id)
                r_mail = getMailBy_RIB(rib)
                dispatcher.utter_message(text = "Transaction went successfully ")
                msg = EmailMessage()
                msg['Subject'] = 'New Transaction '
                msg['From'] = 'bankingchatbot1@gmail.com'
                msg['To'] = str(r_mail)
                msg.set_content('You got a new transaction ,amount recieved is :{}check your account balance if you want').format(amount)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                    smtp.send_message(msg)
                dispatcher.utter_message(text="Email has been sent.")

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
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            today = date.today()
            date_closed = today.strftime("%Y-%m-%d")
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
        buttons.append({"title": "Switching Bank", "payload":'/swittching_bank{"reason":"switching bank "}'})
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
        buttons.append({"title": "Server crash problem", "payload":'/complaint_typee{"complaint_type":"server crash problem}'})
        buttons.append({"title": "Transactions problem", "payload":'/complaint_typee{"complaint_type":"transactions problem}'})
        buttons.append({"title": "Sign_in problem", "payload":'/complaint_typee{"complaint_type":"sign_in problem}'})
    
        dispatcher.utter_message(text="Please select the complaint type ", buttons = buttons)
    
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

class ShowAgenciesAction(Action):
    def name(self) -> Text:
        return "action_show_agencies"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        df = pd.read_csv(r"C:\Users\medez\Desktop\pi\agencies_locations.csv")
        m = folium.Map(location=[36, 10], tiles='openstreetmap', zoom_start=7)
        for idx, row in df.iterrows():
            Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)
        m.save("map.html")
        webbrowser.open("map.html")
        return []

class AccceptLocationAction(Action):
    def name(self) -> Text:
        return "action_use_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Accept", "payload":'/track_location{"track_status":"Yes"}'})
        buttons.append({"title": "Deny", "payload":'/track_location{"track_status":"No"}'})
    
        dispatcher.utter_message(text="Do you allow me to locate your position ?", buttons = buttons)
    
        return []

class NearestagencyAction(Action):
    def name(self) -> Text:
        return "action_nearest_agency"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        bool = tracker.get_slot("track_status")
        if(bool=="Yes"):
            map = nearest_ag()
            map.save("map.html")
            webbrowser.open("map.html")
        else:
            dispatcher.utter_message(text ="As you like you wish")
        return []
    
class ChequeRequestAction(Action):
    def name(self) -> Text:
        return "action_cheque_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You need to sign in")
        else:
            num_demande = random.randint(100,999)
            cheque_request(num_demande, account_id)
            dispatcher.utter_message(text = "Request stored successfully \nyour application number is : "+str(num_demande))
        return[]

class TunisianResidentAction(Action):
    def name(self) -> Text:
        return "action_tunisian_resident"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Tunisian", "payload":'/tunisian{"residency":"tunisian"}'})
        buttons.append({"title": "Resident", "payload":'/resident{"residency":"resident"}'})
        dispatcher.utter_message(text="Please select the button that describes your status", buttons = buttons)
        return[]

class ChequeStatusAction(Action):
    def name(self) -> Text:
        return "action_cheque_request_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        request_num = tracker.get_slot("request_num")
        status = cheque_request_status(request_num)
        dispatcher.utter_message(text = 'you request status is : '+status)
        return[]

class VerifRibNameAction(Action):
    def name(self) -> Text:
        return "action_verif_rib_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        rib =  tracker.get_slot("rib")
        name = verif_rib_name(rib)
        buttons = []
        buttons.append({"title": "Agree", "payload":'/submit_n{"sub_type":"yes"}'})
        buttons.append({"title": "Decline", "payload":'/submit_n{"sub_type":"no"}'})
    
        dispatcher.utter_message(text="The reciever name is: "+name, buttons = buttons)
    
        return []

class Sign_inAction(Action):
     def name(self) -> Text:
        return "action_sign_in"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text = "please connect via this link http://127.0.0.1:8000/login/")
        return []
class LogOutAction(Action):
     def name(self) -> Text:
        return "action_logout"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "You're not signed in")
        else:
            logout()
            dispatcher.utter_message(text = "You're logged out")

        return []

class LogoutVerifAction(Action):
    def name(self) -> Text:
        return "action_logout_verif"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Logout", "payload":'/submit_n{"sub_type":"yes"}'})
        buttons.append({"title": "Stay", "payload":'/submit_n{"sub_type":"no"}'})
        dispatcher.utter_message(text="Are you sure you want logout ", buttons = buttons)
        return[]

class extrait_bnk(Action):
     def name(self) -> Text:
        return "action_extrait_bnk_tn"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Une authentification est requise")
        else:
            extrait()
            rep="file:///C:/Users/medez/Desktop/pi/extrait.pdf"
            dispatcher.utter_message(rep)
            email = getMail_by_AccountId(account_id)
            msg = EmailMessage()
            msg['Subject'] = 'Vous avez reçu votre extrait'
            msg['From'] = 'bankingchatbot1@gmail.com'
            msg['To'] = str(email)
            

            msg.set_content('Voici votre extrait bancaire')

            file ="C:/Users/medez/Desktop/pi/extrait.pdf"
            with open(file,'rb') as f :
                file_data= f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data,maintype='application',subtype='octet-stram',filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                smtp.send_message(msg)
            dispatcher.utter_message(text="Un mail a été envoyé.")
        
            #attachment = {"document": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
            #dispatcher.utter_custom_json(attachment)
        
        return []

class ChequeRequestAction(Action):
    def name(self) -> Text:
        return "action_cheque_request_fr"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Une authentification est requise")
        else:
            num_demande = random.randint(100,999)
            cheque_request(num_demande, account_id)
            dispatcher.utter_message(text = "Opération effectuée avec succés votre numéro de demande est : "+str(num_demande))
        return[]

class LogOutAction(Action):
     def name(self) -> Text:
        return "action_logout_fr"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Aucune connexion est enregistrée")
        else:
            logout()
            dispatcher.utter_message(text = "Vous êtes maintenant déconnecté ")

        return []

class LogoutVerifAction(Action):
    def name(self) -> Text:
        return "action_logout_verif_fr"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Se déconnecter", "payload":'/submit_n{"sub_type":"oui"}'})
        buttons.append({"title": "Rester", "payload":'/submit_n{"sub_type":"non"}'})
        dispatcher.utter_message(text="Vous voulez quittez ? ", buttons = buttons)
        return[]

class currency(Action):
     def name(self) -> Text:
        return "action_currency_calculator_tn"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        amnt = tracker.get_slot("amount-of-money")
        frm = tracker.get_slot("currency_dep")
        to = tracker.get_slot("currency_arriv")
        msg=currencyConversion (int(amnt),frm,to)
        dispatcher.utter_message(text=msg)

        return []


class extrait_bnk(Action):
     def name(self) -> Text:
        return "action_extrait_bnk_tn"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:
            extrait()
            rep="file:///C:/Users/medez/Desktop/pi/extrait.pdf"
            dispatcher.utter_message(rep)
            email = getMail_by_AccountId(account_id)
            msg = EmailMessage()
            msg['Subject'] = 'You got new transaction!'
            msg['From'] = 'bankingchatbot1@gmail.com'
            msg['To'] = str(email)
            

            msg.set_content('This is a plain text email')

            file ="C:/Users/medez/Desktop/pi_tn/extrait.pdf"
            with open(file,'rb') as f :
                file_data= f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data,maintype='application',subtype='octet-stram',filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                smtp.send_message(msg)
            dispatcher.utter_message(text="Baathenelek mmail.")
        
            #attachment = {"document": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"}
            #dispatcher.utter_custom_json(attachment)
        
        return []

class PossibleCreditAction(Action):
    def name(self) -> Text:
        return "action_possible_credit_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        salary = tracker.get_slot("salary")
        duration = tracker.get_slot("duration")
        credit_type = tracker.get_slot("credit_type")
        if(int(salary)< 450): 
            dispatcher.utter_message(text = "salaire mte3ek a9al mel minimum salaire nécessaire")
        elif(credit_type =="credit personnel"):
            credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
        elif (credit_type == "credit voiture"):
            credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
        else:
            credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
        
        dispatcher.utter_message(text = "l montant possible elli tnajam tekhdhou : "+str(credit)+" dinars")
        return []

class CreateAccountAction(Action):
    def name(self) -> Text:
        return "action_create_account_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        f_name = tracker.get_slot("name")
        l_name = tracker.get_slot("last_name")
        name = f_name+" "+l_name 
        cin = tracker.get_slot("id")
        email = tracker.get_slot("email")
        birthdate = tracker.get_slot("birthdate")
        number = tracker.get_slot("number")
        num = int(number)
        address= tracker.get_slot("address")
        account_type = tracker.get_slot("account_type")
        today = date.today()
        date_open = today.strftime("%Y-%m-%d")
        buttons = []
        buttons.append({"title": "confirmi", "payload":'/submit_n_tn{"sub_type":"oui"}'})
        buttons.append({"title": "reufse", "payload":'/submit_n_tn{"sub_type":"non"}'}) 
        dispatcher.utter_message(text = "esmek: "+name+"\nnum bita9et ta3rif : "+cin+"\nl'email mte3ek  : "+email+"\n3id mileledek : "+birthdate+"\nnoumrouk :"+number+"\nadress mte3ek : "+address+"\nl compte elli t7eb ta3mlou : "+account_type)
 
        dispatcher.utter_message(text="Les informations mte3ek s7a7", buttons = buttons)
        dispatcher.utter_message(text ="tawa netaadew lel verification b Cin l cam mte3ek besh tet7al besh te5ou capture enzel s w ba3d q , svp hawel tkoun cin wadh7a" )
        
        return []

class CreateAccountAction1(Action):
    def name(self) -> Text:
        return "action_create_account1"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        sub = tracker.get_slot("sub_type")
        f_name = tracker.get_slot("name")
        l_name = tracker.get_slot("last_name")
        name = f_name+" "+l_name 
        cin = tracker.get_slot("id")
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
        login = f_name+number
        password = cin
        if(sub == "no"):
            dispatcher.utter_message(text = "A3mel verification lel informations mte3ek w 7awel men jdid")
        else :
            a = verif_cin(cin) 
            c = verif_mail(email)
            RIB = get_rib()+1

            cin_ocr,last_n,name_ocr = ocr_pross(RIB)
            cin_ocr =   cin_ocr[0]
            print(name_ocr)
            if (len(name_ocr)==1):
                name_tt = name_ocr[0]
                print("name_tt : "+name_tt)
            if (len(name_ocr)>1 ):
                name_tt = name_ocr[0]+' '+name_ocr[1]
                print("name_tt : "+name_tt)   
            
            translator = googletrans.Translator()
            translate = translator.translate(name_tt, dest='english')
            print("txt   ;   "+translator.translate(name_tt, dest='english').text)
            name_tt=translate.text
            
            print("name_tt : "+name_tt)
            print("cin_tt: "+str(cin_ocr))

            f_name = f_name.replace(" ", "")
            name_tt = name_tt.replace(" ", "")

            rat = SequenceMatcher(None, f_name, name_tt).ratio()
            print(rat)
            
            if(len(cin)!=8):
                dispatcher.utter_message(text = "numéro bita9et ta3rif invalid ")
            elif(cin.isalnum()==False):
                dispatcher.utter_message(text = "numéro bita9et ta3rif yelzem kollou des chiffres ")
            elif(a!=0):
                dispatcher.utter_message(text = "numéro bita9et ta3rif déjà mesta3mel")
            elif(c!=0):
                dispatcher.utter_message(text = "email hedha déjà mesta3mel")
            elif(rat<0.5 and (cin != cin_ocr)):
                print("data non valid")
                dispatcher.utter_message(text = "les informations mte3 cin welli 3addithom fel formulaires mesh identiques")
            else:
                
                balance = 0.0
                create_account(name, cin, email, birthdate, num, address, login, password, RIB, date_open , balance, account_type) 
                dispatcher.utter_message(text = "compte ajouté , login mte3ek :"+login+" mot de passe : "+password+"svp 7awel ma twarri tes informations l 7ad")
                msg = EmailMessage()
                msg['Subject'] = 'Compte Ajouté'
                msg['From'] = 'bankingchatbot1@gmail.com'
                #msg['To'] = str(email)
                msg['To'] = 'bankingchatbot1@gmail.com'
                msg.set_content("C'est bon creation du compte  t3amlet")
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                    smtp.send_message(msg)
                dispatcher.utter_message(text="C'est bon b3athnelek mail")
        return []


class AccountTypeAction(Action):
    def name(self) -> Text:
        return "action_account_type_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Compte épargne", "payload":'/savings_account_ty_tn{"account_type":"compte épargne"}'})
        buttons.append({"title": "Compte courant", "payload":'/current_account_ty_tn{"account_type":"compte courant"}'})
        buttons.append({"title": "Compte salaire", "payload":'/salary_account_ty_tn{"account_type":"compte salaire"}'})
    
        dispatcher.utter_message(text="Svp akhtar type de compte", buttons = buttons)
    
        return []

class CarCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_car_credit_duration_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "5 snin", "payload":'/get_duration5_tn{"duration":"5"}'})
        buttons.append({"title": "7 snin", "payload":'/get_duration7_tn{"duration":"7"}'})
        buttons.append({"title": "10 snin", "payload":'/get_duration10_tn{"duration":"10"}'})
 
        dispatcher.utter_message(text="Svp akhtar durée de credit voiture", buttons = buttons)
    
        return []

class PersonalCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_personal_credit_duration_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "5 snin", "payload":'/get_duration5_tn{"duration":"5"}'})
        buttons.append({"title": "7 snin", "payload":'/get_duration7_tn{"duration":"7"}'})
 
        dispatcher.utter_message(text="Svp akhtar durée credit personnel", buttons = buttons)
    
        return []

class RealCreditDurationAction(Action):
    def name(self) -> Text:
        return "action_real_estate_credit_duration_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "10 snin", "payload":'/get_duration10_tn{"duration":"10"}'})
        buttons.append({"title": "15 snin", "payload":'/get_duration15_tn{"duration":"15"}'})
        buttons.append({"title": "20 snin", "payload":'/get_duration20_tn{"duration":"20"}'})
 
        dispatcher.utter_message(text="Svp akhtar durée credit immobilier", buttons = buttons)
    
        return []

class CreditTypeAction(Action):
    def name(self) -> Text:
        return "action_credit_type_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Credit personnel", "payload":'/personal_credit_tn{"credit_type":"personal credit"}'})
        buttons.append({"title": "Credit voiture", "payload":'/car_credit_tn{"credit_type":"car credit"}'})
        buttons.append({"title": "Credit immobilier", "payload":'/real_estate_credit_tn{"credit_type":"real estate credit"}'})
    
        dispatcher.utter_message(text="Svp akhtar type de credit", buttons = buttons)
    
        return []

class CreateCreditAction(Action):
    def name(self) -> Text:
        return "action_create_credit_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:
            salary = tracker.get_slot("salary")
            duration = tracker.get_slot("duration")
            credit_type = tracker.get_slot("credit_type")
            desired_amount = tracker.get_slot("amount-of-money")
            today = date.today()
            date_sub = today.strftime("%Y-%m-%d")
            if(int(salary)<450):
                dispatcher.utter_message(text = "salaire mte3ek a9al mel minimum salaire nécessaire")
            elif (credit_type =="personal credit"):
                credit = int(salary) * int(duration) * 12 * 0.25 * 0.9
            elif (credit_type == "car credit"):
                credit = int(salary) * int(duration) * 12 * 0.30 * 0.9
            else:
                credit = int(salary) * int(duration) * 12 * 0.40 * 0.9
            if (credit<int(desired_amount)): 
                dispatcher.utter_message(text = " l montant elli talbou akber mel montant possible ")
            else:
                create_credit(date_sub, int(duration), float(desired_amount), credit_type, account_id,0 , 1)
                dispatcher.utter_message(text = "Operation terminée avec succés , credit accepté")
        return []

class ShowBalanceAction(Action):
    def name(self) -> Text:
        return "action_show_balance_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:
            balance = show_balance(account_id)
            dispatcher.utter_message(text = "balance mte3ek : "+balance)
        return []

class CheckEarningsAction(Action):
    def name(self) -> Text:
        return "action_check_earnings_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:                             
            cur = check_earnings(account_id)
            for i in cur :
                print(i)
                dispatcher.utter_message(text = ""+str(i[0])+" "+str(i[1])+" "+str(i[2])+" "+str(i[3]))
        return []

class TransferMOneyAction(Action):
    def name(self) -> Text:
        return "action_transfer_money_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Lezem tabda connecté")
        else:
            rib = tracker.get_slot("rib")
            amount = tracker.get_slot("amount-of-money")
            print("amount:"+amount)
            b = verif_amount(float(amount),account_id)
            if(b==0):
                dispatcher.utter_message(text = "ma3andekch flous tekfi fil compte")
            else:
                transfer_money(rib , float(amount), account_id)
                s_mail = getMail_by_AccountId(account_id)
                print(s_mail)
                dispatcher.utter_message(text = "C'est bon tba3thou l flous ")
                msg = EmailMessage()
                msg['Subject'] = 'New Transaction '
                msg['From'] = 'bankingchatbot1@gmail.com'
                msg['To'] = str(s_mail)
                msg.set_content('Transfer money operation is done,you can check your balance')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("bankingchatbot1@gmail.com", "bank123bank")
                    smtp.send_message(msg)
                dispatcher.utter_message(text="B3athnelek mail .")

        return []

class CloseAccountAction(Action):
    def name(self) -> Text:
        return "action_delete_tn"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:
            today = date.today()
            date_closed = today.strftime("%Y-%m-%d")
            close_account(date_closed, account_id)
            dispatcher.utter_message(text = "Ton compte est fermé avec succés")
        return []

class AskWhyAction(Action):
    def name(self) -> Text:
        return "action_ask_why_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Besh tbadel l banque", "payload":'/swittching_bank_tn{"reason":"besh nbadal l banque"}'})
        buttons.append({"title": "Service khayeb", "payload":'/poor_services_tn{"reason":"service khayeb"}'})
        buttons.append({"title": "Barcha impôt", "payload":'/high_charges_tn{"reason":"barcha impot"}'})
    
        dispatcher.utter_message(text="Svp akhtar aaleh theb tsakkar l compte ", buttons = buttons)
    
        return []

class TransactionsTypoeAction(Action):
    def name(self) -> Text:
        return "action_transactions_type_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Derniers 5", "payload":'/last_five_trans_tn{"transactions_type":"derniers 5"}'})
        buttons.append({"title": "Tous", "payload":'/all_trans_tn{"transactions_type":"tous"}'})
    
        dispatcher.utter_message(text="Svp akhtar les transactions elli theb tchoufhom", buttons = buttons)
    
        return []

class ComplaintTypoeAction(Action):
    def name(self) -> Text:
        return "action_complaint_type_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Probleme serveur", "payload":'/complaint_typee_tn{"complaint_type":"probleme serveur}'})
        buttons.append({"title": "Probleme transactions", "payload":'/complaint_typee_tn{"complaint_type":"problemr transactions}'})
        buttons.append({"title": "Probleme connexion", "payload":'/complaint_typee_tn{"complaint_type":"problem connexion}'})
    
        dispatcher.utter_message(text="Svp akhtar type de réclamations", buttons = buttons)
    
        return []

class CreateComplaintAction(Action):
    def name(self) -> Text:
        return "action_create_complaint_tn"

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
            dispatcher.utter_message(text = "RIB invalide")
        else:
            create_complaint(desc, int(rib), ref)
            dispatcher.utter_message(text = "Recalamtion enregistrée")
        return []

class CheckComplaintAction(Action):
    def name(self) -> Text:
        return "action_check_complaint_status_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        rib = tracker.get_slot("rib")
        stat = complaint_status(rib)
        if(len(verif_rib(int(rib)))==0):
            dispatcher.utter_message(text = "RIB invalide")
        else:
            dispatcher.utter_message(text = "Etat de reclamation: "+stat)
        return []

class ShowAgenciesAction(Action):
    def name(self) -> Text:
        return "action_show_agencies_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        df = pd.read_csv(r"C:\Users\medez\Desktop\pi_tn\agencies_locations.csv")
        m = folium.Map(location=[36, 10], tiles='openstreetmap', zoom_start=7)
        for idx, row in df.iterrows():
            Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)
        m.save("map.html")
        webbrowser.open("map.html")
        return []

class AccceptLocationAction(Action):
    def name(self) -> Text:
        return "action_use_location_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Accepter", "payload":'/track_location_tn{"track_status":"oui"}'})
        buttons.append({"title": "Refuser", "payload":'/track_location_tn{"track_status":"non"}'})
    
        dispatcher.utter_message(text="Najam nekhou accés lel position mte3ek ?", buttons = buttons)
    
        return []

class NearestagencyAction(Action):
    def name(self) -> Text:
        return "action_nearest_agency_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        bool = tracker.get_slot("track_status")
        if(bool=="oui"):
            map = nearest_ag()
            map.save("map.html")
            webbrowser.open("map.html")
        else:
            dispatcher.utter_message(text ="Kima t7eb")
        return []

class ChequeRequestAction(Action):
    def name(self) -> Text:
        return "action_cheque_request"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Yelzem ta3mel sign in")
        else:
            num_demande = random.randint(100,999)
            cheque_request(num_demande, account_id)
            dispatcher.utter_message(text = "Demande enregistrée avec succés \nvotre numéro de demande est : "+str(num_demande))
        return[]

class TunisianResidentAction(Action):
    def name(self) -> Text:
        return "action_tunisian_resident_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Tousni", "payload":'/tunisian_tn{"residency":"tounsi"}'})
        buttons.append({"title": "Etranger", "payload":'/resident_tn{"residency":"etranger"}'})
        dispatcher.utter_message(text="Akhtar l'état mte3ek", buttons = buttons)
        return[]

class ChequeStatusAction(Action):
    def name(self) -> Text:
        return "action_cheque_request_status_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        request_num = tracker.get_slot("request_num")
        status = cheque_request_status(request_num)
        dispatcher.utter_message(text = "l'état de votre demande est : "+status)
        return[]

class VerifRibNameAction(Action):
    def name(self) -> Text:
        return "action_verif_rib_name_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        rib =  tracker.get_slot("rib")
        name = verif_rib_name(rib)
        buttons = []
        buttons.append({"title": "Valider", "payload":'/submit_n{"sub_type":"yes"}'})
        buttons.append({"title": "Annuler", "payload":'/submit_n{"sub_type":"no"}'})
    
        dispatcher.utter_message(text="Esm elli bech tab3athlou l flous : "+name, buttons = buttons)
    
        return []

class Sign_inAction(Action):
     def name(self) -> Text:
        return "action_sign_in_tn"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        dispatcher.utter_message(text = "svp odkhol lel lien hedha http://127.0.0.1:8000/login/")
        return []

class LogOutAction(Action):
     def name(self) -> Text:
        return "action_logout_tn"

     def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        account_id = getConnectionid()
        if( not account_id):
            dispatcher.utter_message(text = "Vous n'êtes pas connecté déjà")
        else:
            logout()
            dispatcher.utter_message(text = "C'est bon tu est déconnecté")

        return []

class LogoutVerifAction(Action):
    def name(self) -> Text:
        return "action_logout_verif_tn"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) ->List[Dict[Text, Any]]:
        buttons = []
        buttons.append({"title": "Logout", "payload":'/submit_n{"sub_type":"oui"}'})
        buttons.append({"title": "Non", "payload":'/submit_n{"sub_type":"non"}'})
        dispatcher.utter_message(text="Vous êtes sûr theb ta3mel déconnexion", buttons = buttons)
        return[]
