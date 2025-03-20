import sqlite3
import pandas as pd 
import data_handler


def calcular_metricas():
    conexcao = sqlite3.connect('carteira.db')
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY data DESC", conexcao)
    conexcao.close()