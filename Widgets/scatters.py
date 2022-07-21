# import matplotlib.pyplot as plt
import pandas
import plotly.express as px
# from sklearn import preprocessing as pre
# import dataframe_handler as dfh
import numpy as np


# from numpy import ma

# Auswertung über den Zusammenhang von Alkoholkonsum, Demenz und Alzheimer Todesrate und Lebenserwartung
# x-Achse: Alkoholkonsum
# y-Achse: Demenz und Alzehimer Todes Rate
# Bubble Größe: Lebenserwartung
# Bubble Farbe: Kontinentzordnung
# einzelner Bubble: Land
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


# Auswertung über den Zusammenhang von Alkoholkonsum, Demenz und Alzheimer Todesrate und BMI
# x-Achse: Alkoholkonsum
# y-Achse: Demenz und Alzehimer Todes Rate
# Bubble Größe: BMI
# Bubble Farbe: Kontinentzordnung
# einzelner Bubble: Land
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


# Auswertung über den Zusammenhang von Alkoholkonsum, Demenz und Alzheimer Todesrate und der Einwohnerzahl
# x-Achse: Alkoholkonsum
# y-Achse: Demenz und Alzheimer Todes Rate
# Bubble Größe: Population logarithmisch
# Bubble Farbe: Kontinentzuordnung
# einzelner Bubble: Land
def get_scatter_alcohol_population_scatter(df_alcohol_consumption, df_alz_dem_deathrate_b, df_pop):
    # sub_df_alcohol_consumption = df_alcohol_consumption.rename(columns={"SpatialDim": "Country"})

    # Country Population noch umbennen mit dem Divisionsfaktor (zB divided by 10000)
    df_pop = df_pop[["Country Name", "Country Code", "2016"]].rename(columns={"Country Code": "Country",
                                                                              "2016": "Country Population of 2016"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_alz_dem_deathrate_b, on="Country")

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption",
                                      "Rate": "Dementia and Alzheimers Death Rate per 100000"})

    scatter = pandas.merge(scatter, df_pop, on=["Country"])
    scatter['Country Population of 2016'] = scatter["Country Population of 2016"].fillna(0)

    ##Tests mit MinMaxScaler und einfacher Division
    # scatter['Country Population of 2016'] = scatter['Country Population of 2016'] / 10000
    # scaler = pre.MinMaxScaler()
    # scatter['Country Population of 2016'] = scaler.fit_transform(scatter[['Country Population of 2016']].to_numpy())
    # scatter['Country Population of 2016'] = round(scatter['Country Population of 2016'],3)

    scatter['Country Population of 2016'] = np.log2(scatter['Country Population of 2016'],
                                                    out=np.zeros_like(scatter['Country Population of 2016']),
                                                    where=(scatter['Country Population of 2016'] != 0))

    fig = px.scatter(scatter, x='Alcoholconsumption', y='Dementia and Alzheimers Death Rate per 100000',
                     color='Continent',
                     size='Country Population of 2016', hover_data=["Country Name"])

    return fig


# Auswertung über den Zusammenhang von Alkoholkonsum, BMI und Einwohnerzahl
# x-Achse: Alkoholkonsum
# y-Achse: BMI
# Bubble Größe: Population logarithmisch
# Bubble Farbe: Kontinentzordnung
# einzelner Bubble: Land
"""
def get_scatter_alcohol_bmi_population_scatter(df_alcohol_consumption, df_bmi, df_pop):
    df_pop = df_pop[["Country Name", "Country Code", "2016"]].rename(columns={"Country Code": "Country",
                                                                              "2016": "Country Population of 2016"})

    df_bmi = df_bmi[["SpatialDim", "TimeDim", "Dim1", "NumericValue"]].rename(columns={"SpatialDim": "Country",
                                                                                       "NumericValue": "BMI"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_pop, on="Country")
    scatter['Country Population of 2016'] = scatter["Country Population of 2016"].fillna(0)
    scatter['Country Population of 2016'] = np.log2(scatter['Country Population of 2016'],
                                                    out=np.zeros_like(scatter['Country Population of 2016']),
                                                    where=(scatter['Country Population of 2016'] != 0))

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption"})

    df_bmi = df_bmi.query('Dim1 == "%s"' % "BTSX")
    df_bmi = df_bmi.groupby(["Country"]).mean()

    scatter = pandas.merge(scatter, df_bmi, on=["Country"])
    scatter = scatter.dropna()

    fig = px.scatter(scatter, x='Alcoholconsumption', y='BMI', color='Continent',
                     size='Country Population of 2016', hover_data=["Country Name"])

    return fig
"""

# Test Slider Nils
def get_scatter_alcohol_bmi_population_scatter(df_alcohol_consumption, df_bmi, df_pop, year):
    df_pop = df_pop[["Country Name", "Country Code", year]].rename(columns={"Country Code": "Country",
                                                                            f"{year}": f"Country Population of {year}"})

    df_bmi = df_bmi[["SpatialDim", "TimeDim", "Dim1", "NumericValue"]].rename(columns={"SpatialDim": "Country",
                                                                                       "NumericValue": "BMI"})

    scatter = pandas.merge(df_alcohol_consumption.query('Dim1 == "BTSX"')[["Country", "NumericValue", "Continent"]],
                           df_pop, on="Country")
    scatter[f'Country Population of {year}'] = scatter[f'Country Population of {year}'].fillna(0)
    scatter[f'Country Population of {year}'] = np.log2(scatter[f'Country Population of {year}'],
                                                    out=np.zeros_like(scatter[f'Country Population of {year}']),
                                                    where=(scatter[f'Country Population of {year}'] != 0))

    scatter = scatter.rename(columns={"NumericValue": "Alcoholconsumption"})

    df_bmi = df_bmi.query('Dim1 == "%s"' % "BTSX")
    df_bmi = df_bmi.groupby(["Country"]).mean()

    scatter = pandas.merge(scatter, df_bmi, on=["Country"])
    scatter = scatter.dropna()

    fig = px.scatter(scatter, x='Alcoholconsumption', y='BMI', color='Continent',
                     size=f'Country Population of {year}', hover_data=["Country Name"])

    return fig
