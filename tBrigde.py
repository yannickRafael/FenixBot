from config import auth_token, account_sid
from twilio.rest import Client
from flask import Flask, request, jsonify


def fill(string):
    if str(string).startswith('whatsapp:'):
        return string
    else:
        return 'whatsapp:' + str(string)


def send(message, number):
    client = Client(account_sid, auth_token)
    message = fill(message)
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=number
    )


app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    number = request.form.get('From')
    request.values.get('Body', '')
    send('Mensagem recebida!', number)
    send('Comando recebido, buscando notas', number)

    return jsonify({'message': 'Success'})


if __name__ == "__main__":
    app.run()
