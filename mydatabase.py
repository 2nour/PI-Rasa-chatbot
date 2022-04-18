import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             port=3306,
                             password='',
                             database="rasadatabase")
mycursor = connection.cursor()
#mycursor.execute("CREATE TABLE Customers (id int AUTO_INCREMENT PRIMARY KEY, full_name VARCHAR(255) , cin int(8) , email varchar(255)  , birthdate DATETIME , phone_number int ,address VARCHAR(255) , login VARCHAR(255), password varchar(255) NOT NULL)")
#mycursor.execute("CREATE TABLE Account (id int AUTO_INCREMENT PRIMARY KEY,  date_opened DATETIME NOT NULL , date_closed DATETIME , balance float NOT NULL , account_type varchar(255) NOT NULL  , customer_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (customer_id) REFERENCES Customers(id) )")
#mycursor.execute("CREATE TABLE Credit (id int AUTO_INCREMENT PRIMARY KEY,  date DATE NOT NULL , duration int  NOT NULL , ammount float NOT NULL , credit_type varchar(255) NOT NULL  , account_id int NOT NULL , CONSTRAINT FK FOREIGN KEY (account_id) REFERENCES  Account(id))")
#mycursor.execute("CREATE TABLE Credit_card (id int AUTO_INCREMENT PRIMARY KEY, credit_card_number int NOT NULL , date_exp date NOT NULL , cvv int NOT NULL , pin_code int NOT NULL , account_id int NOT NULL , constraint FK FOREIGN KEY  (account_id) REFERENCES Account(id))")
#mycursor.execute("CREATE TABLE TRANSACTION (id int AUTO_INCREMENT PRIMARY KEY, date DATETIME NOT NULL , amount_of_transaction float NOT NULL , transaction_type binary NOT NULL , account_id_s int NOT NULL , account_id_r int NOT NULL ,constraint FK FOREIGN KEY  (account_id_s) REFERENCES Account(id), constraint FK1 FOREIGN KEY  (account_id_r) references  Account(id))" )
def create_account(fullname, cin, email, birthdate, number, address, login, password ):
  sql = 'INSERT INTO customers(full_name, cin, email, birthdate, phone_number, address, login ,password) VALUES ("{0}","{1}", "{2}", "{3}", "{4}", "{5}" , "{6}" )'.format(fullname, cin, email, birthdate, number,  address, login, password)
  mycursor.execute(sql)
     