import pandas as pd
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'
driver.get(url)

download_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
download_link.click()

time.sleep(2)

current_date = datetime.now().strftime('%d-%m-%y')
download_folder = 'C:/Users/rerys/Downloads'

files_in_download_folder = os.listdir(download_folder)

download_filename = f'IBOVDia_{current_date}.csv'
download_path = os.path.join(download_folder, download_filename)

if not os.path.exists(download_path):
    print(f"Erro: o arquivo {download_filename} não foi encontrado na pasta de downloads.")
else:
    # Lê o CSV
    df = pd.read_csv(download_path, encoding='latin1', sep=';', header=None, skiprows=2, on_bad_lines='skip')
    df = df.dropna(axis=1, how='all')

    # Adiciona as colunas de cabeçalho
    df.columns = ['Codigo', 'Acao', 'Tipo', 'Qtde. Teorica', 'Part.']

    # Adiciona uma coluna de data no formato americano
    current_date_american = datetime.now().strftime('%Y-%m-%d')
    df['Data'] = current_date_american

    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')

    parquet_dir = f'D:/Dev/Scraping_b3/Parquet/{year}/{month}/{day}'
    os.makedirs(parquet_dir, exist_ok=True)

    # Define o caminho para salvar o arquivo Parquet com nome baseado na data do download
    parquet_output_path = os.path.join(parquet_dir, f'ibovespa_{current_date_american}.parquet')

    # Salva o DataFrame em formato Parquet
    df.to_parquet(parquet_output_path, index=False)

    # Lê o arquivo Parquet salvo para verificar
    df_loaded = pd.read_parquet(parquet_output_path)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print(df_loaded)