import requests
import json


def currencyConversion (amnt,frm,to) :
    url = "https://api.apilayer.com/fixer/convert?to="+to+"&from="+frm+"&amount="+str(amnt)

    payload = {}
    headers= {
    "apikey": "VqBUH1rRODlZmeaXB7dAbMNitlyC5kah"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text

    convertedAmount = json.loads (result)
    msg=""+str(amnt)+" "+str(frm)+" = "+str(convertedAmount['result'])+" "+str(to)
    return msg