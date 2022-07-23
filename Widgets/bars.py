import pandas
import plotly.express as px

import dataframe_handler
from dataframe_handler import *


def get_alcohol_consumption_barchart_per_continent(df, sex):
    df = df.rename(columns={"SpatialDim": "Country",
                            "NumericValue": "purer Alkoholkonsum in Litern"})
    df = df.query('Dim1 == "%s"' % sex)
    #df = dataframe_handler.add_continent_by_iso3_code(df[["Country", "TimeDim", "Dim1", "NumericValue"]])
    #df = df.drop(columns=["Country"])

    #ValueError: Value of 'x' is not the name of a column in 'data_frame'. Expected one of ['TimeDim', 'NumericValue'] but received: Continent
    #df = df.groupby(["Continent"]).sum()
    # Da sonst nicht bei beiden geschlechtern eine andere reihenfolge bei den ländern vorherrscht
    df = df.sort_values(by=['Continent'])
    print(f'Geschlecht {sex}:')
    print(df)
    #df = df.reset_index()
    fig = px.bar(df, x="Continent", y="purer Alkoholkonsum in Litern", color="Country",
                 hover_data=["CountryName", "purer Alkoholkonsum in Litern"])
    return fig


def get_top_and_last_alcohol_consumption_rank_per_country(df, sex):
    df = df.rename(columns={"SpatialDim": "Country",
                            "NumericValue": "purer Alkoholkonsum in Litern"})
    df = df.sort_values(by=["purer Alkoholkonsum in Litern"])
    df = df.query('Dim1 == "%s"' % sex)
    df = df[["Country", "purer Alkoholkonsum in Litern", "CountryName"]]
    #print("#############################")
    #print(df)
    df = df.dropna()
    #print(df)
    df = pandas.concat([df.head(5), df.tail(5)])
    fig = px.bar(df, x="Country", y="purer Alkoholkonsum in Litern",
                 hover_data=["CountryName", "purer Alkoholkonsum in Litern"])
    return fig

def get_pie_alcohol_consumption_per_country(df, sex):
    df = df.rename(columns={"SpatialDim": "Country",
                            "NumericValue": "purer Alkoholkonsum in Litern"})
    df.loc[df['purer Alkoholkonsum in Litern'] ]

    df = df.query('Dim1 == "%s"' % sex)

    return