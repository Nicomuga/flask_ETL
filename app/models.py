from . import db

class DataEntry(db.Model):
    __tablename__ = 'revision_qa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folio_recepcion = db.Column(db.String, nullable=True)
    campo_con_error = db.Column(db.String, nullable=True)
    debe_decir_otros_campos = db.Column(db.String, nullable=True)
    falta_sacar_deducible = db.Column(db.String, nullable=True)
    saco_deducible_erroneo = db.Column(db.String, nullable=True)
    responsable = db.Column(db.String, nullable=True)
    razon = db.Column(db.String, nullable=True)
    comentarios = db.Column(db.String, nullable=True)
    file = db.Column(db.String, nullable=False)