import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import sqlite3
import plotly.graph_objects as go

import indicators
import order_manager
import data_handler

#inicializa o app
app = dash.Dash(__name__)

def painel():
    metricas = indicators.calcular_metricas()
    
    return html.Div([
        html.Div([
            html.H4("Saldo Total"),
            html.H2(f"R$ {metricas['saldo_total']:,}".replace(",", "."), style={'color': 'green'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),

        html.Div([
            html.H4("Rentabilidade"),
            html.H2(f"{metricas['rentabilidade']}%", style={'color': 'blue'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),

        html.Div([
            html.H4("Lucro Bruto"),
            html.H2(f"R$ {metricas['lucro_bruto']:,}".replace(",", "."), 
                    style={'color': 'green' if metricas['lucro_bruto'] >= 0 else 'red'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'marginBottom': '20px'})

def carregar_transacoes():
    conexao = sqlite3.connect('carteira.db')
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY data DESC", conexao)
    conexao.close()

    if df.empty:
        return pd.DataFrame(columns=["id", "ativo", "tipo", "quantidade", "preco", "preco_atual", "data"])
    
    df["preco_atual"] = df["ativo"].apply(lambda x: data_handler.obter_preco_atual(x) if x else None)

    return df

app.layout = html.Div(children=[
    html.H1("Controle de Carteira de Investimentos", style={'textAlign': 'center'}),

    #Painel de metricas
    html.Div(id="painel-metricas"),

    #Formulario de ordens
    html.Div([
        html.Label("Ativo:"),
        dcc.Input(id="input-ativo", type="text", placeholder="Ex: PETR4", style={'width': '100px'}),

        html.Label("Tipo:"),
        dcc.Dropdown(
            id="input-tipo",
            options=[{"label": "Compra", "value": "compra"}, {"label": "Venda", "value": "venda"}],
            placeholder="Selecione...",
            style={'width': '150px'}
        ),

        html.Label("Quantidade:"),
        dcc.Input(id="input-quantidade", type="number", placeholder="Quantidade", style={'width': '100px'}),

        html.Label("Preço Unitário (R$):"),
        dcc.Input(id="input-preco", type="number", placeholder="Preço", style={'width': '120px'}),

        html.Label("Data da Transação:"),
        dcc.Input(id="input-data", type="text", placeholder="YYYY-MM-DD", style={'width': '120px'}),

        html.Button("Registrar Ordem", id="botao-registrar", n_clicks=0, style={'marginLeft': '10px'}),
    ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '20px'}),

    # Tabela de transações
    html.Div([
        html.H3("📊 Histórico de Transações"),
        dash_table.DataTable(
            id='tabela-transacoes',
            columns=[
                {"name": "ID", "id": "id"},
                {"name": "Ativo", "id": "ativo"},
                {"name": "Tipo", "id": "tipo"},
                {"name": "Quantidade", "id": "quantidade"},
                {"name": "Preço (R$)", "id": "preco"},
                {"name": "Preço Atual (R$)", "id": "preco_atual"},
                {"name": "Data", "id": "data"}
            ],
            data=carregar_transacoes().to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'}
        ),
    ]),

    html.Div([
    html.H3("📊 Desempenho da Carteira"),
    dcc.Graph(id="grafico-rentabilidade", figure={}),   
        ]),
])

# Callback para inserir ordens e atualizar a tabela
@app.callback(
    Output('tabela-transacoes', 'data'),
    Input('botao-registrar', 'n_clicks'),
    State('input-ativo', 'value'),
    State('input-tipo', 'value'),
    State('input-quantidade', 'value'),
    State('input-preco', 'value'),
    State('input-data', 'value'),
    prevent_initial_call=True
)
def registrar_ordem(n_clicks, ativo, tipo, quantidade, preco, data):
    if ativo and tipo and quantidade and preco and data:
        order_manager.inserir_ordem(ativo, tipo, int(quantidade), float(preco), data)
    
    # Atualiza a tabela
    df = carregar_transacoes()
    return df.to_dict('records')

@app.callback(
    Output("grafico-rentabilidade", "figure"),
    Input("tabela-transacoes", "data")
)

@app.callback(
    Output("painel-metricas", "children"),
    Input("tabela-transacoes", "data")
)
def atualizar_painel(transacoes):
    return painel()

def atualizar_grafico(transacoes):
    if not transacoes or len(transacoes) == 0:
        fig = go.Figure()
        fig.update_layout(
            title="Carteira vazia! Adicione ordens para visualizar o desempenho.",
            xaxis_title="Ativo",
            yaxis_title="Valor (R$)"
        )
        return fig
    
    df = pd.DataFrame(transacoes)
    
    # Converter para float (evita erro na plotagem)
    df["preco"] = df["preco"].astype(float)
    df["preco_atual"] = df["preco_atual"].astype(float)
    
    # Calcular valor total por ativo (quantidade * preço)
    df["valor_investido"] = df["quantidade"] * df["preco"]
    df["valor_atual"] = df["quantidade"] * df["preco_atual"]
    
    # Criar gráfico
    fig = {
        "data": [
            {"x": df["ativo"], "y": df["valor_investido"], "type": "bar", "name": "Valor Investido"},
            {"x": df["ativo"], "y": df["valor_atual"], "type": "bar", "name": "Valor Atual"},
        ],
        "layout": {
            "title": "Comparação: Investimento vs. Valor Atual"
        }
    }
    
    return fig

# Executar o app
if __name__ == '__main__':
    app.run(debug=True)