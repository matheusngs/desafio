from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Inicialização do aplicativo Dash
app = Dash(__name__)

# Carregar os dados do Excel
df = pd.read_excel('Desafio-Digital-2023.xlsx', sheet_name='Dados - Questão 1')

# Criar gráficos iniciais
fig = px.bar(df, x="Unidade", y="Qtd", color="Produto", barmode="group")
fig2 = px.pie(df, names='Produto', title='Produtos mais Vendidos')

# Opções para o Dropdown
opcoes = list(df['Unidade'].unique())
opcoes.append("Todas as Lojas")

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com os produtos mais vendidos'),
    html.Div(children='''
        Selecione uma loja:
    '''),

    dcc.Dropdown(options=[{'label': opcao, 'value': opcao} for opcao in opcoes],
                 value='Todas as Lojas', id='lista_lojas'),

    dcc.Graph(id='grafico_quantidade_vendas', figure=fig),
    dcc.Graph(id='Loja-mais-vendas', figure=fig2)
])

# Callback para atualização do gráfico
@app.callback(Output('grafico_quantidade_vendas', 'figure'), Input('lista_lojas', 'value'))
def update_output(value):
    if value == "Todas as Lojas":
        figura_atualizada = px.bar(df, x="Unidade", y="Qtd", color="Produto", barmode="group")
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        figura_atualizada = px.bar(tabela_filtrada, x="Unidade", y="Qtd", color="Produto", barmode="group")
    return figura_atualizada

# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
