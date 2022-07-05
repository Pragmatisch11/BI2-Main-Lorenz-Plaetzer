# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas
import requests
import json
import plotly.express as px
from dash import Dash, html, dcc
import heatmaps as hm


def get_indicator_code(search):
    r = requests.get("https://ghoapi.azureedge.net/api/Indicator")
    r = r.json()["value"]
    # print(r["value"])
    for i in r:
        if search in i['IndicatorName'] \
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
    # df.set_index('SpatialDim', inplace=True)
    # df = pd.DataFrame(r, index="SpatialDim")
    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    IndicatorCode = get_indicator_code(
        "Alcohol, drinkers only per capita (15+)consumption in litres of pure alcohol")['IndicatorCode']
    df = get_dataframe_of_indicatorcode(IndicatorCode)
    pandas.set_option('display.max_rows', df.shape[0] + 1, 'display.max_columns', df.shape[0] + 1)

    print(IndicatorCode)
    fig = hm.get_heatmap_alcoholconsumption_btsx(df)

    # fig.show()

    ### Alex Bereich

    ##Bubble Map für Alkohol Consumption
    ## Indicator-Code lautet SA_0000001404 (https://ghoapi.azureedge.net/api/SA_0000001404)
    sub1_df = df[["SpatialDim", "NumericValue", "Dim1"]]
    sub1_df = sub1_df[sub1_df.Dim1 != "BTSX"]
    sub1_df = sub1_df[sub1_df.Dim1 != "FMLE"]
    sub1_df['WerteMax'] = sub1_df["NumericValue"].rank()
    sub1_df = sub1_df.sort_values(by=['WerteMax'], ascending=False)
    sub1_df = sub1_df[["SpatialDim", "NumericValue"]]
    ##Überschreiben der NaN werte durch 0, Länge des Dataframes bestimmen und dann die Tabelle durchgehen
    ##for i in range(sub1_df[sub1_df.Dim1].shape):
      ##  if i == "NaN":
        ##    sub1_df['Dim1'] = sub1_df['Dim1'].replace(['NaN'], '0')
         ##   break

    fig1 = px.scatter_geo(sub1_df, locations=sub1_df.index,
                          color="NumericValue", hover_name=sub1_df.index,
                          color_continuous_scale=px.colors.sequential.speed)

    print("Hier die sub1df")
    print(sub1_df)
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

        ##Neues HTML-Div für zweien Graphen

        html.Div([
            dcc.Graph(id='Bubble Map Men',
                      figure=fig1
                      )
        ])

    ])
    app.run_server(debug=True, use_reloader=False)
    # app.layout = dash_table.DataTable(x.to_dict('records'), [{"name": i, "id": i} for i in x.columns])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
