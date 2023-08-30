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

# Calcular os descontos nas rendas com base nas faixas de renda
def calcular_desconto_renda(renda):
    if renda <= 2100000:
        return renda * 0.05
    elif 2100000 < renda <= 2400000:
        return renda * 0.12
    else:
        return renda * 0.17

rend['Desconto Renda'] = rend['Renda'].apply(calcular_desconto_renda)

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
# ...   

# Função para calcular o produto mais vendido
# ...

# Callback para atualização da unidade que mais vendeu
# ...

# Callback para atualização do produto mais vendido
# ...

# Callback para atualização do gráfico de quantidades por unidade
# ...

# Callback para atualização do gráfico de produtos mais vendidos
# ...

# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
