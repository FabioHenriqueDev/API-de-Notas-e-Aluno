# 📚 API de Notas e Alunos

Bem-vindo à API de Notas e Alunos! 🚀
Esta API permite o cadastro de estudantes, registro de notas em diferentes matérias e envio de e-mails automáticos com base no desempenho acadêmico.

---

## 🛠️ Tecnologias Utilizadas

- Python 🐍
- Flask ⚡
- SQLAlchemy 🗄️
- SQLite 🛢️
- Flask-Migrate 🔄
- Flask-SQLAlchemy 🔧
- Dotenv 🔐
- Re 🧐 (Expressões Regulares)
- SMTP 📧

---

## 📌 Funcionalidades

✅ Cadastro de estudantes com validação de CPF e e-mail 📄
✅ Registro de notas dos alunos 📑
✅ Cálculo automático da média final 📊
✅ Envio de e-mails automáticos informando a aprovação ou reprovação 🎓✉️
✅ Atualização de notas 🎯

---

## 📂 Estrutura do Projeto

```
📂 API-de-Notas-e-Aluno
│-- 📂 migrations
│-- 📂 extensions
│-- 📂 models
│-- 📄 __init__.py
│-- 📄 app.py
│-- 📄 config.py
│-- 📄 requirements.txt
│-- 📄 .env
```

- `app.py`: Arquivo principal contendo as rotas e regras de negócio
- `models.py`: Definição dos modelos do banco de dados
- `config.py`: Configurações da aplicação
- `extensions.py`: Inicialização do banco de dados
- `migrations/`: Pasta gerenciada pelo Flask-Migrate
- `.env`: Variáveis de ambiente sensíveis

---

## 🔧 Como Executar o Projeto

1️⃣ Clone o repositório:
```sh
   git clone https://github.com/FabioHenriqueDev/API-de-Notas-e-Aluno.git
```

2️⃣ Acesse o diretório do projeto:
```sh
   cd API-de-Notas-e-Aluno
```

3️⃣ Crie um ambiente virtual e ative-o:
```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
```

4️⃣ Instale as dependências:
```sh
   pip install -r requirements.txt
```

5️⃣ Configure suas variáveis de ambiente no arquivo `.env`:
```sh
   email=seuemail@gmail.com
   senha_app=suasenha
```

6️⃣ Execute a aplicação:
```sh
   flask run
```

---

## 📬 Contato

Desenvolvido por [Fabio Henrique](https://github.com/FabioHenriqueDev) 👨‍💻

Se você gostou do projeto, deixe uma ⭐ no repositório! 😊

