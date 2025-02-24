from flask import Flask
from extensions import db
from flask_cors import CORS


app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 

from models import Estudante, NotaDasMaterias

with app.app_context():
    
    db.create_all()

import routes