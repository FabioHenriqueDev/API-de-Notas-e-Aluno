from flask import Flask, request, jsonify
from models import Estudante, NotaDasMaterias
from extensions import db
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from __init__ import app
import re
from datetime import datetime
import smtplib


load_dotenv()

@app.route("/registro", methods=['POST'])
def cadastro():
    dados = request.get_json()

    
    if not dados or 'nome' not in dados or not dados['nome']:
        return jsonify({'Erro': 'Digite o nome do aluno para continuar o cadastro...'})
    
    if not dados or 'cpf' not in dados or not dados['cpf']:
        return jsonify({'Erro': 'Digite o CPF do aluno para continuar o cadastro...'})
    
    cpf_existente = Estudante.query.filter_by(cpf=dados['cpf']).first()

    if cpf_existente:
        return jsonify({'Erro': "Esse CPF já está cadastrado no nosso sistema."})

    if not dados or 'data_nascimento' not in dados or not dados['data_nascimento']:
        return jsonify({'Erro': 'Digite a data de nascimento para continuar...'})
    
    if not dados or 'endereco' not in dados or not dados['endereco']:
        return jsonify({'Erro': 'Digite o endereço do aluno para continuar...'})
    
    if not dados or 'email' not in dados or not dados['email']:
        return jsonify({'Erro': 'Digite o E-mail do aluno para continuar...'})
    
    email_existente = Estudante.query.filter_by(email=dados['email']).first()

    if email_existente:
        return jsonify({'Erro': 'Esse E-mail ja está cadastrado no nosso sistema.'})
    
    if not re.fullmatch(r"^\d+$", dados['cpf']):
        return jsonify({'Erro': "Digite números no CPF"})
    
    if len(dados['cpf']) != 11:
        return jsonify({'Erro': 'CPF tem que ter 11 digitos.'})
    
    email_padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_padrao, dados['email']):
        return jsonify({'Erro': 'Digite um E-mail válido'})
    
    data_nascimento = datetime.strptime(dados['data_nascimento'], "%d-%m-%Y").date()
    
    
    estudante = Estudante(
        
        nome = dados['nome'],
        cpf = dados['cpf'],
        data_nascimento = data_nascimento,
        endereco = dados['endereco'],
        email = dados['email']
    )

    try:
        db.session.add(estudante)
        db.session.commit()
        return jsonify({'Sucesso':  "Estudante cadastrado com sucesso!"})
    
    except Exception as e:
        print(f'Erro: {e}')
        return jsonify({'Erro': f'{e}'})
        

@app.route('/registromaterias', methods=['POST'])
def cadastro_metrias():
    
    lista_materias = ['nota_artes', 'nota_ciencias', 'nota_geografia', 'nota_historia', 'nota_portugues', 'nota_matematica', 'nota_ingles']

    dados = request.get_json()

    if not dados or 'email' not in dados or not dados['email']:
        return jsonify({'Erro': 'Digite o E-mail do aluno para continuar...'})

    estudante = Estudante.query.filter_by(email=dados['email']).first()

    if not estudante:
        return jsonify({'Erro': 'Esse E-mail não foi cadastrado no nosso sistema'})
    
    
    for materia in lista_materias:
        if not dados or materia not in dados or not dados[materia]:
            return jsonify({'Erro': 'Digite a nota de todas materias para continuar...'})

    
    media = (dados['nota_artes'] + dados['nota_ciencias'] + dados['nota_geografia'] + dados['nota_historia'] + dados['nota_portugues'] + dados['nota_matematica'] + dados['nota_ingles']) / 7
    media_formatada = f'{media:.1f}'
    
    nota_das_materias = NotaDasMaterias(
                        
                        id_usuario=estudante.id,
                        nome=estudante.nome,
                        email=dados['email'],
                        nota_artes=dados['nota_artes'],
                        nota_ciencias=dados['nota_ciencias'],
                        nota_geografia=dados['nota_geografia'],
                        nota_historia=dados['nota_historia'],
                        nota_portugues=dados['nota_portugues'],
                        nota_matematica=dados['nota_matematica'],
                        nota_ingles=dados['nota_ingles'],
                        media_final=media_formatada
        
                    )
    
    if media >= 6:
        
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = os.environ["email"]
        sender_password = os.environ["senha_app"]

        # Compondo o e-mail
        msg = MIMEMultipart()
        msg['Subject'] = 'Parabéns! Você foi aprovado na nossa escola!'
        msg['From'] = sender_email
        msg['To'] = dados['email']

        html = f"""
                <html>
                <body style="font-family: Arial">
                    <h1 style="color: blue;">Olá {nota_das_materias.nome},</h1>
                    <h2>Espero que esta mensagem te encontre bem. Tenho o prazer de informar que você foi aprovado na nossa escola! Parabéns pela sua conquista. Estamos muito empolgados em tê-lo como parte da nossa comunidade.</h2>
                    <b><h3>Detalhes da Aprovação:</h3></b>
                    <ul>
                        <li><b>Nome:</b>{nota_das_materias.nome}</li>
                        <li><b>Data da Aprovação:</b> {datetime.today()}</li>
                        <li><b>Curso/Programa:</b> Ensino Médio</li>
                    </ul>
                    <h3>A sua aprovação é um reflexo do seu esforço e dedicação, e estamos ansiosos para te ajudar a alcançar todos os seus objetivos acadêmicos e pessoais.</h3>
                    <h3>Por favor, fique atento ao seu e-mail para mais informações sobre o processo de matrícula, horários das aulas e outras orientações importantes. Se você tiver qualquer dúvida, não hesite em entrar em contato conosco.</h3>
                    <h4>Agradecemos pela sua atenção e estamos à disposição para qualquer dúvida.</a></h4>
                    <p style="color: gray;">Atenciosamente, Sistema</p>
                </body>
                </html>
            """

        msg.attach(MIMEText(html, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
                print('Email Enviado com Sucesso')

        except:
            print('Erro ao envio do E-mail')
    
    else:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = os.environ["email"]
        sender_password = os.environ["senha_app"]

        # Compondo o e-mail
        msg = MIMEMultipart()
        msg['Subject'] = 'Atualização sobre sua situação acadêmica'
        msg['From'] = sender_email
        msg['To'] = dados['email']

        html = f"""
                <html>
                <body style="font-family: Arial">
                    <h1 style="color: blue;">Olá {nota_das_materias.nome},</h1>
                    <h2>Espero que esta mensagem te encontre bem. Gostaríamos de informar que, após a análise de suas notas, você não atingiu a média necessária para ser aprovado este ano. Sabemos que essa notícia pode ser decepcionante, mas estamos aqui para apoiar você e ajudá-lo a seguir em frente.</h2>
                    <b><h3>Detalhes da Reprovação:</h3></b>
                    <ul>
                        <li><b>Nome:</b>{nota_das_materias.nome}</li>
                        <li><b>Data da Atualização:</b> {datetime.today()}</li>
                        <li><b>Curso/Programa:</b> Ensino Médio</li>
                    </ul>
                    <h3>Apesar dessa adversidade, acreditamos no seu potencial e estamos prontos para oferecer todo o suporte necessário para que você possa superar esses desafios e alcançar seus objetivos acadêmicos e pessoais.</h3>
                    <h3>Por favor, fique atento ao seu e-mail para mais informações sobre as opções disponíveis, como recuperação de notas, aulas de reforço, e orientações importantes. Se você tiver qualquer dúvida ou precisar de suporte, não hesite em entrar em contato conosco.</h3>
                    <h4>Agradecemos pela sua atenção e estamos à disposição para qualquer dúvida.</a></h4>
                    <p style="color: gray;">Atenciosamente, Sistema</p>
                </body>
                </html>
            """

        msg.attach(MIMEText(html, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
                print('Email Enviado com Sucesso')

        except:
            print('Erro ao envio do E-mail')
    

    try:
        db.session.add(nota_das_materias)
        db.session.commit()
        return jsonify({'Sucesso': 'Informações adicionadas ao Banco de Dados!'})
    
    except Exception as e:
        print(f'Erro: {e}')
        return jsonify({'Erro': f'{e}'})

    
    
@app.route('/atualizarinfo', methods=['PUT'])
def atualizar_info():
    dados = request.get_json()
    lista_materias = ['nota_artes', 'nota_ciencias', 'nota_geografia', 'nota_historia', 'nota_portugues', 'nota_matematica', 'nota_ingles']
    
    if not dados or 'email' not in dados or not dados['email']:
        return jsonify({'Erro': 'Digite o email cadastrado...'}), 400
    

    for materia in lista_materias:
        if not dados or materia not in dados or not dados[materia]:
            return jsonify({'Erro': 'Digite a nota de todas materias para atualizar...'})

    estudante = NotaDasMaterias.query.filter_by(email=dados["email"]).first()

    if not estudante:
        return jsonify({'Erro': "Estudante não encontrado"})

    
   
    try:
        estudante.nota_artes = dados["nota_artes"]
        estudante.nota_ciencias = dados["nota_ciencias"]
        estudante.nota_geografia = dados["nota_geografia"]
        estudante.nota_historia = dados["nota_historia"]
        estudante.nota_portugues = dados["nota_portugues"]
        estudante.nota_matematica = dados["nota_matematica"]
        estudante.nota_ingles = dados["nota_ingles"]
        db.session.commit()
        return jsonify({'Sucesso': 'Informações atualizadas!'})
        
    
    except Exception as e:
        return jsonify({'Erro': f'{e}'})
    
