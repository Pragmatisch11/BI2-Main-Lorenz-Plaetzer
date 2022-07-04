# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas
import requests
import json
from dash import Dash, html, dcc
import heatmaps as hm

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
    print("hello")
    print("Alex")
    IndicatorCode = get_indicator_code(
        "Alcohol, drinkers only per capita (15+)consumption in litres of pure alcohol")['IndicatorCode']
    df = get_dataframe_of_indicatorcode(IndicatorCode)
    pandas.set_option('display.max_rows', df.shape[0] + 1, 'display.max_columns', df.shape[0] +1)

    fig = hm.get_heatmap_alcoholconsumption_btsx(df)

    #fig.show()

    app = Dash(__name__)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
    app.run_server(debug=True, use_reloader=False)
    #app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
