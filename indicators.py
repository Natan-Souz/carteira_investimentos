import sqlite3
import pandas as pd 
import data_handler


def calcular_metricas():
    conexcao = sqlite3.connect('carteira.db')
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY data DESC", conexcao)
    conexcao.close()

    if df.empty:
        return{"saldo_total": 0, "lucro_bruto": 0, "rentabilidade": 0}
    
    #Obter cotação atual
    df["preco_atual"] = df["ativo"].apply(lambda x: data_handler.obter_preco_atual(x) if x else None)

    # Converter valores para números
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    df["preco_atual"] = pd.to_numeric(df["preco_atual"], errors="coerce")
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
