import pandas
import plotly.express as px

def get_heatmap_alcoholconsumption_btsx(df):

    sub_df = df[["SpatialDim", "NumericValue", "Dim1"]]

    sub_df = sub_df[sub_df.Dim1 != "BTSX"]
    # sub_df = sub_df.drop(sub_df[sub_df.Dim1 == "BTSX"].index)

    sub_df = sub_df[["SpatialDim", "NumericValue"]]

    sub_df = sub_df.groupby(["SpatialDim"]).sum()
    # sub_df = sub_df.reset_index()
    #print(sub_df)

    fig = px.choropleth(sub_df, locations=sub_df.index,
                        color="NumericValue",
                        hover_name=sub_df.index,
                        color_continuous_scale=px.colors.sequential.Plasma)

    return fig

def get_heatmap_alcoholconsumtion_rank_male(df):
    sub1_df = df[["SpatialDim", "NumericValue", "Dim1"]]
    sub1_df = sub1_df[sub1_df.Dim1 != "BTSX"]
    sub1_df = sub1_df[sub1_df.Dim1 != "FMLE"]
    sub1_df['WerteMax'] = sub1_df["NumericValue"].rank()
    sub1_df = sub1_df.sort_values(by=['WerteMax'], ascending=False)
    sub1_df = sub1_df[["SpatialDim", "NumericValue"]]
    #sub1_df["NumericValue"] = sub1_df["NumericValue"].astype(float)
    #sub1_df = sub1_df.convert_objects(convert_numeric=True)
    #sub1_df["NumericValue"] = sub1_df["NumericValue"].apply(pandas.to_numeric)


    ## DAMIT ÜBERSCHREIBST DU EINFACH DIE NaN MIT 0
    sub1_df['NumericValue'] = sub1_df["NumericValue"].fillna(0)

    ##Überschreiben der NaN werte durch 0, Länge des Dataframes bestimmen und dann die Tabelle durchgehen
    ##for i in range(sub1_df[sub1_df.Dim1].shape):
    ##  if i == "NaN":
    ##    sub1_df['Dim1'] = sub1_df['Dim1'].replace(['NaN'], '0')
    ##   break

    fig = px.scatter_geo(sub1_df, locations=sub1_df.SpatialDim,
                          color="NumericValue", hover_name=sub1_df.SpatialDim,
                          color_continuous_scale=px.colors.sequential.speed, size=sub1_df["NumericValue"])

    #print("Hier die sub1df")
    #print(sub1_df)

    return fig