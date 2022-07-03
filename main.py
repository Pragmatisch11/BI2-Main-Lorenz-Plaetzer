# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas
import pandas as pd
import requests
import json
import IPython
import pandasgui as pdg
import matplotlib.pyplot as plt
from dash import Dash, html, dcc, dash_table
import plotly.express as px

def get_indicator_code(search):
    r = requests.get("https://ghoapi.azureedge.net/api/Indicator")
    r = r.json()["value"]
    # print(r["value"])
    for i in r:
        if search in i['IndicatorName']\
                and not "ARCHIVED" in i['IndicatorCode']:
            return i

def get_indicator_code_request(search):
    r = requests.get(("https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'" + search + "')"))
    return r

def get_dataframe_of_indicatorcode(IndicatorCode):
    r = requests.get("https://ghoapi.azureedge.net/api/" + IndicatorCode)
    r = r.json()["value"]
    r = json.dumps(r)
    df = pandas.read_json(r)
    #df.set_index('SpatialDim', inplace=True)
    #df = pd.DataFrame(r, index="SpatialDim")
    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    IndicatorCode = get_indicator_code(
        "Alcohol, drinkers only per capita (15+)consumption in litres of pure alcohol")['IndicatorCode']
    df = get_dataframe_of_indicatorcode(IndicatorCode)
    pandas.set_option('display.max_rows', df.shape[0] + 1, 'display.max_columns', df.shape[0] +1)

    sub_df = df[["SpatialDim", "NumericValue", "Dim1"]]

    sub_df = sub_df[sub_df.Dim1 != "BTSX"]

    sub_df = df[["SpatialDim", "NumericValue"]]
    sub_df = sub_df.groupby(["SpatialDim"]).sum()

    print(sub_df)

    #df = df.groupby([''])

    #print(df)

    #fig = px.choropleth(df, locations="iso_alpha",
    #                   color="")





    #app = Dash(__name__)
    #app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])
    #IPython.Application.d(r.style)

    #r = pandas.read_json(r.text)
    #pdg.show(r)
    #print(IndicatorCode)
    #data = pd.read_csv('')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
