from re import fullmatch

from numpy import full
from pdf.create_table_fpdf2 import PDF
#from database_connectivity import *
import pymysql

def extrait():
    mydatabase =  pymysql.connect(host="localhost", port=3308, user="root", passwd="", database="rasadatabase")
    #mydatabase =  pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", database="rasadatabase")


    mycursor = mydatabase.cursor()

    data = [
        ["date", "amount of transaction	", "transaction type", "external account",], # 'testing','size'],
    ]
    mycursor.execute('SELECT * from transactions where account_id=1')


    pdf = PDF() 
    pdf.add_page()
    # get total page numbers
    pdf.alias_nb_pages()


    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 15)
    pdf.set_font("Times", size=10)

    pdf.extrait_title()
    pdf.account_data()
    output = mycursor.fetchall()
    for x in output:
        lst=[]
        for i in range(1,6) :
            if(i!=4): 
                if(i==5):
                    mycursor.execute('SELECT full_name from account A, Customers C where A.customer_id=C.id and A.id = '+str(x[5]))
                    fullname=str(mycursor.fetchall())
                    #output1 = mycursor.fetchall()
                    print(fullname)
                    lst.append(fullname)
                    break; 
                lst.append(str(x[i]))
        data.append(lst)
    mycursor.execute('SELECT balance from account where account.id = 1')
    output1 = mycursor.fetchall()

    tt='Solde à ce jour sauf erreur ou omission  ' +str(output1[0][0])
    pdf.create_table(table_data = data,title= tt, cell_width='even')
    pdf.ln()


    pdf.output('extrait.pdf')