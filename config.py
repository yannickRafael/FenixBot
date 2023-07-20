account_sid = 'ACa5c83e45677a24409033440f8499727b'
auth_token = 'c1b4fb1c0d36280276b9f8a0b6a68cf2'
invalid_command_error = "Comando não reconhecido\nDigite 'comandos' para entender mais sobre os comandos"

username = 'yannick.matimbe'
password = 'Y@nnick2003'
login_url = 'https://fenix.isutc.ac.mz/cas/login?service=https://fenix.isutc.ac.mz/isutc/'
logged_url = 'https://fenix.isutc.ac.mz/isutc/fenixEduIndex.do'
mark_url = 'https://fenix.isutc.ac.mz/isutc/publico/executionCourse.do?method=marks&executionCourseID=1126312223704031'
cursos = ["lca", "lea", "lect", "lecc", "lemec", "leet", "lee", "lef", "leit", "lemt", "lgbs", "lgf"]
invalid_semester_error = 'Semestre inválido.'
comands_tutorial= '''Aqui estão os comandos e seu modo de uso:

1. Para a busca de notas => notas:[sigla da cadeira]/[nr de estudante]
   ex: notas:PRDM-2/111 
   NB: as siglas são diferentes das acostumadas, e podem ser consultadas
       pelo comando a seguir

2. Para a consulta de siglas => sigla:[curso]/[cadeira]/[semestre]
   ex: sigla:lecc/Análise/1
       sigla:lecc/Programação/2
   Quanto à parte da [cadeira], basta escrever uma palavra dentro do nome da cadeira'''


print(comands_tutorial)


