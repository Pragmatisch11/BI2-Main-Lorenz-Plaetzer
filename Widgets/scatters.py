import matplotlib.pyplot as plt
import pandas
import plotly.express as px
from sklearn import preprocessing as pre
import dataframe_handler as dfh


def get_scatter_alcohol_demalz_hale_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_hale):
    # sub_df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})
    df_hale = df_hale.rename(columns={"SpatialDim": "Country"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_alz_dem_deathrate_b, on="Country")

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption",
                                      "Rate": "Dementia and Alzheimers Death Rate per 100000"})

    # unsinnig diese trendlinie, da überhaupt keine korrelation
    # fig3 = px.scatter(x,x='Alcoholconsumption',
    # y='Dementia and Alzheimers Death Rate per 100000', trendline="ols",size_max=1000)

    # Auf Basis von ISO3-Codes hinzufügen der Continent Namen
    # scatter = dfh.add_continent_by_iso3_code(scatter)

    # Merge von Lebenserwartung
    # scatter = scatter.assign(HALE=None)
    # print(df_hale)
    print("----------############-------------")

    df_hale = df_hale.query('Dim1 == "%s"' % "BTSX")
    df_hale = df_hale.groupby(["Country"]).mean()
    df_hale = df_hale.reset_index()
    print(df_hale)
    print("----------############-------------")

    scatter = pandas.merge(scatter, df_hale[["Country", "Value"]], on=["Country"])

    scatter = scatter.rename(columns={"Value": "HALE"})

    # print(scatter)
    fig = px.scatter(scatter, x='Alcoholconsumption', y='Dementia and Alzheimers Death Rate per 100000',
                     color='Continent', size='HALE')
    return fig


def get_scatter_alcohol_demalz_bmi_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_bmi):
    # sub_df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})
    df_bmi = df_bmi[["SpatialDim", "TimeDim", "Dim1", "NumericValue"]].rename(columns={"SpatialDim": "Country",
                                                                                       "NumericValue": "BMI"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_alz_dem_deathrate_b, on="Country")

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption",
                                      "Rate": "Dementia and Alzheimers Death Rate per 100000"})

    # unsinnig diese trendlinie, da überhaupt keine korrelation
    # fig3 = px.scatter(x,x='Alcoholconsumption',
    # y='Dementia and Alzheimers Death Rate per 100000', trendline="ols",size_max=1000)

    # Auf Basis von ISO3-Codes hinzufügen der Continent Namen
    # scatter = dfh.add_continent_by_iso3_code(scatter)

    print("----------############-------------")

    df_bmi = df_bmi.query('Dim1 == "%s"' % "BTSX")
    df_bmi = df_bmi.groupby(["Country"]).mean()

    scatter = pandas.merge(scatter, df_bmi, on=["Country"])
    scatter = scatter.dropna()
    print(scatter)
    fig = px.scatter(scatter, x='Alcoholconsumption', y='Dementia and Alzheimers Death Rate per 100000',
                     color='Continent', size='BMI')

    return fig


def get_scatter_alcohol_population_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_pop):

    # sub_df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})

    # Country Population noch umbennen mit dem Divisionsfaktor (zB divided by 10000)
    df_pop = df_pop[["Country Code", "2016"]].rename(columns={"Country Code": "Country",
                                                              "2016": "Country Population of 2016"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_alz_dem_deathrate_b, on="Country")

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption",
                                      "Rate": "Dementia and Alzheimers Death Rate per 100000"})


    scatter = pandas.merge(scatter, df_pop, on=["Country"])
    scatter['Country Population of 2016'] = scatter["Country Population of 2016"].fillna(0)
    #scatter['Country Population of 2016'] = scatter['Country Population of 2016'] / 10000

    #Test mit MinMaxScaler zur besseren Darstellung der Bubblegrößen
    scaler = pre.MinMaxScaler()
    scatter['Country Population of 2016'] = scaler.fit_transform(scatter[['Country Population of 2016']].to_numpy())




    ##Continent einfügen

    #x='Alcoholconsumption', y='Dementia and Alzheimers Death Rate per 100000'
    fig = px.scatter(scatter, x='Alcoholconsumption', y='Dementia and Alzheimers Death Rate per 100000', color='Continent',
                     size='Country Population of 2016', hover_data=["Country"])

    return fig
