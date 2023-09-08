from config import *
from payment import pay
from twilio.rest import Client
from flask import Flask, request, jsonify
import pandas as pd
import FirebaseQuery as fbq
from WebScrapper import encontrar_estudante
from FeedBack import register_feedback

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

def get_command(texto):
    indice_dois_pontos = texto.find(':')
    if indice_dois_pontos != -1:
        return texto[indice_dois_pontos + 1:].strip()
    return ""




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

def report(message, number):
    send(f'''
    from: {number};
    description: {message}
    ''', 'whatsapp:+258869469505')
    send(f'''
    from: {number};
    description: {message}
    ''', 'whatsapp:+258844236139')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    number = request.form.get('From')

    message = request.values.get('Body', '')



    # send('Comando recebido, buscando notas', number)
    if message.lower().startswith('comandos'):
        send(comands_tutorial, number)
    elif message.lower().strip().startswith('notas:'):
        command = get_command(message)
        keys = command.split('/')
        answer = ''
        send(f'procurando notas de {keys[1]} da cadeira {keys[0]}', number)
        link = fbq.link_query(keys[0])
        if link =='none':
            answer = 'Nenhum resultado encontrado 😞. Sigla da cadeira não encontrada'
            send(answer, number)
        else:
            answer = encontrar_estudante(link, keys[1])
            send(answer, number)



    elif message.strip().lower().startswith('sigla:'):
        command = get_command(message)
        keys = command.split('/')
        send(f'procurando as siglas de {keys[1]} do semestre {keys[2]}', number)
        answer = fbq.siglas_query(keys[0], keys[1])
        send(answer, number)
    elif message.lower().startswith('pagar'):
        command = get_command(message)
        keys = command.split('/')
        send("Aguarde, irá receber uma notificação para completar o pagamento", number)
        res, data = pay('258'+keys[0], keys[1], keys[2])
        send(res, number)

    elif message.lower().startswith('feedback'):
        command = get_command(message)
        register_feedback(command, number)
        report(command, number)
        send('O seu feedback foi registado! Agradecemos pela sua contribuição\nSe houver a acrescentar não hesite!', number)
    else:
        send(invalid_command_error, number)

    return jsonify({'message': 'Success'})


if __name__ == "__main__":
    app.run()
