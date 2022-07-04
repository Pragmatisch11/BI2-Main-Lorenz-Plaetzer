import pandas
import plotly.express as px

def get_heatmap_alcoholconsumption_btsx(df):

    sub_df = df[["SpatialDim", "NumericValue", "Dim1"]]

    sub_df = sub_df[sub_df.Dim1 != "BTSX"]
    # sub_df = sub_df.drop(sub_df[sub_df.Dim1 == "BTSX"].index)

    sub_df = sub_df[["SpatialDim", "NumericValue"]]

    sub_df = sub_df.groupby(["SpatialDim"]).sum()
    # sub_df = sub_df.reset_index()
    print(sub_df)

    fig = px.choropleth(sub_df, locations=sub_df.index,
                        color="NumericValue",
                        hover_name=sub_df.index,
                        color_continuous_scale=px.colors.sequential.Plasma)

    return fig