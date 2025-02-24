from flask import Flask, request, jsonify
from extensions import db
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from __init__ import app
import re

load_dotenv()

@app.route("/cadastro", methods=['POST'])
def cadastro():
    dados = request.get_json()

    
    if not dados or 'nome' not in dados or not dados['nome']:
        return jsonify({'Erro': 'Digite o nome do aluno para continuar o cadastro...'})
    
    if not dados or 'cpf' not in dados or not dados['cpf']:
        return jsonify({'Erro': 'Digite o CPF do aluno para continuar o cadastro...'})

    if not dados or 'data de nascimento' not in dados or not dados['data de nascimento']:
        return jsonify({'Erro': 'Digite a data de nascimento para continuar...'})
    
    if not dados or 'endereco' not in dados or not dados['endereco']:
        return jsonify({'Erro': 'Digite o endereço do aluno para continuar...'})
    
    if not dados or 'email' not in dados or not dados['email']:
        return jsonify({'Erro': 'Digite o E-mail do aluno para continuar...'})

    
    return jsonify({'Sucesso': 'Deu tudo certo'})