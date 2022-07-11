import pandas
import plotly.express as px

import dataframe_handler
from dataframe_handler import *


def get_alcohol_consumption_barchart_per_continent(df, sex):
    df = df.rename(columns={"SpatialDim": "Country"})
    df = df.query('Dim1 == "%s"' % sex)
    df = dataframe_handler.add_continent_by_iso3_code(df[["Country", "TimeDim", "Dim1", "NumericValue"]])
    #df = df.drop(columns=["Country"])

    #ValueError: Value of 'x' is not the name of a column in 'data_frame'. Expected one of ['TimeDim', 'NumericValue'] but received: Continent
    #df = df.groupby(["Continent"]).sum()
    print(df)
    df = df.reset_index()
    fig = px.bar(df, x="Continent", y="NumericValue", color="Country", title="Alkoholkonsum aufgeteilt nach Kontinent")
    return fig