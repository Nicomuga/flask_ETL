from . import db

class DeductibleAmount(db.Model):
    __tablename__ = 'revision_qa_monto_deducible'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folio_recepcion = db.Column(db.String, nullable=True)
    mes = db.Column(db.String, nullable=True)
    debe_decir_otros_campos = db.Column(db.String, nullable=True)
    falta_sacar_deducible = db.Column(db.String, nullable=True)
    saco_deducible_erroneo = db.Column(db.String, nullable=True)
    responsable = db.Column(db.String, nullable=True)
    razon = db.Column(db.String, nullable=True)
    comentarios = db.Column(db.String, nullable=True)
    fecha_rev = db.Column(db.String, nullable=True)
    file = db.Column(db.String, nullable=False)

class OtherFields(db.Model):
    __tablename__ = 'revision_qa_otros_campos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folio_recepcion = db.Column(db.String, nullable=True)
    mes = db.Column(db.String, nullable=True)
    campo_con_error = db.Column(db.String, nullable=True)
    debe_decir_otros_campos = db.Column(db.String, nullable=True)
    responsable = db.Column(db.String, nullable=True)
    razon = db.Column(db.String, nullable=True)
    comentarios = db.Column(db.String, nullable=True)
    fecha_rev = db.Column(db.String, nullable=True)
    file = db.Column(db.String, nullable=False)