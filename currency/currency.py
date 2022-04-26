
import requests
import json
from pprint import pprint




def getJsonData (fileName, key) :
    file = open(fileName)
    data=json. load (file)
    return data[key]


apiFile=open('currency\currencies.json')

data=json.load(apiFile)
# 7dbb21c2210255c334f248e945f51ce0

#api_key=data['API_KEY']

url ="http://data.fixer.io/api/latest?access_key=" +'7dbb21c2210255c334f248e945f51ce0'

dataURL= requests. get (url) . text
dataJson = json. loads (dataURL)
currencies=dataJson
dataRates=currencies['rates']
def currencyConversion (amnt,frm,to) :
    #query =input ("Show Currency (y/n") . upper()
    #if query == "Y" :
    #    pprint(currencies)

    amount =amnt
    fromCurrency =frm
    toCurrency =to
    convertedAmount = round( amount * dataRates[toCurrency]/dataRates [fromCurrency ],2)
    msg=""+str(amount)+" "+str(fromCurrency)+" = "+str(convertedAmount)+" "+str(toCurrency)
    print(f"{amount} {fromCurrency} = {convertedAmount} {toCurrency}")
    return msg
#try:
#    currencyConversion ()
#except :
#    print ("You Entered wrong input")
#    currencyConversion


