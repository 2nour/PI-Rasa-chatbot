from colorama import Cursor
from django.db import connection
import pymysql
from difflib import SequenceMatcher
mydatabase = pymysql.connect(
  host="localhost",
  port=3308 ,
  user="root",
  password="",
  database="rasadatabase"
)
#mydatabase =  pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", database="rasadatabase")

mycursor = mydatabase.cursor()

#mycursor.execute("CREATE TABLE Customers (id int AUTO_INCREMENT PRIMARY KEY, full_name VARCHAR(255) , cin int(8) , email varchar(255)  , birthdate DATETIME , phone_number varchar(255) ,address VARCHAR(255) ,login VARCHAR(255) NOT NULL, password varchar(255) NOT NULL)")
#mycursor.execute("CREATE TABLE Account (id int AUTO_INCREMENT PRIMARY KEY, RIB int(16) NOT NULL,  date_opened DATETIME NOT NULL , date_closed DATETIME , balance float NOT NULL , account_type varchar(255) NOT NULL , customer_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (customer_id) REFERENCES Customers(id) )")
#mycursor.execute("CREATE TABLE Credit (id int AUTO_INCREMENT PRIMARY KEY,  date DATE NOT NULL , duration int  NOT NULL , ammount float NOT NULL , credit_type varchar(255) NOT NULL  , account_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (account_id) REFERENCES  Account(id))")
#mycursor.execute("CREATE TABLE Credit_card (id int AUTO_INCREMENT PRIMARY KEY, credit_card_number int NOT NULL , date_exp date NOT NULL , cvv int NOT NULL , pin_code int NOT NULL , account_id int NOT NULL , constraint FK FOREIGN KEY  (account_id) REFERENCES Account(id))")
#mycursor.execute("CREATE TABLE Transactions (id int AUTO_INCREMENT PRIMARY KEY, date DATETIME NOT NULL , amount_of_transaction float NOT NULL , transaction_type varchar(255) NOT NULL , account_id int NOT NULL , external_account_id int NOT NULL ,constraint FK FOREIGN KEY  (account_id) REFERENCES Account(id), constraint FK1 FOREIGN KEY  (account_id) references  Account(id))" )
#mycursor.execute("CREATE TABLE Reclamation(id int AUTO_INCREMENT PRIMARY KEY, description varchar(255) NOT NULL , rib int(16) NOT NULL , status varchar(255) DEFAULT 'In progress' , ref_code int NOT NULL)")
#mycursor.execute("CREATE TABLE Cheque(id int AUTO_INCREMENT PRIMARY KEY, demande int NOT NULL , etat varchar(255) DEFAULT 'In progress' , account_id int NOT NULL, constraint FK FOREIGN KEY (account_id) REFERENCES Account(id))")
def verif_cin(cin):
  a = mycursor.execute('SELECT cin from Customers where cin='+cin)
  return a
def verif_login(login):
  a = mycursor.execute('SELECT login from Customers where login='+login)
  return a
def verif_mail(mail):
  a = mycursor.execute('SELECT email from Customers where email='+mail)
  return a
def get_rib():
  mycursor.execute('SELECT RIB from Account ORDER BY id DESC LIMIT 1')
  return mycursor.fetchall()

def create_account(fullname, cin, email, birthdate, number, address, login, password ,RIB, date_open, balance, account_type,customer_id):
  sql = 'INSERT INTO Customers(full_name, cin, email, birthdate, phone_number, address, login ,password) VALUES ("{0}","{1}", "{2}", "{3}", "{4}", "{5}" , "{6}" )'.format(fullname, cin, email, birthdate, number,  address, login, password)
  mycursor.execute(sql)
  sql= 'SELECT id FROM Customers ORDER BY id DESC LIMIT 1'
  #customer_id = mycursor.execute(sql)
  sql = 'INSERT INTO Account(RIB, date_opened, balance, account_type, customer_id ) VALUES ("{7}", "{8}", "{9}", "{10}","{11}" )'.format(RIB,date_open, balance, account_type, customer_id)
  mycursor.execute(sql)

def create_credit(date, duration, amount, credit_type,  account_id , external_account_id, transacion_type):
  sql = 'INSERT INTO Customers(date, duration, amount, credit_type, account_id) VALUES ("{0}","{1}", "{2}", "{3}", "{4}")'.format(date, duration, amount, credit_type, account_id)
  mycursor.execute(sql)
  sql = 'INSERT INTO Transactions(date, amount_of_transaction, transaction_type, account_id, external_account_id) VALUES ("{0}","{1}", "{2}", "{3}", "{4}")'.format(date, amount, transacion_type, account_id, external_account_id)
  mycursor.execute(sql)
  sql = 'SELECT balance from Account where id='+account_id
  bal = mycursor.execute(sql)+amount
  sql = 'UPDATE Account set balance='+bal+' where id='+account_id
  mycursor.execute(sql)

def show_balance(account_id):
  sql = 'SELECT balance from Account where id='+account_id
  bal = mycursor.execute(sql)
  return bal

def check_earnings(account_id):
  sql = 'SELECT date , amount_of_transaction , transaction_type , full_name from Transactions T , Customer C , Account A where T.account_id='+account_id+'and A.id=T.external_account_id and C.id = A.customer_id LIMIt 5'
  tran = mycursor.execute(sql)
  return tran

def verif_transfer_info(fullname,rib):
  sql = 'SELECT full_name , RIB from Customers C , Account A where C.fullname='+fullname+' and A.RIB='+rib+' and C.id=A.customer_id'
  a = mycursor.execute(sql)
  return a

def transfer_money(rib , amount, account_id):
  sql = 'SELECT balance from Account where id='+account_id
  bal = mycursor.execute(sql)-amount
  sql = 'UPDATE Account set balance='+bal+' where id='+account_id
  mycursor.execute(sql)
  sql = 'SELECT balance from Account where RIB='+rib
  bal = mycursor.execute(sql)+amount
  sql = 'UPDATE Account set balance='+bal+' where RIB='+rib
  mycursor.execute(sql)

def close_account(date_close, account_id):
  sql = 'Update Account set date_closed='+date_close+' where id='+account_id
  mycursor.execute(sql)

def verif_amount(amount,account_id):
  sql= 'SELECT balance from account where id='+account_id
  bal=mycursor.execute(sql)
  if(amount>bal):
    return 0
  else:
    return 1
  
def create_complaint(desc, rib, ref):
  sql = 'INSERT INTO Reclamations(description, rib, ref_code) VALUES ("{0}","{1}", "{2}")'.format(desc, rib, ref)
  mycursor.execute(sql)

def verif_rib(rib):
  sql = 'SELECT RIB From Account where RIB='+rib
  r = mycursor.execute(sql) 
  return r

def complaint_status(rib):
  sql = 'SELECT status FROM Reclamations where rib='+rib
  stat = mycursor.execute(sql)
  return stat

def cheque_request(num_demande, account_id):
  sql = 'INSERT INTO Cheque(demande, account_id) VALUES ("{0}","{1}")'.format(num_demande, account_id)
  mycursor.execute(sql)

def cheque_request_status(request_num):
  sql = 'SELECT etat FROM Cheque where demande='+request_num
  a = mycursor.execute(sql)
  return a.fetchall()



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()