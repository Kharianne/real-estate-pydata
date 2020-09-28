import pandas as pd
import plotly.express as px
import requests
import plotly.graph_objects as go
from helper import get_number_of_built_flats


avg_2018 = pd.read_csv('data/avg_2016-2018.csv', dtype={'kupni_cena': 'Int64', 'odhadni_cena': 'Int64'})
avg_2017 = pd.read_csv('data/avg_2015-2017.csv', dtype={'kupni_cena': 'Int64', 'odhadni_cena': 'Int64'})
avg_2016 = pd.read_csv('data/avg_2014-2016.csv', dtype={'kupni_cena': 'Int64', 'odhadni_cena': 'Int64'})


def get_comparison_graph():
    avg_2018['pomer'] = avg_2018['kupni_cena'] / avg_2018['odhadni_cena']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=avg_2016['kraj'],
                         y=avg_2016['kupni_cena'],
                         name='Avg 2014 - 2016',
                         marker_color='rgb(173,216,230)'
                         ))
    fig.add_trace(go.Bar(x=avg_2017['kraj'],
                         y=avg_2017['kupni_cena'],
                         name='Avg 2015 - 2017',
                         marker_color='rgb(55, 83, 109)'
                         ))

    fig.add_trace(go.Bar(x=avg_2018['kraj'],
                         y=avg_2018['kupni_cena'],
                         name='Avg 2016 - 2018',
                         marker_color='rgb(30,144,255)'
                         ))

    fig.update_layout(
        title={
            'text': 'Flat prices in the Czech republic',
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='CZK for square meter',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def get_map_graph():
    eu_geojson = requests.get(
        "https://ec.europa.eu/eurostat/cache/GISCO/distribution/v2/nuts/geojson/NUTS_RG_01M_2016_4326_LEVL_3.geojson")\
        .json()

    cz_features = []
    for feature in eu_geojson['features']:
        if feature['properties']['CNTR_CODE'] == "CZ":
            cz_features.append(feature)
        if len(cz_features) == 14:
            break

    eu_geojson['features'] = cz_features

    fig = px.choropleth_mapbox(avg_2018, geojson=eu_geojson,
                               title='Average price in 2016-2018 data period',
                               locations='kraj',
                               color='kupni_cena',
                               featureidkey='properties.NUTS_NAME',
                               color_continuous_scale="Blues",
                               range_color=(0, 60000),
                               mapbox_style="carto-positron",
                               zoom=6,
                               center={"lat": 50.0902, "lon": 14.7129},
                               opacity=0.5,
                               labels={'kupni_cena': 'Kupní cena za m2'}
                               )
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                      title='Average price in 2016-2018 data period',
                      paper_bgcolor = 'rgba(0,0,0,0)')
    return fig


def get_buy_estimate_comp():
    avg_2018_in = avg_2018.set_index('kraj')
    fig = go.Figure()

    fig.add_trace(go.Bar(x=avg_2018_in.index,
                         y=avg_2018_in['kupni_cena'],
                         name='Average buy price 2016-2018',
                         marker_color='rgb(173,216,230)'
                         ))
    fig.add_trace(go.Bar(x=avg_2018_in.index,
                         y=avg_2018_in['odhadni_cena'],
                         name='Average estimate price 2016-2018',
                         marker_color='rgb(55, 83, 109)'
                         ))

    fig.update_layout(
        title={
            'text': 'Comparison of buy price and estimation of value',
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='CZK for square meter',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


def get_ratio():
    avg_2018_in = avg_2018.set_index('kraj')
    avg_2018_in = avg_2018_in.sort_values('pomer')
    fig = go.Figure(
        data=go.Bar(x=avg_2018_in.index, y=avg_2018_in['pomer'], marker_color='#1e5262')
    )
    fig.update_layout(
        title={
            'text': 'Ratio between estimate price and buy price.',
        },
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Ratio',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def new_vs_price():
    avg_2018_in = avg_2018.set_index('kraj')
    number_of_built_flats = get_number_of_built_flats()
    number_of_built_flats['buy_price'] = avg_2018_in['kupni_cena']
    number_of_built_flats = number_of_built_flats.drop('Česká republika')

    fig = go.Figure(data=go.Scatter(
        x=number_of_built_flats[2018],
        y=number_of_built_flats['buy_price'],
        mode='markers',
        marker_color=number_of_built_flats['buy_price'],
        marker_colorscale='teal',
        text=number_of_built_flats.index,
        marker_size=number_of_built_flats[2018] / 100,
        marker_showscale=True

    ))
    fig.update_layout(
        title="Comparison of price per square meter and number of newly built flats in given region",
        xaxis_title="Number of newly built flats",
        yaxis_title="Price per square meter",
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
