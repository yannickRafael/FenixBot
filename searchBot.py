import getMarksBot as search
from config import login_url
import pandas as pd
from bs4 import BeautifulSoup


def encontrar_estudante(html, numero_estudante):
    soup = BeautifulSoup(html, 'html.parser')
    tabelas = soup.find_all('table')  # Encontra todas as tabelas no código HTML
    linha_encontrada = None
    primeira_linha_tabela = None
    ultima_linha_tabela = None

    for tabela in tabelas:
        linhas = tabela.find_all('tr')  # Encontra todas as linhas (tr) na tabela
        for i, linha in enumerate(linhas):
            celulas = linha.find_all(['td', 'th'])  # Encontra todas as células (td/th) na linha
            primeira_celula = celulas[0] if celulas else None  # Obtém a primeira célula da linha
            if primeira_celula and numero_estudante in primeira_celula.text:
                linha_encontrada = [celula.text.strip() for celula in
                                    celulas]  # Obtém o texto de todas as células da linha
            if i == 0:
                primeira_linha_tabela = [celula.text.strip() for celula in
                                         celulas]  # Obtém o texto de todas as células da primeira linha
            ultima_linha_tabela = [celula.text.strip() for celula in
                                   celulas]  # Obtém o texto de todas as células da última linha

    if linha_encontrada:
        return True, linha_encontrada, primeira_linha_tabela, ultima_linha_tabela
    else:
        return False, [], [], []


def obter_link(sigla):
    try:
        df = pd.read_excel('cadeiras.xlsx')
        filtro = df['sigla'] == sigla
        # filtro = (df['cadeira'].str.contains(sigla))
        linha = df.loc[filtro].index[0]
        coluna = df.columns.get_loc('sigla') + 1
        valor = df.iloc[linha, coluna]
        retorno = 'https://fenix.isutc.ac.mz' + str(valor)
        return retorno
    except IndexError:
        return None
    except FileNotFoundError:
        return None


def obter_sigla(curso, cadeira, semestre):
    try:
        semestre = int(semestre)
        df = pd.read_excel('cadeiras.xlsx')
        filtro = (df['semestre'] == semestre) & (df['curso'].str.lower() == curso.lower()) & (df['nome'].str.contains(cadeira, case=False))
        linha = df.loc[filtro]

        print(len(linha))

        nomes = []
        siglas = []

        for i in range(0, len(linha)):
            coluna_nome = int(df.columns.get_loc('nome'))
            coluna_sigla = int(df.columns.get_loc('sigla'))
            nome = df.iloc[linha.index[i], coluna_nome]
            sigla = df.iloc[linha.index[i], coluna_sigla]
            nomes.append(nome)
            siglas.append(sigla)

        txt = ''
        for i in range(0, len(siglas)):
            txt = txt + nomes[i] + ': ' + siglas[i]+'\n'
        return txt

    except IndexError:
        return None
    except FileNotFoundError:
        return None


def getNotas(cadeira, nr):
    print('==BOT STARTED==')
    html = search.main(login_url, obter_link(cadeira))
    b, primeira_linha, linhas_encontradas, ultima_linha = encontrar_estudante(html, nr)
    return primeira_linha, linhas_encontradas, ultima_linha


# message = 'lecc/Artificial/1'
# keys = message.split('/')
# print(obter_sigla(keys[0], keys[1], keys[2]))
