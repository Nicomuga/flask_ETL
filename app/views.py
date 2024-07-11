from flask import Blueprint, jsonify, request, Flask
from . import db
from sqlalchemy import text
from .models import DeductibleAmount, OtherFields
# from .sharepoint import fetch_data_from_sharepoint
from .drive import fetch_data_from_google_drive
import pandas as pd





main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenido a la API de Sharepoint"})

@main.route('/fetch', methods=['GET'])
def fetch_data():
    
    # data = fetch_data_from_google_drive()
    monto_error, otros_campos = fetch_data_from_google_drive()
    
    
    
    breakpoint()
    # Guardar los datos en la base de datos
    for index,  row in monto_error.iterrows():
        entry = DeductibleAmount(
            folio_recepcion=row["FOLIO_RECEPCION"],
            mes=row["MES"],
            debe_decir_otros_campos=row["DEBE_DECIR_OTROS_CAMPOS"],
            falta_sacar_deducible=row["FALTA_SACAR_DEDUCIBLE"],
            saco_deducible_erroneo=row["SACO_DEDUCIBLE_ERRONEO_(NO_DEDUCIBLE)"],
            responsable=row["RESPONSABLE"],
            razon=row["RAZON"],
            comentarios=row["COMENTARIOS"],
            file=row["FILE"],
            fecha_rev=row["FECHA"]
            
        )  
        print(f'+++++++++++++++++++++++--------- CAMPO_ERROR    ENTRY{row["FOLIO_RECEPCION"]}---------++++++++++++++++++++++++')
        db.session.add(entry)
    db.session.commit()

    for index,  row in otros_campos.iterrows():
        entry = OtherFields(
            folio_recepcion=row["FOLIO_RECEPCION"],
            mes=row["MES"],
            campo_con_error=row["CAMPO_CON_ERROR"],
            debe_decir_otros_campos=row["DEBE_DECIR_OTROS_CAMPOS"],
            responsable=row["RESPONSABLE"],
            razon=row["RAZON"],
            comentarios=row["COMENTARIOS"],
            fecha_rev=row["FECHA"],
            file=row["FILE"]
        )  
        print(f'+++++++++++++++++++++++---------OTROS_CAMPOS     ENTRY FOLIO: {row["FOLIO_RECEPCION"]}---------++++++++++++++++++++++++')
        db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Datos extraídos y guardados exitosamente"})

@main.route('/delete', methods=['POST'])
def delete_records():
    data = request.get_json()
    field = data.get('field')  # Obtener el nombre del campo del cuerpo JSON

    if field:
        try:
            # Utilizar text() para construir una expresión SQL dinámica
            stmt = text(f"DELETE FROM {field}")
            result = db.session.execute(stmt)
            db.session.commit()

            num_rows_deleted = result.rowcount
            return jsonify({"message": f"{num_rows_deleted} rows deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Campo 'field' no proporcionado en la solicitud."}), 400