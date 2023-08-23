from bs4 import BeautifulSoup
import firebase_admin
import requests
from firebase_admin import credentials, db
import re
from config import username, password, login_url

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fenixbot-isutc-default-rtdb.firebaseio.com/'
})
cadeiras_ref = db.reference('files/cadeiras')
session = requests.Session()


def extract_hidden_lt(text):
    pattern = r'<input type="hidden" name="lt" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


# def encontrar_estudante(html, numero_estudante):
#     soup = BeautifulSoup(html, 'html.parser')
#     tabelas = soup.find_all('table')  # Encontra todas as tabelas no código HTML
#     linha_encontrada = None
#     primeira_linha_tabela = None
#     ultima_linha_tabela = None
#
#     for tabela in tabelas:
#         linhas = tabela.find_all('tr')  # Encontra todas as linhas (tr) na tabela
#         for i, linha in enumerate(linhas):
#             celulas = linha.find_all(['td', 'th'])  # Encontra todas as células (td/th) na linha
#             primeira_celula = celulas[0] if celulas else None  # Obtém a primeira célula da linha
#             if primeira_celula and numero_estudante in primeira_celula.text:
#                 linha_encontrada = [celula.text.strip() for celula in
#                                     celulas]  # Obtém o texto de todas as células da linha
#             if i == 0:
#                 primeira_linha_tabela = [celula.text.strip() for celula in
#                                          celulas]  # Obtém o texto de todas as células da primeira linha
#             ultima_linha_tabela = [celula.text.strip() for celula in
#                                    celulas]  # Obtém o texto de todas as células da última linha
#
#     if linha_encontrada:
#         return True, linha_encontrada, primeira_linha_tabela, ultima_linha_tabela
#     else:
#         return False, [], [], []

def encontrar_estudante(link, numero_estudante):
    s = requests.Session()

    request = s.get(login_url)
    lt = extract_hidden_lt(request.text)
    print(lt)

    payload = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'submit': 'ENTRAR'
    }


    r = s.post(login_url, data=payload)

    response = ''
    if r.status_code == 200:
        descricao = []
        estudante = []
        total = []
        response = s.get(link).text
        soup = BeautifulSoup(response, 'html.parser')

        tables = soup.find_all('table', class_='tab_complex')



        for table in tables:
            td = table.find('td', text=lambda text: text and text.strip() == '6108')
            print(td.text)
            if td:
                tr = td.find_parent('tr')
                tds = tr.find_all('td')
                for td in tds:
                    estudante.append(td.text.strip())
                table = tr.find_parent('table')
                ths = table.find_all('th')
                for th in ths:
                    descricao.append(th.text.strip())
                trs = table.find_all('tr')
                last_tr = trs[-1]
                tds = last_tr.find_all('td')
                for td in tds:
                    total.append(td.text.strip())
                result = ''
                for i in range(0, len(estudante)):
                    if i<2:
                        result = result + descricao[i] + ': ' + estudante[i] + '\n'
                    elif i>=2:
                        result = result + descricao[i] + ': ' + estudante[i] +'/'+ total[i-1]+'\n'


                return result




    return 'Estudante não encontrado'


# e = encontrar_estudante(
#     'https://fenix.isutc.ac.mz/isutc/publico/executionCourse.do?method=marks&executionCourseID=281887293571686', '6108')
# print(e)