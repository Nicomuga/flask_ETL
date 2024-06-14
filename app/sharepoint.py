import os
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files import file
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Variables de SharePoint
username = os.getenv('SHAREPOINT_USERNAME')
password = os.getenv('SHAREPOINT_PASSWORD')
site_url = os.getenv('SITE_URL')
base_folder_url = os.getenv('BASE_FOLDER_URL')

# Función para normalizar los nombres de columnas
def normalize_column_name(name):
    normalized = name.strip().upper()
    normalized = normalized.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    return normalized

def fetch_data_from_sharepoint():
    ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
    print(ctx)  
    # Obtener la lista de archivos y carpetas en el directorio base
    folders = ctx.web.get_folder_by_server_relative_url(base_folder_url).folders.get().execute_query()
    files = ctx.web.get_folder_by_server_relative_url(base_folder_url).files.get().execute_query()
    print(folders)
    print(files)
    # Lista para almacenar los DataFrames
    dfs = []

    # Iterar a través de cada carpeta y archivo
    for folder in folders:
        print(folder)
        folder_url = folder.properties["ServerRelativeUrl"]
        sub_files = ctx.web.get_folder_by_server_relative_url(folder_url).files.get().execute_query()

        for sub_file in sub_files:
            file_url = sub_file.properties["ServerRelativeUrl"]
            file_name = sub_file.properties["Name"]

            if file_name.endswith('.xlsx'):
                response = File.open_binary(ctx, file_url)
                with open(file_name, 'wb') as local_file:
                    local_file.write(response.content)

                # Leer el archivo Excel
                df = pd.read_excel(file_name, sheet_name='NOK')

                # Normalizar nombres de columnas
                df.columns = [normalize_column_name(col) for col in df.columns]

                # Seleccionar las columnas necesarias
                required_columns = [
                    "FOLIO RECEPCION", "CAMPO CON ERROR", "DEBE DECIR OTROS CAMPOS", 
                    "FALTA SACAR DEDUCIBLE", "SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)"
                ]
                optional_columns = ["RESPONSABLE", "RAZON", "COMENTARIOS"]

                # Verificar y seleccionar las columnas disponibles
                available_columns = [col for col in required_columns if col in df.columns]
                available_optional_columns = [col for col in optional_columns if col in df.columns]
                selected_columns = available_columns + available_optional_columns

                # Agregar columna de origen
                df = df[selected_columns]
                df["ORIGEN"] = folder_url + '/' + file_name

                # Agregar el DataFrame a la lista
                dfs.append(df)

                # Eliminar el archivo temporal
                os.remove(file_name)

    # Concatenar todos los DataFrames
    final_df = pd.concat(dfs, ignore_index=True)
    print(_acquire_service_token_from_adfs)
    return final_df
