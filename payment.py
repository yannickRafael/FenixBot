import requests
from datetime import datetime as dt
URL = 'http://127.0.0.1:3000/pay'




def pay(msisdn, reference, amount):
    payment_data = {
    "amount": amount,
    "msisdn": msisdn,
    "reference": reference,
    "third_party_reference": reference
    }
    response = requests.post(URL, json=payment_data)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            res = "Payment successful"
            return res, data
        else:
            res = "Payment failed"
            return res, data
    elif response.status_code == 204:
        data = ''
        res = '204 error'
        return res, data
    else:
        data = ' '
        res = "Request failed"
        return res, data
