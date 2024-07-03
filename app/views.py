from flask import Blueprint, jsonify, Flask
from . import db
from .models import DataEntry
# from .sharepoint import fetch_data_from_sharepoint
from .drive import fetch_data_from_google_drive





main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenido a la API de Sharepoint"})

@main.route('/fetch', methods=['GET'])
def fetch_data():
    
    data = fetch_data_from_google_drive()

    # Guardar los datos en la base de datos
    for index, row in data.iterrows():
        entry = DataEntry(
            folio_recepcion=row.get("FOLIO RECEPCION"),
            campo_con_error=row.get("CAMPO CON ERROR"),
            debe_decir_otros_campos=row.get("DEBE DECIR OTROS CAMPOS"),
            falta_sacar_deducible=row.get("FALTA SACAR DEDUCIBLE"),
            saco_deducible_erroneo=row.get("SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)"),
            responsable=row.get("RESPONSABLE"),
            razon=row.get("RAZON"),
            comentarios=row.get("COMENTARIOS"),
            file=row["FILE"]
        )
        db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Datos extraídos y guardados exitosamente"})
