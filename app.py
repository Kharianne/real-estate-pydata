import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from graphs import get_comparison_graph, get_map_graph, get_buy_estimate_comp, get_ratio, new_vs_price
from helper import get_number_of_built_flats

comparison_fig = get_comparison_graph()
map_fig = get_map_graph()
estimate = get_buy_estimate_comp()
ratio = get_ratio()
new_vs_price = new_vs_price()

number_of_flats = get_number_of_built_flats()

app = dash.Dash(__name__)
server = app.server

app.title = 'Real estate analysis'
app.layout = html.Div(children=[
    html.H1(children='Comparison of flat prices and number of newly built flats'),
    html.Div(children='''
    A simple project for PyData Pyladies'''),
    dcc.Graph(figure=comparison_fig),
    dcc.Graph(figure=map_fig),
    dcc.Graph(figure=estimate),
    dcc.Graph(figure=ratio),
    html.Div([
            html.H2(children='Newly built flats between 2014 - 2018'),
            html.H3(children='You can select multiple regions'),
            dcc.Dropdown(
                id='kraj',
                options=[{'label': i, 'value': i} for i in number_of_flats.index],
                value=['Česká republika'],
                multi=True
            ),
        ],
        style={'width': '48%', 'display': 'inline-block', 'margin-top': '25px'}),
    dcc.Graph(id='indicator-graphic'),
    dcc.Graph(figure=new_vs_price)
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('kraj', 'value')])
def update_graph(kraj):
    fig = go.Figure()
    for k in kraj:
        fig.add_scatter(
            y=number_of_flats.loc[k].values,
            x=number_of_flats.loc[k].index,
            text=k,
            name=k)

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            title='Year'
        ),
        yaxis=dict(
            type='log',
            title='Number of built flats'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        title='Newly built flats between 2014 - 2018'
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)