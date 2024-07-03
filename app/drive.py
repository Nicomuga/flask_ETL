from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import os
import pandas as pd
from dotenv import load_dotenv
from unidecode import unidecode
import gc

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
    return unidecode(name.strip().upper().replace(' ', '_'))

def normalize_columns(df):
    df.rename(columns=lambda x: normalize_column_name(x), inplace=True)


def normalize_value(value):
    if isinstance(value, str):
        return unidecode(value.strip().upper())
    return value

def normalize_dataframe(df):
    for col in df.columns:
        df[col] = df[col].apply(normalize_value)
    df = df.where(pd.notna(df), None)
    return df


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
                    "FALTA SACAR DEDUCIBLE", "SACO DEDUCIBLE ERRONEO (NO DEDUCIBLE)", "ESTADO OK/NOK"]
    op_columns = ["RESPONSABLE", "RAZON", "COMENTARIOS"]
    required_columns = [normalize_column_name(col) for col in re_columns]
    optional_columns = [normalize_column_name(col) for col in op_columns]
    
    # Lista para almacenar los DataFrames
    final_df = pd.DataFrame()
    # Iterar a través de cada carpeta
    counted_items = 0
    counted_entrys = 0
    
    for folder in folders.get('files', []):
        # Obtener la lista de archivos en la carpeta actual
        items = service.files().list(q="'{0}' in parents".format(folder['id']),
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute().get('files', [])
        print(items)
        print(len(items))
        dfs = []
        counted_items += len(items)
        folder_counter = 0
        item_counter = 0
        print('+++++++++++++++++++++++----------folder---------++++++++++++++++++++++++')
        print('+++++++++++++++++++++++-------------------++++++++++++++++++++++++')
        print('+++++++++++++++++++++++-------------------++++++++++++++++++++++++')
        # Iterar a través de cada archivo
        
        for item in items:
            file_id = item['id']
            file_name = item['name']
            print(f'procesando {file_name}')
            item_counter += 1
            file_counter = 0
            print(f'Archivo N° {item_counter} de {len(items)}')
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
                
                if 'NOK' in upper_fh:
                    df = process_sheet(fh, 'NOK', file_name, required_columns, optional_columns, usecols=range(21))
                    
                else:
                    df = process_sheet(fh, 'RENTAS', file_name, required_columns, optional_columns, usecols=None)

                if df is not None:
                    final_df = pd.concat([final_df, df], ignore_index=True)
                    # Liberar memoria
                counted_entrys += len(df) 
                file_counter += len(df)
                folder_counter += len(df)
                del df
                gc.collect()

            print(f'Se han contado un total de {file_counter}en el archivo {file_name}')
        print(f'Se han contado un total de {folder_counter} en la carpeta {folder["name"]}')
    print(f'Se han contado un total de {counted_entrys} entradas')
    final_df = normalize_dataframe(final_df)
    print(final_df)
    breakpoint()
    return final_df

def process_sheet(fh, sheet_name, file_name, required_columns, optional_columns, usecols):    
    try:
        
        df = pd.DataFrame(pd.ExcelFile(fh).parse(sheet_name, usecols=usecols))
        print(f'PROCESANDO DF ORIGINAL DESDE {sheet_name}++++++++++++++++')
        unnamed_count = count_unnamed_columns(df.columns)
        try_counter = 0
        while unnamed_count > 3:
            try_counter += 1
            df = pd.DataFrame(pd.ExcelFile(fh).parse(sheet_name, skiprows=try_counter, usecols=usecols)) # Eliminar la primera fila
            unnamed_count = count_unnamed_columns(df.columns)
            print(f'+++++++++dropeo de linea N° {try_counter}+++++++++++++')
        estado = 3
    except:
        if sheet_name == 'NOK':
            df = pd.DataFrame(pd.ExcelFile(fh).parse('RENTAS'))
            print(f'PROCESANDO DF ORIGINAL DESDE RENTAS ++++++++++++++++')
            unnamed_count = count_unnamed_columns(df.columns)
            try_counter = 0
            while unnamed_count > 3:
                try_counter += 1
                df = pd.DataFrame(pd.ExcelFile(fh).parse('RENTAS', skiprows=try_counter)) # Eliminar la primera fila
                unnamed_count = count_unnamed_columns(df.columns)
                print(f'+++++++++dropeo de linea N° {try_counter}+++++++++++++')
                # print(df)
            estado = 3
        else: 
            estado = 6
            # TODO agregar una nueva base de datos donde se registren los errores de carga de archivos
            pass
    # breakpoint()
    
    if estado == 3:
        # print(df)
        # print('------------------------------------------------------------------------')
        df.columns = [normalize_column_name(col) for col in df.columns]
        df.columns = df.columns.str.replace('\n', '')
        df.columns = df.columns.str.replace('.', '')
        available_columns = [col for col in required_columns if col in df.columns]
        # print(available_columns)
        available_optional_columns = [col for col in optional_columns if col in df.columns]
        # print(available_optional_columns)
        selected_columns = available_columns + available_optional_columns
        # print(selected_columns)
        df = df[selected_columns]
        df["FILE"] = file_name
        
        # df = df.drop(columns=['ESTADO_OK/NOK'])
        # print(df)
        normalize_dataframe(df)
        df = df[df['ESTADO_OK/NOK'] == 'NOK']
        print(f'Archivo {file_name} leído exitosamente DESDE {sheet_name}')
        print(f'contiene {len(df)} entradas')
        print('-+*-+-*-+-*-+-*-+-*-+-*-+-*-+-*-*-+-*-+-**-+-')
        # print(f'DF FINAL DEL ARCHIVO {file_name}+++++++++++++++++++++++++++++++++++')
        # print(df)
        return df
    else: 
        print(f'No se logra leer el archivo {file_name}')
        print('FORMA DEL DF ERRONEO++++++++++++++++++++++++')
        print(df)
        print('-+*-+-*-+-*-+-*-+-*-+-------------------------++++++++++++++++++++++++-----------------------*-+-*-+-*-*-+-*-+-**-+-')
        return None
       

# fetch_data_from_google_drive()