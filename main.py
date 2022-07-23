# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import Widgets as w
from Widgets import heatmaps, scatters, bars
import request_handler as r
#import matplotlib.pyplot as plt
import plotly.tools as tls
import statsmodels
import dataframe_handler as dfh


def get_alcohol_consumption_df():
    ## Dataframe Alcohol Consumption per country
    ## Indicator-Code lautet SA_0000001404 (https://ghoapi.azureedge.net/api/SA_0000001404)
    ## https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-recorded-per-capita-(15-)-consumption-(in-litres-of-pure-alcohol)
    IndicatorCode = r.get_indicator_code(
        "Alcohol, drinkers only per capita (15+)consumption in litres of pure alcohol")['IndicatorCode']
    return r.get_dataframe_by_indicatorcode(IndicatorCode)


def get_suicide_rates_df():
    ## Dataframe Age-standardized suicide rates (per 100 000 population)
    IndicatorCode = r.get_indicator_code("Age-standardized suicide rates (per 100 000 population)")['IndicatorCode']
    return r.get_dataframe_by_indicatorcode(IndicatorCode)


def get_hale_df():
    # ## Dataframe HALE Life expectancy at birth
    # ## Indicator-Code lautet WHOSIS_000002 (https://ghoapi.azureedge.net/api/WHOSIS_000002)
    IndicatorCode = r.get_indicator_code("Healthy life expectancy (HALE) at birth (years)")['IndicatorCode']
    return r.get_dataframe_by_indicatorcode(IndicatorCode)


def get_bmi_df():
    # ## Dataframe Mean BMI age standardized estimate
    IndicatorCode = r.get_indicator_code("Mean BMI (kg/m\u00b2) (age-standardized estimate)")['IndicatorCode']
    # print(df_bmi.query("TimeDim == 2016"))
    return r.get_dataframe_by_indicatorcode(IndicatorCode)


def get_alz_dem_deathrate_f_df():
    ## Dataframe Death Rate per 100.000 Alzheimers & Dementia
    # https://www.worldlifeexpectancy.com/cause-of-death/alzheimers-dementia/by-country/female
    return r.get_dataframe_by_csv("./Alzheimers_Dementia_Female.csv")


def get_alz_dem_deathrate_m_df():
    ## Dataframe Death Rate per 100.000 Alzheimers & Dementia
    # https://www.worldlifeexpectancy.com/cause-of-death/alzheimers-dementia/by-country/male
    return r.get_dataframe_by_csv("./Alzheimers_Dementia_Male.csv")


def get_alz_dem_deathrate_b_df():
    ## Dataframe Death Rate per 100.000 Alzheimers & Dementia
    # https://www.worldlifeexpectancy.com/cause-of-death/alzheimers-dementia/by-country/female
    return r.get_dataframe_by_csv("./Alzheimers_Dementia_BTSX.csv")


def get_country_population_df():
    # https://data.worldbank.org/indicator/SP.POP.TOTL
    return r.get_dataframe_by_csv("./Country_Population.csv")

def dropdown_sex(p_id):
    return html.Div([
        dcc.Dropdown(
            [
                {
                    "label": html.Div(
                        [
                            html.Img(src="/assets/images/sex_icons/female.svg", height=20),
                            html.Div("Weiblich", style={'font-size': 15, 'padding-left': 10}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "FMLE",
                },
                {
                    "label": html.Div(
                        [
                            html.Img(src="assets/images/sex_icons/male.svg", height=20),
                            html.Div("Männlich", style={'font-size': 15, 'padding-left': 10}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "MLE",
                },
                {
                    "label": html.Div(
                        [
                            html.Img(src="assets/images/sex_icons/btsx.svg", height=20),
                            html.Div("Beide Geschlechter", style={'font-size': 15, 'padding-left': 10}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                    ),
                    "value": "BTSX",
                },
            ],
            id=p_id,
            value="BTSX",
            clearable=False,
        ),
    ])

df_alcohol_consumption = get_alcohol_consumption_df()
df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})
df_alcohol_consumption = dfh.add_continent_by_iso3_code(df_alcohol_consumption)
df_alcohol_consumption = dfh.add_full_country_name_by_iso3_code(df_alcohol_consumption)

# pandas.set_option('display.max_rows', df_alcohol_consumption.shape[0] + 1, 'display.max_columns', df_alcohol_consumption.shape[0] + 1)

df_alz_dem_deathrate_b = get_alz_dem_deathrate_b_df()
# Konvertieren der ausgeschriebenen Country-Namen zu ISO 3 mittels country-converter
df_alz_dem_deathrate_b = dfh.modify_country_codes(df_alz_dem_deathrate_b)

df_hale = get_hale_df()
df_hale = df_hale.rename(columns={"SpatialDim": "Country"})

df_bmi = get_bmi_df()


df_pop = get_country_population_df()

## Heatmap für Alcohol Consumpion BTSX
#fig = w.heatmaps.get_heatmap_alcoholconsumption(df_alcohol_consumption)

### Alex Bereich ###

##Bubble Map für Alkohol Consumption
#fig1 = w.heatmaps.get_bubblemap_alcoholconsumtion(df_alcohol_consumption)

fig2 = w.scatters.get_scatter_alcohol_demalz_hale_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_hale)

fig3 = w.scatters.get_scatter_alcohol_demalz_bmi_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_bmi)

#fig4 = w.bars.get_alcohol_consumption_barchart_per_continent(df_alcohol_consumption, "BTSX")

fig6 = w.scatters.get_scatter_alcohol_population_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_pop)

#fig7 = w.scatters.test_get_scatter_alcohol_bmi_population_scatter(df_alcohol_consumption, df_bmi, df_pop, "1960")


#### Dash Server
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

url_bar_and_content_div = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

index_page = html.Div([

    html.H1('Eine Analyse des weltweiten Alkoholkonsums'),
    #html.Br(),
    html.H2('Aufbereitung mittels Dash und Plotly'),
    dcc.Link('Zur Aufbereitung mittels Bar Plots', href='/page-bar'),
    html.Br(),
    dcc.Link('Zur Aufbereitung mittels Scatter Plots', href='/page-scatter'),


    ##Graph 1
    html.Div([
        html.H5('Alkoholkonsum in puren Litern weltweit nach Geschlecht; Darstellung mittels einer Heatmap'),
        dropdown_sex("DropdownSex_heatmap_alcoholconsumption"),

        dcc.Graph(
            id='heatmap_alcoholconsumption',
        ),
    ]),


    ##Neues HTML-Div für zweiten Graphen

    html.Div([
        html.H5('Alkoholkonsum in puren Litern weltweit nach Geschlecht; Darstellung mittels einer Bubblemap'),
        dropdown_sex("DropdownSex_bubblemap_alcoholconsumption"),
        dcc.Graph(id='bubblemap_alcoholconsumption'),
    ]),



])
layout_scatter_page = html.Div([
    html.H3('Eine Aufbereitung mittels Scatter Plots'),
    html.Div([
        html.H5('Auswertung über den Zusammenhang von Alkoholkonsum, '
                'Demenz und Alzheimer Todesrate und Lebenserwartung'),
        dcc.Graph(id='Korrelation',
                  figure=fig2
                  ),

    ]),
    html.Div([
        html.H5('Auswertung über den Zusammenhang von Alkoholkonsum, Demenz und Alzheimer Todesrate und BMI'),
        dcc.Graph(id='Korrelation2',
                  figure=fig3
                  ),

    ]),

    html.Div([
        html.H5('Auswertung über den Zusammenhang von Alkoholkonsum, '
                'Demenz und Alzheimer Todesrate und der Einwohnerzahl'),
        dcc.Graph(id='Korrelation3',
                  figure=fig6
                  ),

    ]),

    html.Div([
        html.H5('Auswertung über den Zusammenhang von Alkoholkonsum, BMI und Einwohnerzahl'),
        dcc.Graph(id='scatter_alcohol_bmi_population_scatter'),
        dcc.Slider(1960, 2021, 1, value=2016, id='SliderYear_scatter_alcohol_bmi_population_scatter',
                   marks={key: str(key) for key in range(1960, 2021, 5)},
                   tooltip={"placement": "bottom", "always_visible": True})

    ]),



    dcc.Link('Zurück zur Startseite', href='/'),
])
layout_bar_page = html.Div([
    html.H3('Eine Aufbereitung mittels Bar Plots'),
    html.Div([
        html.H5('Alkoholkonsum aufgeteilt nach Kontinent'),
        dropdown_sex('DropdownSex_alcohol_consumption_per_continent'),
        dcc.Graph(id='Bar_alcohol_consumption_per_continent'),
    ]),

    html.Div([
        html.H5('Top 5 und Last 5 Länder hinsichtlich des Alkoholkonsum in Litern'),
        dropdown_sex('DropdownSex_top_and_last_alcohol_consumption_rank_per_country'),
        dcc.Graph(id='Bar_top_and_last_alcohol_consumption_rank_per_country'),
    ]),

    dcc.Link('Zurück zur Startseite', href='/'),
])

#https://dash.plotly.com/urls#dynamically-create-a-layout-for-multi-page-app-validation
app.layout = url_bar_and_content_div
app.validation_layout = html.Div([
    url_bar_and_content_div,
    index_page,
    layout_bar_page,
    layout_scatter_page,
])


# Index Page Callbacks
@app.callback(
    Output("heatmap_alcoholconsumption", "figure"),
    Input("DropdownSex_heatmap_alcoholconsumption", "value"))
def update_heatmap_alcoholconsumption(sex):
    fig = w.heatmaps.get_heatmap_alcoholconsumption(df_alcohol_consumption, sex)
    return fig


@app.callback(
    Output("bubblemap_alcoholconsumption", "figure"),
    Input("DropdownSex_bubblemap_alcoholconsumption", "value"))
def update_heatmap_alcoholconsumption(sex):
    fig = w.heatmaps.get_bubblemap_alcoholconsumtion(df_alcohol_consumption, sex)
    return fig

# Bar Page Callbacks
@app.callback(
    Output("Bar_alcohol_consumption_per_continent", "figure"),
    Input("DropdownSex_alcohol_consumption_per_continent", "value"))
def update_alcohol_consumption_barchart_per_continent(sex):
    fig = w.bars.get_alcohol_consumption_barchart_per_continent(df_alcohol_consumption, sex)
    return fig

@app.callback(
    Output("Bar_top_and_last_alcohol_consumption_rank_per_country", "figure"),
    Input("DropdownSex_top_and_last_alcohol_consumption_rank_per_country", "value"))
def update_top_and_last_alcohol_consumption_rank_per_country(sex):
    fig = w.bars.get_top_and_last_alcohol_consumption_rank_per_country(df_alcohol_consumption, sex)
    return fig

# Scatter Page Callback
@app.callback(
    Output("scatter_alcohol_bmi_population_scatter", "figure"),
    Input("SliderYear_scatter_alcohol_bmi_population_scatter", "value"))
def update_scatter_alcohol_bmi_population_scatter(year):
    fig = w.scatters.get_scatter_alcohol_bmi_population_scatter(df_alcohol_consumption, df_bmi, df_pop, str(year))
    #fig = fig.update_traces(marker_sizeref=2 * max(f'Country Population of {year}') / (40. ** 2),
    #                        selector=dict(type='scatter'))
    return fig

# Update the index
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-bar':
        return layout_bar_page
    if pathname == '/page-scatter':
        return layout_scatter_page
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
