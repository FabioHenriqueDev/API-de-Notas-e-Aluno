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


load_dotenv()

@app.route("/cadastro", methods=['POST'])
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
        

    