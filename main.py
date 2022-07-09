# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
from typing import io

import pandas
import json
import plotly.express as px
from dash import Dash, html, dcc
import heatmaps as hm
import request_handler as r
import matplotlib.pyplot as plt
import plotly.tools as tls

# import pycountry


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ## Dataframe Alcohol Consumption per country
    ## Indicator-Code lautet SA_0000001404 (https://ghoapi.azureedge.net/api/SA_0000001404)
    IndicatorCode = r.get_indicator_code(
        "Alcohol, drinkers only per capita (15+)consumption in litres of pure alcohol")['IndicatorCode']
    df_alcohol_consumption_per_country = r.get_dataframe_by_indicatorcode(IndicatorCode)
    pandas.set_option('display.max_rows', df_alcohol_consumption_per_country.shape[0] + 1, 'display.max_columns',
                      df_alcohol_consumption_per_country.shape[0] + 1)

    ## Dataframe Age-standardized suicide rates (per 100 000 population)
    # IndicatorCode = r.get_indicator_code("Age-standardized suicide rates (per 100 000 population)")['IndicatorCode']
    # df_suicide_rates = r.get_dataframe_by_indicatorcode(IndicatorCode)
    # # zeige nur einträge aus dem jahr 2016
    # #print(df_suicide_rates.query("TimeDim == 2016"))
    #
    # ## Dataframe HALE Life expectancy at birth
    # ## Indicator-Code lautet WHOSIS_000002 (https://ghoapi.azureedge.net/api/WHOSIS_000002)
    # IndicatorCode = r.get_indicator_code("Healthy life expectancy (HALE) at birth (years)")['IndicatorCode']
    # df_hale = r.get_dataframe_by_indicatorcode(IndicatorCode)
    # # zeige nur einträge aus dem jahr 2019
    # #print(df_hale.query("TimeDim == 2019"))
    #
    # ## Dataframe Mean BMI age standardized estimate
    # IndicatorCode = r.get_indicator_code("Mean BMI (kg/m\u00b2) (age-standardized estimate)")['IndicatorCode']
    # df_bmi = r.get_dataframe_by_indicatorcode(IndicatorCode)
    # print(df_bmi.query("TimeDim == 2016"))

    ## Dataframe Death Rate per 100.000 Alzheimers & Dementia
    # https://www.worldlifeexpectancy.com/cause-of-death/alzheimers-dementia/by-country/female
    # Female:
    #df_alz_dem_lifeexpectancy_f = r.get_dataframe_by_csv("./Alzheimers_Dementia_Female.csv")
    # Male:
    #df_alz_dem_lifeexpectancy_m = r.get_dataframe_by_csv("./Alzheimers_Dementia_Male.csv")
    # BTSX:
    df_alz_dem_lifeexpectancy_b = r.get_dataframe_by_csv("./Alzheimers_Dementia_BTSX.csv")

    # Konvertieren der ausgeschriebenen Country-Namen zu ISO 3 mittels country-converter
    df_alz_dem_lifeexpectancy_b = r.modify_country_codes(df_alz_dem_lifeexpectancy_b)
    #df_alz_dem_lifeexpectancy_f = r.modify_country_codes(df_alz_dem_lifeexpectancy_f)
    #df_alz_dem_lifeexpectancy_m = r.modify_country_codes(df_alz_dem_lifeexpectancy_m)

    sub_df_alcohol_consumption_per_country = df_alcohol_consumption_per_country.rename(columns={"SpatialDim":"Country"})
    print(sub_df_alcohol_consumption_per_country[["Country", "NumericValue"]], df_alz_dem_lifeexpectancy_b)
    x = pandas.merge(sub_df_alcohol_consumption_per_country.query('Dim1 == "BTSX"')[["Country", "NumericValue"]],
                     df_alz_dem_lifeexpectancy_b, on="Country")
    print(x)

    fig3 = px.scatter(x,x='Rate',y='NumericValue')

    #data = base64.b64encode(buf.getbuffer()).decode("utf8")


    # print(df_alz_dem_lifeexpectancy_f, df_alz_dem_lifeexpectancy_m, df_alz_dem_lifeexpectancy_b)
    ## Heatmap für Alcohol Consumpion BTSX
    fig = hm.get_heatmap_alcoholconsumption_btsx(df_alcohol_consumption_per_country)

    ### Alex Bereich ###

    ##Bubble Map für Alkohol Consumption
    fig1 = hm.get_heatmap_alcoholconsumtion_rank_male(df_alcohol_consumption_per_country)

    ##print(df)

    #### Dash Server
    app = Dash(__name__)

    app.layout = html.Div(children=[

        html.Div([

            html.H1(children='Hello Dash'),


            html.Div(children='''
            Dash: A web application framework for your data.
        '''),

            ##Graph 1
            dcc.Graph(
                id='example-graph',
                figure=fig

            ),
        ]),

        html.Div([
            dcc.Graph(id='Korrelation',
                      figure=fig3
                      ),


        ]),


        ##Neues HTML-Div für zweiten Graphen

        html.Div([
            dcc.Graph(id='Bubble Map Men',
                      figure=fig1
                      ),
        ])

    ])
    app.run_server(debug=True, use_reloader=False)
    # app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
