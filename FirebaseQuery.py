from config import cadeiras_ref
from Cadeiras import Cadeiras
import unidecode


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


def siglas_query(curso, cadeira):
    # Consultar dados onde "curso", "cadeira" e "semestre" correspondem aos valores desejados
    snapshot = (cadeiras_ref
                .order_by_child('curso')
                .equal_to(curso)
                .get())

    # Filtrar os dados pela cadeira e semestre e criar objetos da classe Cadeiras
    cadeiras_encontradas = []
    for key, val in snapshot.items():
        name  = unidecode.unidecode(val.get('nome').lower())
        cadeira = unidecode.unidecode(cadeira.lower())
        print(f'Compare: {cadeira} in {name} is {cadeira in name}')
        if cadeira in name:
            cadeira_obj = Cadeiras(nome=val.get('nome'),
                                   sigla=key,
                                   ano=val.get('ano'),
                                   curso=val.get('curso'),
                                   semestre=val.get('semestre'),
                                   link=val.get('link'))
            cadeiras_encontradas.append(cadeira_obj)
    # Criar uma lista de siglas a partir dos objetos Cadeiras
    print(f'Quantidade: {len(cadeiras_encontradas)}')
    siglas_encontradas = []
    nome_das_cadeiras =[]
    for i in cadeiras_encontradas:
        siglas_encontradas.append(i.sigla)
        nome_das_cadeiras.append(i.nome)

    print(f'Quantidade: {len(nome_das_cadeiras)}')
    print(f'Quantidade: {len(siglas_encontradas)}')




    ans = ''
    n = len(siglas_encontradas)
    if len(siglas_encontradas) == 0:
        ans = 'Nenhum resultado encontrado 😞'
    else:
        for i in range(0, n):
            ans = ans + nome_das_cadeiras[i] + ': ' + siglas_encontradas[i] + '\n'
    return ans


def link_query(key):
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
