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
    
    dados = request.get_json()

    if not dados or 'email' not in dados or not dados['email']:
        return jsonify({'Erro': 'Digite o E-mail do aluno para continuar...'})

    estudante = Estudante.query.filter_by(email=dados['email']).first()

    if not estudante:
        return jsonify({'Erro': 'Esse E-mail não foi cadastrado no nosso sistema'})
    
    if not dados or 'nota_artes' not in dados or not dados['nota_artes']:
        return jsonify({'Erro': 'Digite a nota de artes para continuar...'})
    
    if not dados or 'nota_ciencias' not in dados or not dados['nota_ciencias']:
        return jsonify({'Erro': 'Digite a nota de ciencias para continuar...'})
    
    if not dados or 'nota_geografia' not in dados or not dados['nota_geografia']:
        return jsonify({'Erro': 'Digite a nota de geografia para continuar...'})
    
    if not dados or 'nota_historia' not in dados or not dados['nota_historia']:
        return jsonify({'Erro': 'Digite a nota de historia para continuar...'})
    
    if not dados or 'nota_portugues' not in dados or not dados['nota_portugues']:
        return jsonify({'Erro': 'Digite a nota de português para continuar...'})
    
    if not dados or 'nota_matematica' not in dados or not dados['nota_matematica']:
        return jsonify({'Erro': 'Digite a nota de matemática para continuar...'})
    
    if not dados or 'nota_ingles' not in dados or not dados['nota_ingles']:
        return jsonify({'Erro': 'Digite a nota de inglês para continuar...'})
    
    media = (dados['nota_artes'] + dados['nota_ciencias'] + dados['nota_geografia'] + dados['nota_historia'] + dados['nota_portugues'] + dados['nota_matematica'] + dados['nota_ingles']) / 7
    media_formatada = f'{media:.2f}'


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
    try:
        db.session.add(nota_das_materias)
        db.session.commit()
        return jsonify({'Sucesso': 'Informações adicionadas ao Banco de Dados!'})
    
    except Exception as e:
        print(f'Erro: {e}')
        return jsonify({'Erro': f'{e}'})
    
    