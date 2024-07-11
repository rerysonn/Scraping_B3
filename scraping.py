import pandas as pd
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

driver.get(url)

download_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
download_link.click()

time.sleep(2)

download_path = 'C:/Users/rerys/Downloads/IBOVDia_10-07-24.csv'
print(f"Arquivo baixado: {download_path}")

df = pd.read_csv(download_path, encoding='latin1', sep=';', header=2, on_bad_lines='skip')
df = df.dropna(axis=1, how='all')


print(df.head())
