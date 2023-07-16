import config
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

dados_curso = ''
dados_ano: str
dados_semestre: str
dados_cadeira: str







@app.route('/', methods=['POST'])
def bot():
    number = request.form.get('From')
    message = request.values.get('Body', '')


    if config.state == 'blank':
        send(config.main_menu.to_string(), number)
    if config.state == config.states[0]:
        if message in config.main_menu.range:
            if message == '1':
                send(config.menu_curso.to_string(), number)
                config.state = config.menu_curso.estado
                print(config.state)
            else:
                send('Estamo a trabalhar no Sobre', number)
        else:
            send('Opção inválida', number)
            send(config.main_menu.to_string(), number)
    elif config.state == config.states[1]:
        if message in config.menu_curso.range:
            crs = config.menu_curso.options[int(message)]
            extrair_cursos(crs)
            config.state = config.menu_ano.estado
            send(config.menu_ano.to_string(), number)
        else:
            send('Opção inválida', number)
            send(config.menu_curso.to_string(), number)
    elif config.state == config.states[2]:
        if message in config.menu_curso.range:
            ano = config.menu_ano.options[int(message)]
            extrair_ano(ano)
            config.state = config.menu_semestre.estado
            send(config.menu_semestre.to_string(), number)
        else:
            send('Opção inválida', number)
            send(config.menu_ano.to_string(), number)
    elif config.state == config.states[3]:
        if message in config.menu_semestre.range:
            sem = config.menu_semestre.options[int(message)]
            extrair_semestre(sem)
            config.state = config.menu_cadeiras.estado
            send(config.menu_cadeiras.to_string(), number)
        else:
            send('Opção inválida', number)
            send(config.menu_semestre.to_string(), number)
    elif config.state == config.states[4]:
        if message in config.menu_cadeiras.range:
            cad = config.menu_cadeiras.options[int(message)]
            extrair_semestre(cad)
            config.state = config.menu_cadeiras.estado
            send(config.menu_cadeiras.to_string(), number)
        else:
            send('Opção inválida', number)
            send(config.menu_semestre.to_string(), number)

    return jsonify({'message': 'Success'})









if __name__ == "__main__":
    app.run()
