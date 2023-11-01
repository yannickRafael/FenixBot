import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fenixbot-isutc-default-rtdb.firebaseio.com/'
})


cadeiras_ref = db.reference('files/cadeiras')
recibos_ref = db.reference('files/recibos')
feedback_ref = db.reference('files/feedbacks')
account_sid = 'AC676d8e071ce0ea4839865a3c45e13968'
auth_token = '53ceb3e6492c0c8867aa96d6484463fd'
invalid_command_error = "Comando não reconhecido\nDigite 'comandos' para entender mais sobre os comandos"

username = 'yannick.matimbe'
password = 'Y@nnickR@fael2003'
login_url = 'https://fenixlbb.isutc.ac.mz:8443/cas/login?service=https://fenixlbb.isutc.ac.mz:8443/isutc/'
logged_url = 'https://fenixlbb.isutc.ac.mz/isutc/fenixEduIndex.do'
mark_url = 'https://fenixlbb.isutc.ac.mz/isutc/publico/executionCourse.do?method=marks&executionCourseID=1126312223704031'
cursos = ["lca", "lea", "lect", "lecc", "lemec", "leet", "lee", "lef", "leit", "lemt", "lgbs", "lgf"]
invalid_semester_error = 'Semestre inválido.'
comands_tutorial= '''Aqui estão os comandos e seu modo de uso:

1. Para a busca de notas 
   ↳ notas:[sigla da cadeira]/[nr de estudante]
   ex: notas:PRDM-2/111 
   NB: as siglas são diferentes das acostumadas, e podem ser consultadas
       pelo comando a seguir

2. Para a consulta de siglas
   ↳ sigla:[curso]/[cadeira]
   ex: sigla:lecc/Análise/1
       sigla:lecc/Programação/2
   Quanto à parte da [cadeira], basta escrever uma palavra dentro do nome da cadeira
   
3. Para pagar mensalidade
   ↳ pagar:[numero-mpesa]/[referência]/[valor]
   NB: Este comando está em fase de testes. O pagamento não será efectivamente realizado
   ex: pagar:841111111/1000/11500

4. Para dar feedbacks sobre este bot
   ↳ feedback:[feedback]
   ex: feedback:Este bot precisa de melhorar no aspecto "x"
   
'''





