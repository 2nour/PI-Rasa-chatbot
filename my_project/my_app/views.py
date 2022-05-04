from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pyparsing import empty
from rest_framework.response import Response
import pymysql,jwt,datetime
from .models import Customers as cutomer
# Create your views here.

def index(request):
    return render(request, "chatroom.html")

response = Response()


def loginView(request):
    if request.method=="POST":
        con = pymysql.connect(host="localhost",port=3308, user="root",password="",database="rasadatabase")
        cursor = con.cursor()
        
        login =''
        password=''
        cutomerr= cutomer
        d= request.POST
        for key,value in d.items():
            if key=='login':
                login = value
            if key =='password':
                password = value
        
        sql1= "select * from customers where login='{}' and password='{}' ".format(login,password)
        cursor.execute(sql1)
        #t = tuple(cursor.fetchall())
        #t= cutomer.objects.filter(login=login).first()
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("id: ", row[0])
            print("fullname: ", row[1])
            print("Email: ", row[2])
            print("Salary: ", row[3])
            cutomerr =row
            print("\n")

        if records==():
            return render(request,'registration/login.html') 
        else :
            payload = {
                    'id': cutomerr[0],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                   
                   
                }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                    'jwt': token,
                   'id': cutomerr[0]
                    }
            
        
            print(response.data)
        
            request.session["id"]= cutomerr[0]
            sqql= 'insert into connexion(account_id) values("{}")'.format(request.session["id"])
            cursor.execute(sqql)
            print(request.session["id"])
            return render(request,"chatroom.html")
            
    return render(request,'registration/login.html')
