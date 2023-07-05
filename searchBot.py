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
        filtro = df['sigla da cadeira'] == sigla
        linha = df.loc[filtro].index[0]
        coluna = df.columns.get_loc('sigla da cadeira') + 1
        valor = df.iloc[linha, coluna]
        return valor
    except IndexError:
        return None
    except FileNotFoundError:
        return None


def getNotas(curso, cadeira, nr):
    print('==BOT STARTED==')
    print(str(curso)+' '+str(cadeira))
    html = search.main(login_url, obter_link(curso, cadeira))
    b, primeira_linha, linhas_encontradas, ultima_linha = encontrar_estudante(html, nr)
    return primeira_linha, linhas_encontradas, ultima_linha
























