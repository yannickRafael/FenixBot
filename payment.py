import requests
from config import recibos_ref
from datetime import datetime as dt
URL = 'http://127.0.0.1:3000/pay'

def format_ref(date):
    response = str(date).replace('-', '')
    response = str(response).replace(' ', '')
    response = str(response).replace(':', '')
    response = str(response).replace('.', '')

    return response




def pay(msisdn, reference, amount):
    third_party_reference = format_ref(dt.today())
    payment_data = {
    "amount": amount,
    "msisdn": msisdn,
    "reference": reference,
    "third_party_reference": third_party_reference
    }
    response = requests.post(URL, json=payment_data)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            res = "Payment successful"
            response_data = {
                'amount': amount,
                'msisdn': msisdn,
                'reference': reference,
                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                'status': res
            }
            recibos_ref.child(third_party_reference).set(data)
            return res, response_data
        else:
            res = "Payment failed"
            response_data = {
                'amount': amount,
                'msisdn': msisdn,
                'reference': reference,
                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                'status': res
            }
            recibos_ref.child(third_party_reference).set(data)
            return res, data
    else:
        data = ' '
        res = "Request failed"
        return res, data
