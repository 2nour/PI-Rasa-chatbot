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

#mycursor.execute("CREATE TABLE Customers (id int AUTO_INCREMENT PRIMARY KEY, full_name VARCHAR(255) , cin VARCHAR(255) , email varchar(255)  , birthdate DATETIME , phone_number varchar(255) ,address VARCHAR(255) ,login VARCHAR(255) NOT NULL, password varchar(255) NOT NULL)")
#mycursor.execute("CREATE TABLE Account (id int AUTO_INCREMENT PRIMARY KEY, RIB int(16) NOT NULL,  date_opened DATETIME NOT NULL , date_closed DATETIME , balance float NOT NULL , account_type varchar(255) NOT NULL , customer_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (customer_id) REFERENCES Customers(id) )")
#mycursor.execute("CREATE TABLE Credit (id int AUTO_INCREMENT PRIMARY KEY,  date DATE NOT NULL , duration int  NOT NULL , ammount float NOT NULL , credit_type varchar(255) NOT NULL  , account_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (account_id) REFERENCES  Account(id))")
#mycursor.execute("CREATE TABLE Credit_card (id int AUTO_INCREMENT PRIMARY KEY, credit_card_number int NOT NULL , date_exp date NOT NULL , cvv int NOT NULL , pin_code int NOT NULL , account_id int NOT NULL , constraint FK FOREIGN KEY  (account_id) REFERENCES Account(id))")
#mycursor.execute("CREATE TABLE Transactions (id int AUTO_INCREMENT PRIMARY KEY, date DATETIME NOT NULL , amount_of_transaction float NOT NULL , transaction_type varchar(255) NOT NULL , account_id int NOT NULL , external_account_id int NOT NULL ,constraint FK FOREIGN KEY  (account_id) REFERENCES Account(id), constraint FK1 FOREIGN KEY  (account_id) references  Account(id))" )
#mycursor.execute("CREATE TABLE Reclamation(id int AUTO_INCREMENT PRIMARY KEY, description varchar(255) NOT NULL , rib int(16) NOT NULL , status varchar(255) DEFAULT 'In progress' , ref_code int NOT NULL)")
#mycursor.execute("CREATE TABLE Cheque(id int AUTO_INCREMENT PRIMARY KEY, demande int NOT NULL , etat varchar(255) DEFAULT 'In progress' , account_id int NOT NULL, constraint FK FOREIGN KEY (account_id) REFERENCES Account(id))")
#mycursor.execute("CREATE TABLE Connexion(id int AUTO_INCREMENT PRIMARY KEY, id_account int NOT NULL )")



def verif_cin(cin):
  a= mycursor.execute('SELECT cin from Customers where cin='+str(cin))
  return a

def verif_login(login):
  mycursor.execute("SELECT login from Customers where login = '"+login+"'")
  return len(list(mycursor))

def verif_rib_name(rib):
  mycursor.execute("Select full_name From Customers C , Account A where C.id = A.customer_id and A.rib = "+str(rib))
  return mycursor.fetchall()[0][0]


def verif_mail(mail):
  a = mycursor.execute("SELECT email from Customers where email = '"+mail+"'")
  return a

def get_rib():
  mycursor.execute('SELECT RIB from Account   ORDER BY id DESC LIMIT 1')
  return mycursor.fetchall()[0][0]

def create_account(fullname, cin, email, birthdate, phone_number, address, login, password ,RIB, date_open, balance, account_type):
  
  sql = "INSERT INTO Customers(full_name, cin, email, birthdate, phone_number, address, login ,password) VALUES ('"+fullname+"',"+"'"+cin+"',"+"'"+email+"',"+"'"+birthdate+"',"+str(phone_number)+","+"'"+address+"',"+"'"+login+"',"+"'"+password+"')"
  mycursor.execute(sql)
  sql= 'SELECT id FROM Customers  ORDER BY id DESC LIMIT 1'
  mycursor.execute(sql)
  customer_id=mycursor.fetchall()[0][0]
  sql= 'SELECT id FROM Account   ORDER BY id DESC LIMIT 1'
  mycursor.execute(sql)
  id=mycursor.fetchall()[0][0]+1
  sql = "INSERT INTO Account VALUES ("+str(id)+","+str(RIB)+","+"'"+date_open+"',NULL,"+str(balance)+",'" +account_type+"','"+str(customer_id)+"')"
  mycursor.execute(sql)

create_account('amine amine' , '01234567' , 'email@email.com','1999-10-10' , 20123123, 'TN TN ' , 'az123','123123',1231231,'2022-04-30',0.0,'current')

def create_credit(date, duration, amount, credit_type,  account_id , external_account_id, transacion_type):
  sql = 'INSERT INTO Credit(date, duration, ammount, credit_type, account_id) VALUES ("{0}","{1}", "{2}", "{3}", "{4}")'.format(date, duration, amount, credit_type, account_id)
  mycursor.execute(sql)
  sql = 'INSERT INTO Transactions(date, amount_of_transaction, transaction_type, account_id, external_account_id) VALUES ("{0}","{1}", "{2}", "{3}", "{4}")'.format(date, amount, transacion_type, account_id, external_account_id)
  mycursor.execute(sql)
  sql = 'SELECT balance from Account where id='+str(account_id)
  mycursor.execute(sql)
  bal = int(mycursor.fetchall()[0][0])+amount
  sql = 'UPDATE Account set balance='+str(bal)+' where id='+str(account_id)
  mycursor.execute(sql)
  return 'Credit Transaction sent successfully'

#print(create_credit('2022-04-12', 5, 20000.0, 'car credit',  1 , 99999, 'debit'))


def show_balance(account_id):
  sql = 'SELECT balance from Account where id='+str(account_id)
  mycursor.execute(sql)
  return mycursor.fetchall()[0][0]


def check_earnings(account_id):
  sql = 'SELECT date , amount_of_transaction , transaction_type , full_name from Transactions T , Customer C , Account A where T.account_id='+account_id+'and A.id=T.external_account_id and C.id = A.customer_id LIMIt 5'
  tran = mycursor.execute(sql)
  return tran

#def verif_transfer_info(fullname,rib):
 # sql = 'SELECT full_name , RIB from Customers C , Account A where C.fullname='+fullname+' and A.RIB='+rib+' and C.id=A.customer_id'
  #a = mycursor.execute(sql)
  #return a

def transfer_money(rib , amount, account_id):
    sql = 'SELECT balance from Account where id='+str(account_id)
    mycursor.execute(sql)
    bal = int(mycursor.fetchall()[0][0])-amount
    sql = 'UPDATE Account set balance='+str(bal)+' where id='+str(account_id)
    mycursor.execute(sql)
    sql = 'SELECT balance from Account where RIB='+str(rib)
    mycursor.execute(sql)
    bal2 = int(mycursor.fetchall()[0][0])+amount
    sql = 'UPDATE Account set balance='+str(bal2)+' where RIB='+str(rib)
    mycursor.execute(sql)
    print(bal,bal2)
    return 'money sent successfully'



#print(transfer_money('hedy ezine',888555660,50,1))



def close_account(date_close, account_id):
  sql = 'Update Account set date_closed='+str(date_close)+' where id='+str(account_id)
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
  mycursor.execute(sql)
  return mycursor.fetchall()[0]

def cheque_request(num_demande, account_id):
  sql = 'INSERT INTO Cheque(demande, account_id) VALUES ("{0}","{1}")'.format(num_demande, account_id)
  mycursor.execute(sql)

def cheque_request_status(request_num):
  sql = 'SELECT etat FROM Cheque where demande='+request_num
  a = mycursor.execute(sql)
  return a.fetchall()



def similar(a, b):
    return SequenceMatcher(None, a, b).rat()

def sign_in(login , password):
  b = False
  if (login):
    a = mycursor.execute("Select login from Customers where login ='"+login+"'")
    if (a != 0):
        mycursor.execute("Select password from Customers where login ='"+login+"'")
        c = mycursor.fetchall()[0][0]
        if (c == password ):
          b = True
  return b

def get_account_id(login, password):
   if (sign_in(login, password) == 1):
      a= mycursor.execute("Select A.id from Account A, Customers C where A.customer_id=C.id and login ='"+login+"'")
      if(a):
        return mycursor.fetchall()[0][0]    
      else :
        return "None"

def getMailBy_RIB(rib):
  mycursor.execute("Select email from Account A, Customers C where A.customer_id=C.id and rib ="+str(rib))
  return mycursor.fetchall()[0][0]
def getMail_by_AccountId(account_id):
    mycursor.execute("Select email from Account A, Customers C where A.customer_id=C.id and A.id ="+str(account_id))
    return mycursor.fetchall()[0][0] 

def logout():
    mycursor.execute("TRUNCATE TABLE Connexion")


def getConnectionid():
    a= mycursor.execute("SELECT account_id from Connexion ")
    if(a>0) :
      return mycursor.fetchall()[0][0]
    else :
      return None

mycursor.execute("TRUNCATE TABLE Connexion")