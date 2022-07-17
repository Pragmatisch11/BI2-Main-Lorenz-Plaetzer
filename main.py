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
import matplotlib.pyplot as plt
import plotly.tools as tls
import statsmodels
import dataframe_handler as dfh


def get_alcohol_consumption_df():
    ## Dataframe Alcohol Consumption per country
    ## Indicator-Code lautet SA_0000001404 (https://ghoapi.azureedge.net/api/SA_0000001404)
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


df_alcohol_consumption = get_alcohol_consumption_df()
df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})
df_alcohol_consumption = dfh.add_continent_by_iso3_code(df_alcohol_consumption)


# pandas.set_option('display.max_rows', df_alcohol_consumption.shape[0] + 1, 'display.max_columns', df_alcohol_consumption.shape[0] + 1)

df_alz_dem_deathrate_b = get_alz_dem_deathrate_b_df()
# Konvertieren der ausgeschriebenen Country-Namen zu ISO 3 mittels country-converter
df_alz_dem_deathrate_b = dfh.modify_country_codes(df_alz_dem_deathrate_b)

df_hale = get_hale_df()
df_hale = df_hale.rename(columns={"SpatialDim": "Country"})

df_bmi = get_bmi_df()


df_pop = get_country_population_df()

## Heatmap für Alcohol Consumpion BTSX
fig = w.heatmaps.get_heatmap_alcoholconsumption_btsx(df_alcohol_consumption)

### Alex Bereich ###

##Bubble Map für Alkohol Consumption
fig1 = w.heatmaps.get_heatmap_alcoholconsumtion_rank_male(df_alcohol_consumption)

fig2 = w.scatters.get_scatter_alcohol_demalz_hale_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_hale)

fig3 = w.scatters.get_scatter_alcohol_demalz_bmi_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_bmi)

#fig4 = w.bars.get_alcohol_consumption_barchart_per_continent(df_alcohol_consumption, "BTSX")

fig6 = w.scatters.get_scatter_alcohol_population_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_pop)

fig7 = w.scatters.get_scatter_alcohol_bmi_population_scatter(df_alcohol_consumption, df_bmi, df_pop)


#### Dash Server
app = Dash(__name__)

app.layout = html.Div(children=[

    html.Div([

        html.H1(children='Hello Dash'),

        html.Div(children='''Dash: A web application framework for your data.'''),

        ##Graph 1
        dcc.Graph(
            id='example-graph',
            figure=fig

        ),

        ##Neues HTML-Div für zweiten Graphen

        html.Div([
            dcc.Graph(id='Bubble Map Men',
                      figure=fig1
                      ),
        ]),

        html.Div([
            dcc.Graph(id='Korrelation',
                      figure=fig2
                      ),

        ]),
        html.Div([
            dcc.Graph(id='Korrelation2',
                      figure=fig3
                      ),

        ]),

        html.Div([
            html.H4('Scatter Plot mit Country Population of 2016, y-Achse dementia rate'),
            dcc.Graph(id='Korrelation3',
                      figure=fig6
                      ),

        ]),

        html.Div([
            html.H4('Scatter Plot mit Country Population of 2016, y-Achse BMI'),
            dcc.Graph(id='Korrelation4',
                      figure=fig7
                      ),

        ]),
        html.Div([
            dcc.Dropdown(
                id="dropdown1",
                options=["BTSX", "FMLE", "MLE"],
                value="BTSX",
                clearable=False,
            ),
            dcc.Graph(id='Bar1'),

        ]),
    ], style={'margin': 'auto'}),

])


@app.callback(
    Output("Bar1", "figure"),
    Input("dropdown1", "value"))
def update_alcohol_consumption_barchart_per_continent(sex):
    fig5 = w.bars.get_alcohol_consumption_barchart_per_continent(df_alcohol_consumption, sex)
    return fig5


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    # app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
