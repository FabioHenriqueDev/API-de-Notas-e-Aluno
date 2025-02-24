from extensions import db

class Estudante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    cpf = db.Column(db.Integer, nullable=False, unique=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(140), nullable=False, unique=True)


class NotaDasMaterias(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True, nullable=False)
    nome = db.Column(db.String(60), db.ForeignKey('estudante.id'), nullable=False)
    email = db.Column(db.String(140), db.ForeignKey('estudante.id'), nullable=False, unique=True)
    nota_artes = db.Column(db.Integer, nullable=False)
    nota_ciencias = db.Column(db.Integer, nullable=False)
    nota_geografia = db.Column(db.Integer, nullable=False)
    nota_historia = db.Column(db.Integer, nullable=False)
    nota_portugues = db.Column(db.Integer, nullable=False)
    nota_matematica = db.Column(db.Integer, nullable=False)
    nota_ingles = db.Column(db.Integer, nullable=False)
    media_final = db.Column(db.Integer, nullable=False)