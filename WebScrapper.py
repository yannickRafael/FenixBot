from bs4 import BeautifulSoup
import requests
import re
from config import username, password, login_url, cadeiras_ref


session = requests.Session()


def extract_hidden_lt(text):
    pattern = r'<input type="hidden" name="lt" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def extract_hidden_execution(text):
    pattern = r'<input type="hidden" name="execution" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None



def encontrar_estudante(link, numero_estudante):
    s = requests.Session()

    request = s.get(login_url)
    lt = extract_hidden_lt(request.text)
    execution = extract_hidden_execution(request.text)
    print(lt)

    payload = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': 'LOGIN'
    }


    r = s.post(login_url, data=payload)

    response = ''
    if r.status_code == 200:
        descricao = []
        estudante = []
        total = []
        response = s.get(link).text
        print(link)
        print(response)
        soup = BeautifulSoup(response, 'html.parser')
        

        tables = soup.find_all('table', class_='tab_complex')
        



        for table in tables:
            td = table.find('td', text=lambda text: text and text.strip() == numero_estudante)
            
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


