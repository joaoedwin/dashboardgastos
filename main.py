import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Dados
categorias = ['Alimentação', 'Materiais Limpeza', 'Juros e Multas']
gastos_2023_setor2 = [5759.25, 2482.50, 19.67]
gastos_2024_setor2 = [5993.48, 4008.49, 48.39]
gastos_2024_uberlandia = [3343.04, 1475.47, 0]  # Não há informações sobre os juros e multas

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Estilo externo
external_stylesheets = ['/assets/styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout do aplicativo
app.layout = html.Div([
    html.H1('Dashboard de Gastos', className='text-center text-2xl font-bold mb-4'),
    html.Div([
        html.Button('2023 - Gastos Mensais do Setor 2', id='botao-2023-setor2', n_clicks=0, className='botao-menu mr-4 px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded'),
        html.Button('2024 - Gastos Mensais do Setor 2', id='botao-2024-setor2', n_clicks=0, className='botao-menu mr-4 px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded'),
        html.Button('2024 - Gastos Mensais Demais Setores', id='botao-2024-uberlandia', n_clicks=0, className='botao-menu mr-4 px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded'),
        html.Button('Comparação entre Setor 2 e Demais Setores Uberlândia', id='botao-comparacao', n_clicks=0, className='botao-menu px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded'),
    ], className='text-center mb-4'),  # Adicionando margem inferior entre os botões
    dcc.Graph(id='grafico-gastos')
])

# Callback para atualizar o gráfico com base no botão clicado
@app.callback(
    Output('grafico-gastos', 'figure'),
    [Input('botao-2023-setor2', 'n_clicks'),
     Input('botao-2024-setor2', 'n_clicks'),
     Input('botao-2024-uberlandia', 'n_clicks'),
     Input('botao-comparacao', 'n_clicks')]
)
def update_graph(n_clicks_2023_setor2, n_clicks_2024_setor2, n_clicks_2024_uberlandia, n_clicks_comparacao):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'botao-2023-setor2'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'botao-2023-setor2':
        gastos = gastos_2023_setor2
        titulo = 'Gastos Médios Mensais do Setor 2 em 2023'
    elif button_id == 'botao-2024-setor2':
        gastos = gastos_2024_setor2
        titulo = 'Gastos Médios Mensais do Setor 2 em 2024'
    elif button_id == 'botao-2024-uberlandia':
        gastos = gastos_2024_uberlandia
        titulo = 'Gastos Médios Mensais dos Demais Setores em Uberlândia em 2024'
    else:
        fig = go.Figure(data=[
            go.Bar(name='Setor 2', x=categorias, y=gastos_2024_setor2, text=['R$ {:.2f}'.format(valor) for valor in gastos_2024_setor2], textposition='auto', width=0.4),
            go.Bar(name='Demais Setores', x=categorias, y=gastos_2024_uberlandia, text=['R$ {:.2f}'.format(valor) for valor in gastos_2024_uberlandia], textposition='auto', width=0.4)
        ])
        fig.update_layout(barmode='group')
        return fig

    fig = go.Figure()
    fig.add_trace(go.Bar(x=categorias, y=gastos, text=['R$ {:.2f}'.format(valor) for valor in gastos], textposition='auto', width=0.4))
    fig.update_layout(title=titulo, xaxis_title='Categorias', yaxis_title='Gastos (R$)')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
