from Menu import Menu
import pandas as pd

account_sid = 'ACa5c83e45677a24409033440f8499727b'
auth_token = 'c1b4fb1c0d36280276b9f8a0b6a68cf2'
invalid_comand_error = 'Comando não reconhecido\nFormato de comando:\n    [curso]/[cadeira]/[nr de estudante]'
username = 'yannick.matimbe'
password = 'Y@nnick2003'
login_url = 'https://fenix.isutc.ac.mz/cas/login?service=https://fenix.isutc.ac.mz/isutc/'
logged_url = 'https://fenix.isutc.ac.mz/isutc/fenixEduIndex.do'
mark_url = 'https://fenix.isutc.ac.mz/isutc/publico/executionCourse.do?method=marks&executionCourseID=1126312223704031'
cursos = ["lca", "lea", "lect", "lecc", "lemec", "leet", "lee", "lef", "leit", "lemt", "lgbs", "lgf"]
invalid_semester_error = 'Semestre inválido.'
states = ['main_menu', 'menu_cursos', 'menu_ano', 'menu_semestre', 'menu_cadeiras']

main_menu = Menu('Escolha uma operação: ', ['Cursos', 'Sobre'], 'main_menu')
menu_curso = Menu('Selecione o curso: ', cursos, 'menu_curso')
menu_ano = Menu('Selecione o ano: ', ['1º Ano', '2º Ano', '3º Ano', '4º Ano'], 'menu_ano')
menu_semestre = Menu('Selecione o semestre: ', ['1', '2'], 'menu_semestre')
menu_cadeiras = Menu('Selecione a cadeira: ', [], 'menu_cadeira')
prev_menu: Menu
state = 'blank'



def extrair_cursos(curso):
    # Ler o arquivo "cadeiras.xlsx" na sheet "main"
    df = pd.read_excel('cadeiras.xlsx', sheet_name='main')

    # Filtrar as linhas que correspondem ao curso
    filtro = df['curso'] == curso
    cadeiras_encontradas = df[filtro]

    # Verificar se foram encontrados cursos
    if cadeiras_encontradas.empty:
        return

    # Criar um novo DataFrame apenas com as linhas encontradas
    novo_df = pd.DataFrame(cadeiras_encontradas)

    # Salvar o novo DataFrame em um arquivo xlsx
    novo_df.to_excel('cadeiras_encontradas.xlsx', index=False)


def extrair_ano(ano):
    # Ler o arquivo "cadeiras.xlsx" na sheet "main"
    df = pd.read_excel('cadeiras_encontradas.xlsx', sheet_name='Sheet1')

    # Filtrar as linhas que correspondem ao curso
    filtro = df['ano'] == ano
    cadeiras_encontradas = df[filtro]

    # Verificar se foram encontrados cursos
    if cadeiras_encontradas.empty:
        return

    # Criar um novo DataFrame apenas com as linhas encontradas
    novo_df = pd.DataFrame(cadeiras_encontradas)

    # Salvar o novo DataFrame em um arquivo xlsx
    novo_df.to_excel('cadeiras_encontradas.xlsx', index=False)


def extrair_semestre(semestre):
    # Ler o arquivo "cadeiras.xlsx" na sheet "main"
    df = pd.read_excel('cadeiras_encontradas.xlsx', sheet_name='Sheet1')

    # Filtrar as linhas que correspondem ao curso
    filtro = df['semestre'] == semestre
    cadeiras_encontradas = df[filtro]

    # Verificar se foram encontrados cursos
    if cadeiras_encontradas.empty:
        return

    # Criar um novo DataFrame apenas com as linhas encontradas
    novo_df = pd.DataFrame(cadeiras_encontradas)

    # Salvar o novo DataFrame em um arquivo xlsx
    novo_df.to_excel('cadeiras_encontradas.xlsx', index=False)

