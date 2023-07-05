from config import *
from searchBot import getNotas as getNotas
from twilio.rest import Client
from flask import Flask, request, jsonify


def fill(string):
    if str(string).startswith('whatsapp:'):
        return string
    else:
        return 'whatsapp:' + str(string)


def format_answer(primeira_linha, linhas_encontradas, ultima_linha):
    ans = []
    for i in range(0, len(linhas_encontradas)):
        if i >= 2:
            text = linhas_encontradas[i] + ': ' + primeira_linha[i] + '/' + ultima_linha[i - 1]
            ans.append(text)
        if i < 2:
            text = linhas_encontradas[i] + ': ' + primeira_linha[i]
            ans.append(text)

    text = ""
    for i in ans:
        text = text + i + '\n'
    return text


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
    message = request.values.get('Body', '')

    # send('Comando recebido, buscando notas', number)
    keys = message.split('/')
    if len(keys) != 3:
        send(invalid_comand_error, number)
    else:
        send(f'procurando notas de {keys[2]} da cadeira {keys[1]}', number)
        primeira_linha, linhas_encontradas, ultima_linha = getNotas(keys[0], keys[1], keys[2])

        answer = format_answer(primeira_linha, linhas_encontradas, ultima_linha)
        send(answer, number)

    return jsonify({'message': 'Success'})


if __name__ == "__main__":
    app.run()
