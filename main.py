from config import *
from searchBot import getNotas as getNotas
from searchBot import obter_sigla as obter_sigla
from twilio.rest import Client
from flask import Flask, request, jsonify
import pandas as pd


def buscar_cursos_por_semestre(curso, semestre):
    # Ler o arquivo Excel
    dados = pd.read_excel('cadeiras.xlsx')

    # Filtrar as linhas que correspondem ao curso e semestre
    filtro = (dados['curso'] == curso) & (dados['semestre'] == semestre)
    cursos_encontrados = dados.loc[filtro]
    print(cursos_encontrados)

    # Verificar se foram encontrados cursos
    if cursos_encontrados.empty:
        return None, None

    # Retornar as listas com nomes e siglas
    nomes = cursos_encontrados['cadeira'].tolist()
    siglas = cursos_encontrados['sigla da cadeira'].tolist()

    return nomes, siglas


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
    if len(keys) == 2:
        send(f'procurando notas de {keys[1]} da cadeira {keys[0]}', number)
        primeira_linha, linhas_encontradas, ultima_linha = getNotas(keys[0], keys[1])
        answer = format_answer(primeira_linha, linhas_encontradas, ultima_linha)
        send(answer, number)
    elif len(keys)==3:
        if (keys[2] == '1')| (keys[2]=='2') :
            send(f'procurando as siglas de {keys[1]} do semestre {keys[2]}', number)
            answer = obter_sigla(keys[0], keys[1], keys[2])
            send(answer, number)
        else:
            send(invalid_semester_error, number)
    else:
        send(invalid_comand_error, number)



    return jsonify({'message': 'Success'})


if __name__ == "__main__":
    app.run()
