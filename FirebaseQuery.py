import firebase_admin
from firebase_admin import credentials, db
from Cadeiras import Cadeiras

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fenixbot-isutc-default-rtdb.firebaseio.com/'
})
cadeiras_ref = db.reference('files/cadeiras')


def cadeiras_query(curso, ano, semestre):


    # Consultar dados onde "ano acadêmico", "semestre" e "curso" correspondem aos valores desejados
    snapshot = (cadeiras_ref
                .order_by_child('ano')
                .equal_to(ano)
                .get())

    # Filtrar os dados pelo semestre e curso e criar objetos da classe Cadeiras
    nomesq = []
    for key, val in snapshot.items():
        if val.get('semestre') == semestre and val.get('curso') == curso:
            cadeira_obj = Cadeiras(nome=val.get('nome'),
                                   sigla=key,
                                   ano=val.get('ano'),
                                   curso=val.get('curso'),
                                   semestre=val.get('semestre'),
                                   link=val.get('link'))
            nomesq.append(cadeira_obj)

    return nomesq


def siglas_query(curso, cadeira, semestre):
    cadeiras_ref = db.reference('files/cadeiras')

    # Consultar dados onde "curso", "cadeira" e "semestre" correspondem aos valores desejados
    snapshot = (cadeiras_ref
                .order_by_child('curso')
                .equal_to(curso)
                .get())

    # Filtrar os dados pela cadeira e semestre e criar objetos da classe Cadeiras
    cadeiras_encontradas = []
    for key, val in snapshot.items():
        if cadeira.lower() in val.get('nome').lower() and val.get('semestre') == semestre:
            cadeira_obj = Cadeiras(nome=val.get('nome'),
                                   sigla=key,
                                   ano=val.get('ano'),
                                   curso=val.get('curso'),
                                   semestre=val.get('semestre'),
                                   link=val.get('link'))
            cadeiras_encontradas.append(cadeira_obj)
    # Criar uma lista de siglas a partir dos objetos Cadeiras
    siglas_encontradas = [cadeira.sigla for cadeira in cadeiras_encontradas]
    nome_das_cadeiras = [cadeira.nome for cadeira in cadeiras_encontradas]

    ans = ''
    for i in range(0, len(siglas_encontradas)):
        ans = nome_das_cadeiras[i]+': '+siglas_encontradas[i]+'\n'

    if len(siglas_encontradas)==0:
        ans = 'Nenhum resultado encontrado 😞'
    return ans


def link_query(key):
    cadeiras_ref = db.reference('files/cadeiras')

    link = 'none'

    # Consultar dados onde a chave corresponde à chave fornecida
    snapshot = (cadeiras_ref
                .order_by_key()
                .equal_to(key)
                .get())

    # Se a chave estiver no snapshot, obtenha o link correspondente
    if snapshot:
        link = snapshot[key].get('link')

    return link



link = link_query('ACEL')
print(link)

