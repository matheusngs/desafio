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

# Calcular o total de vendas da empresa
total_vendas = df['Qtd'].sum()

# Calcular a coluna 'Porcentagem de Vendas' para cada produto
df['Porcentagem de Vendas'] = (df['Qtd'] / total_vendas) * 100


# Função para calcular o desconto com base na renda
def calcular_desconto(renda):
    if renda <= 2100000:
        return renda * 0.05
    elif 2100000 < renda <= 2400000:
        return renda * 0.12
    else:
        return renda * 0.17

# Calcular a renda total e o desconto de cada unidade
renda_por_unidade = rend.groupby('Unidade')['Renda'].sum()
desconto_por_unidade = renda_por_unidade.apply(calcular_desconto)
soma_descontos = list(renda_por_unidade)



# Criar gráficos iniciais
fig_bar = px.bar(df, x="Unidade", y="Qtd", color="Produto", barmode="group")
fig_renda = px.bar(renda_por_unidade.reset_index(), x="Unidade", y="Renda", title="Renda por Unidade")
fig_desconto = px.bar(desconto_por_unidade.reset_index(), x="Unidade", y="Renda", title="Desconto por Unidade")
fig_porcentagem_vendas = px.bar(df, x='Produto', y='Porcentagem de Vendas', color='Produto', title='Porcentagem de Vendas por Produto')


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

    dcc.Graph(id='grafico_desconto_unidades', figure=fig_desconto),
    html.H2(f'O valor total dos descontos é  R${sum(soma_descontos)},00'),
    
    dcc.Graph(id='grafico_porcentagem_vendas', figure=fig_porcentagem_vendas),
])

# Callback para atualização da unidade que mais vendeu
@app.callback(Output('unidade_mais_vendeu', 'children'), Input('lista_lojas', 'value'))
def update_unidade_mais_vendeu(value):
    if value == "Todas as Lojas":
        unidade_mais_vendeu = df.groupby('Unidade')['Qtd'].sum().idxmax()
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        unidade_mais_vendeu = tabela_filtrada.groupby('Unidade')['Qtd'].sum().idxmax()
    return f'A unidade que mais vendeu: {unidade_mais_vendeu}'

# Callback para atualização do produto mais vendido
@app.callback(Output('produto_mais_vendido', 'children'), Input('lista_lojas', 'value'))
def update_produto_mais_vendido(value):
    if value == "Todas as Lojas":
        produto_mais_vendido = df.groupby('Produto')['Qtd'].sum().idxmax()
    else:
        tabela_filtrada = df.loc[df['Unidade'] == value, :]
        produto_mais_vendido = tabela_filtrada.groupby('Produto')['Qtd'].sum().idxmax()
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
