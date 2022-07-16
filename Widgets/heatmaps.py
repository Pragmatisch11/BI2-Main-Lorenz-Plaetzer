import pandas
import plotly.express as px

def get_heatmap_alcoholconsumption_btsx(df):

    sub_df = df[["Country", "NumericValue", "Dim1"]]

    sub_df = sub_df[sub_df.Dim1 != "BTSX"]
    # sub_df = sub_df.drop(sub_df[sub_df.Dim1 == "BTSX"].index)

    sub_df = sub_df[["Country", "NumericValue"]]

    sub_df = sub_df.groupby(["Country"]).sum()
    # sub_df = sub_df.reset_index()
    #print(sub_df)

    fig = px.choropleth(sub_df, locations=sub_df.index,
                        color="NumericValue",
                        hover_name=sub_df.index,
                        color_continuous_scale=px.colors.sequential.Plasma)

    return fig

def get_heatmap_alcoholconsumtion_rank_male(df):
    sub1_df = df[["Country", "NumericValue", "Dim1"]]
    sub1_df = sub1_df[sub1_df.Dim1 != "BTSX"]
    sub1_df = sub1_df[sub1_df.Dim1 != "FMLE"]
    sub1_df['WerteMax'] = sub1_df["NumericValue"].rank()
    sub1_df = sub1_df.sort_values(by=['WerteMax'], ascending=False)
    sub1_df = sub1_df[["Country", "NumericValue"]]
    #sub1_df["NumericValue"] = sub1_df["NumericValue"].astype(float)
    #sub1_df = sub1_df.convert_objects(convert_numeric=True)
    #sub1_df["NumericValue"] = sub1_df["NumericValue"].apply(pandas.to_numeric)


    ## DAMIT ÜBERSCHREIBST DU EINFACH DIE NaN MIT 0
    sub1_df['NumericValue'] = sub1_df["NumericValue"].fillna(0)

    fig = px.scatter_geo(sub1_df, locations=sub1_df.Country,
                          color="NumericValue", hover_name=sub1_df.Country,
                         title="Heatmap des Alkoholkonsums der Männer, aufgeteilt nach Land",
                          color_continuous_scale=px.colors.sequential.speed, size=sub1_df["NumericValue"])

    #print("Hier die sub1df")
    #print(sub1_df)

    return fig