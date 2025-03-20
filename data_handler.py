import yfinance as yf

def obter_preco_atual(ativo):
    try:
        ticker = f"{ativo}"
        acao = yf.Ticker(ticker)
        preco = acao.history(period="1d")["Close"].iloc[-1]
        return round(preco, 2)
    except Exception as e:
        print(f"Erro ao obter preço da ação {ativo}: {e}")
        return None
