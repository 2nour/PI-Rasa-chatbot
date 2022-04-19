from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import pymysql
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
            permission_classes = (IsAuthenticated,)
            print(permission_classes)
            return render(request,"chatroom.html")
    
   # res = list(map(itemgetter(0)))



   