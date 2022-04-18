from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#from mydatabase import mycursor
import pymysql
from django.contrib import messages
from operator import itemgetter

# Create your views here.

def index(request):
    return render (request, "chatroom.html")

def loginView(request):
    if request.method=="POST":
        con = pymysql.connect(host="localhost", user="root",password="",database="rasadatabase")
        cursor = con.cursor()
        
        login =''
        password=''
        d= request.POST
        for key,value in d.items():
            if key=='login':
                login = value
            if key =='password':
                password = value
        
        sql1= "select * from customers where login='{}' and password='{}' ".format(login,password)
        cursor.execute(sql1)
        t = tuple(cursor.fetchall())
        if t==():
            return render(request,'registration/login.html') 
        else :
            print(t)
            return render(request,"chatroom.html")
    return render(request, 'registration/login.html')
    
   # res = list(map(itemgetter(0)))



   