import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import sqlite3
import order_manager


#inicializa o app
app = dash.Dash(__name__)

def carregar_transacoes():
    conexao = sqlite3.connect('carteira.db')
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY data DESC", conexao)
    conexao.close()

    return df

app.layout = html.Div(children=[
    html.H1("Controle de Carteira de Investimentos", style={'textAlign': 'center'}),

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
                {"name": "Data", "id": "data"}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'}
        ),
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

# Executar o app
if __name__ == '__main__':
    app.run(debug=True)