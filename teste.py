from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Inicialização do aplicativo Dash
app = Dash(__name__)

# Carregar os dados do Excel
df = pd.read_excel('Desafio-Digital-2023.xlsx', sheet_name='Dados - Questão 1')
rend = pd.read_excel('Desafio-Digital-2023.xlsx', sheet_name='Dados - Questão 1')

# Calcular a renda de cada venda (quantidade x preço unitário)
rend['Renda'] = rend['Qtd'] * rend['Valor unitário']

# Calcular a renda total de cada unidade
renda_por_unidade = rend.groupby('Unidade')['Renda'].sum()

# Exibir a renda total por unidade
print(renda_por_unidade)






# Criar gráficos iniciais
fig_bar = px.bar(df, x="Unidade", y="Qtd", color="Produto", barmode="group")
fig_renda = px.bar(renda_por_unidade.reset_index(), x="Unidade", y="Renda", title="Renda por Unidade")

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

    dcc.Graph(id='grafico_quantidade_vendas', figure=fig_bar),

    html.H2('Resultado:'),
    html.Div(id='produto_mais_vendido'),
    
   

    
    dcc.Graph(id='grafico_quantidade_unidades'),
    
    html.H2('Resultado:'),
    html.Div(id='unidade_mais_vendeu'),
    dcc.Graph(id='grafico_renda_unidades', figure=fig_renda),
    
])

# Função para calcular a unidade que mais vendeu
def calcular_unidade_mais_vendeu(dataframe):
    unidade_mais_vendeu = dataframe.groupby('Unidade')['Qtd'].sum().idxmax()
    return unidade_mais_vendeu

# Função para calcular o produto mais vendido
def calcular_produto_mais_vendido(dataframe):
    produto_mais_vendido = dataframe.groupby('Produto')['Qtd'].sum().idxmax()
    return produto_mais_vendido

# Callback para atualização da unidade que mais vendeu
@app.callback(Output('unidade_mais_vendeu', 'children'), Input('lista_lojas', 'value'))
def update_unidade_mais_vendeu(value):
    if value == "Todas as Lojas":
        unidade_mais_vendeu = calcular_unidade_mais_vendeu(df)
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        unidade_mais_vendeu = calcular_unidade_mais_vendeu(tabela_filtrada)
    return f'A unidade que mais vendeu: {unidade_mais_vendeu}'

# Callback para atualização do produto mais vendido
@app.callback(Output('produto_mais_vendido', 'children'), Input('lista_lojas', 'value'))
def update_produto_mais_vendido(value):
    if value == "Todas as Lojas":
        produto_mais_vendido = calcular_produto_mais_vendido(df)
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        produto_mais_vendido = calcular_produto_mais_vendido(tabela_filtrada)
    return f'O produto mais vendido: {produto_mais_vendido}'

# Callback para atualização do gráfico de quantidades por unidade
@app.callback(Output('grafico_quantidade_unidades', 'figure'), Input('lista_lojas', 'value'))
def update_output_unidades(value):
    if value == "Todas as Lojas":
        fig_unidades = px.bar(df, x="Unidade", y="Qtd", color="Unidade", barmode="group", title='Quantidades de Vendas por Unidade')
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        fig_unidades = px.bar(tabela_filtrada, x="Unidade", y="Qtd", color="Unidade", barmode="group", title='Quantidades de Vendas por Unidade')
    return fig_unidades

# Callback para atualização do gráfico de produtos mais vendidos
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
