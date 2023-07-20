from config import *
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

    global status


    if status == 'null':
        send(main_menu.print_prompt(), number)
        status = main_menu.name
        return jsonify({'message': 'Success'})
    if status == 'main_menu':
        if message in main_menu.range:
            if message=='1':
                send(menu_cursos.print_prompt(), number)
                status = menu_cursos.name
                return jsonify({'message': 'Success'})
            if message=='2':
                send('Estamos trabalhando nisso', number)
                return jsonify({'message': 'Success'})
        else:
            send('Opção inválida, tente outra vez', number)
            send(main_menu.print_prompt(), number)
            return jsonify({'message': 'Success'})
    if status == 'menu_cursos':
        if message in menu_cursos.range:
            global curso_filtro
            curso_filtro = menu_cursos.select_data(message)
            status = menu_cursos.get_name()
            send('selecionou o curso '+curso_filtro+'\n'+menu_ano.print_prompt(), number)
            return jsonify({'message': 'Success'})
        else:
            send('Opção inválida, tente outra vez', number)
            return jsonify({'message': 'Success'})











if __name__ == "__main__":
    app.run()
