from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import os
import pandas as pd
from dotenv import load_dotenv
from unidecode import unidecode

# Cargar las variables de entorno
load_dotenv()

# Variables de Google Drive
credentials_file = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')
folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# # Función para normalizar los nombres de columnas
# def normalize_column_name(name):
#     normalized = name.strip().upper()
#     normalized = normalized.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
#     return normalized

def count_unnamed_columns(columns):
    return sum([1 for col in columns if 'Unnamed' in col])

def normalize_column_name(name):
    # Convertir a minúsculas, eliminar espacios y tildes
    return unidecode(name.strip().lower().replace(' ', '_'))

def fetch_data_from_google_drive():
    # Autenticar con la API de Google Drive
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, ['https://www.googleapis.com/auth/drive'])
    creds = flow.run_local_server(port=0)
    service = build('drive', 'v3', credentials=creds)

    # Obtener la lista de archivos en el directorio base
    results = service.files().list(q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])
    print(items)

    folders = service.files().list(
    q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
    spaces='drive',
    fields='nextPageToken, files(id, name)').execute()
    print(folders)
    re_columns = [
                    "FOLIO RECEPCION", "CAMPO CON ERROR", "DEBE DECIR OTROS CAMPOS", 
                    "FALTA SACAR DEDUCIBLE", "SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)"]
    op_columns = ["RESPONSABLE", "RAZON", "COMENTARIOS"]
    required_columns = [normalize_column_name(col) for col in re_columns]
    optional_columns = [normalize_column_name(col) for col in op_columns]
    
    # Lista para almacenar los DataFrames
    dfs = []

    # Iterar a través de cada carpeta
    for folder in folders.get('files', []):
        # Obtener la lista de archivos en la carpeta actual
        items = service.files().list(q="'{0}' in parents".format(folder['id']),
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute().get('files', [])
        print(items)
        
        dfs = []
        # Iterar a través de cada archivo
        for item in items:
            file_id = item['id']
            file_name = item['name']
            print(file_name)
            if file_name.endswith('.xlsx'):
                request = service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                fh.seek(0)

                # if 'Sheet1' in excel_file.sheet_names:
                #     # Cargar la hoja 'Sheet1' en un DataFrame
                #     df_sheet1 = excel_file.parse('Sheet1')

                sheets_fh = pd.ExcelFile(fh).sheet_names
                upper_fh = [sheet.upper() for sheet in sheets_fh]
                if  'NOK' in upper_fh:
                    df = pd.ExcelFile(fh).parse('NOK', usecols='A:U')
                    print('df ORIGINAL ++++++++++++++++')
                    print(df)
                    print(f'original columns ++++++++++++++++++++++++')
                    print(df.columns)
                    unnamed_count = count_unnamed_columns(df.columns)
                    try_counter = 0
                    while unnamed_count > 3:
                        try_counter += 1
                        df = pd.DataFrame(pd.ExcelFile(fh).parse('NOK', skiprows=try_counter + 1, usecols='A:U')) # Eliminar la primera fila
                        unnamed_count = count_unnamed_columns(df.columns)
                        print(df)
                        print(f'+++++++++dropeo de linea N° {try_counter}+++++++++++++')
                    df.columns = [normalize_column_name(col) for col in df.columns]
                    # print(df)
                    # print(df.columns)
                    # required_columns = [
                    #     "FOLIO RECEPCION", "CAMPO CON ERROR", "DEBE DECIR OTROS CAMPOS", 
                    #     "FALTA SACAR DEDUCIBLE", "SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)","ESTADO LM"]
                    # optional_columns = ["RESPONSABLE", "RAZON", "COMENTARIOS"]
                    # Verificar y seleccionar las columnas disponibles
                    available_columns = [col for col in required_columns if col in df.columns]
                    # print(available_columns)
                    available_optional_columns = [col for col in optional_columns if col in df.columns]
                    # print(available_optional_columns)
                    selected_columns = available_columns + available_optional_columns
                    # print(selected_columns)
                    df = df[selected_columns]
                    
                    df["origen"] = file_name
                    print(f'Archivo {file_name} leído exitosamente DESDE NOK')
                    dfs.append(df)
                else:
                    df = pd.ExcelFile(fh).parse('RENTAS',)
                    print('df ORIGINAL ++++++++++++++++ RENTAS ')
                    print(df)
                    print('df columns +++++++++++++++++++++ RENTAS ')
                    print(df.columns)
                    unnamed_count = count_unnamed_columns(df.columns)
                    try_counter = 0
                    while unnamed_count > 3:
                        try_counter += 1
                        df = pd.DataFrame(pd.ExcelFile(fh).parse('RENTAS', skiprows=try_counter)) # Eliminar la primera fila
                        unnamed_count = count_unnamed_columns(df.columns)
                        print(df)
                        print(f'+++++++++dropeo de linea N° {try_counter}+++++++++++++')

                    # Normalizar nombres de columnas
                    df.columns = [normalize_column_name(col) for col in df.columns]
                    # print(df.columns)
                    # Seleccionar las columnas necesarias
                    # required_columns = [
                    #     "FOLIO RECEPCION", "CAMPO CON ERROR", "DEBE DECIR OTROS CAMPOS", 
                    #     "FALTA SACAR DEDUCIBLE", "SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)","ESTADO LM"]
                    # optional_columns = ["RESPONSABLE", "RAZON", "COMENTARIOS"]
                    # Verificar y seleccionar las columnas disponibles
                    
                    available_columns = [col for col in required_columns if col in df.columns]
                    # print(available_columns)
                    available_optional_columns = [col for col in optional_columns if col in df.columns]
                    # print(available_optional_columns)
                    selected_columns = available_columns + available_optional_columns + ['estado_lm']
                    df = df[selected_columns]
                    df["origen"] = file_name
                    # print(df)
                    df = df[df['estado_lm'] == 'NOK']
                    df = df.drop(columns=['estado_lm'])
                    # Agregar el DataFrame a la lista
                    print(f'Archivo {file_name} leído exitosamente DESDE RENTAS')
                    dfs.append(df)

        # Concatenar todos los DataFrames
        final_df = pd.concat(dfs, ignore_index=True)
        print(final_df)
        return final_df

fetch_data_from_google_drive()