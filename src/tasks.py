import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import requests
from prefect import task
from sqlalchemy import create_engine
from schemas import BrtReport
from utils import log

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


URL = "https://dados.mobilidade.rio/gps/brt"
DATA_FOLDER = os.path.join('..', 'reports')

DB_CONN_STR = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/postgres"
TABLE_NAME = 'brt_report'

@task
def get_data() -> dict:
    """
    Função para realizar a captura de dados. Retorna a resposta em caso de sucesso na requisição, se não retorna um dicionário vazio.

    Returns:
        dict: dicionário com o conteúdo capturado.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()

        log("✅ Dados capturados com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        log(f"❌ Falha na requisição: {str(e)}")
        raise


@task
def parse_data(data: dict) -> pd.DataFrame:
    """
    Transforma os dados capturados em um DataFrame do Pandas. Retorna um dataf

    Args:
        data (dict): dados capturados pela API

    Returns:
        pd.DataFrame: dados estruturados em um DataFrame
    """
    try:
        df = pd.DataFrame(data["veiculos"])
        log("✅ Dados estruturados com sucesso.")
        return df
    except Exception as e:
        log(f"❌ Falha na estruturação dos dados: {e}")

@task
def save_report(data: pd.DataFrame) -> str:
    """
    Salva os dados capturados em um arquivo CSV

    Args:
        data (pd.DataFrame): DataFrame com os dados estruturados
    """

    time = datetime.now().strftime("%Y-%m-%d-%H%M")

    filename = f"BRT_GPS_{time}.csv"
    filepath = os.path.join(DATA_FOLDER, filename)
    print(filepath)
    data.to_csv(filepath, index=False)
    log("✅ Dados salvos com sucesso.")

    return filepath  
        
@task
def process_data(filepath) -> pd.DataFrame:
    """
    Processa os dados extraídos e estruturados.

    Args:
        data (pd.DataFrame): DataFrame estruturado.

    Returns:
        pd.DataFrame: DataFrame processado.
    """
    
    df = pd.read_csv(filepath)
    df.rename(columns={'dataHora':'datahora'}, inplace=True)
    df["datahora"] = pd.to_datetime(df["datahora"], unit='ms')
    df.drop(columns="id_migracao_trajeto", inplace=True) # Atributo sempre vazio
    
    
    log('✅ Dados processados com sucesso.')
    return df

@task
def load_to_database(dataframe:pd.DataFrame) -> None:
    """
    Carrega o conjunto de dados estruturado no banco de dados.

    Args:
        dataframe (pd.DataFrame): DataFrame processado.
    """
    engine = create_engine(DB_CONN_STR)

    try:
        df_validated = BrtReport.validate(dataframe)
        df_validated.to_sql(
            TABLE_NAME, engine, if_exists="append", index=False, method="multi"
        )
        log("✅ Dados carregados na base de dados.")
    except Exception as e:
        log(f"❌ Erro durante o carregamento na base de dados: {str(e)}")
    
