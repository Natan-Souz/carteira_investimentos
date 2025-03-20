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
    
    #Calcular valores investidos e atuais
    df["valor_investido"] = df["quantidade"] * df["preco"]
    df["valor_atual"] = df["quantidade"] * df["preco_atual"]

    saldo_total = df["valor_atual"].sum()
    lucro_bruto = saldo_total - df["valor_investido"].sum()
    rentabilidade = (lucro_bruto / df["valor_investido"].sum()) * 100 if df["valor_investido"].sum() > 0 else 0

    return {
        "saldo_total": round(saldo_total, 2),
        "lucro_bruto": round(lucro_bruto, 2),
        "rentabilidade": round(rentabilidade, 2)
    }