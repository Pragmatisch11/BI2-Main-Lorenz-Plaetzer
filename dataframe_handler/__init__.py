import pandas
import country_converter as coco


def modify_country_codes(df):
    # Central Africa not found in regex -> es ist Central African Republic gemeint:
    df.loc[(df.Country == 'Central Africa'), 'Country'] = 'Central African Republic'
    df["Country"] = [coco.convert(names=x, to='ISO3') for x in df["Country"]]
    # print(df)
    return df


def add_continent_by_iso3_code(df):
    df = df.assign(Continent=None)
    df["Continent"] = [coco.convert(names=x, src='ISO3', to='continent') for x in df["Country"]]
    return df


def add_full_country_name_by_iso3_code(df):
    df = df.assign(CountryName=None)
    df["CountryName"] = [coco.convert(names=x, src='ISO3', to='name_short') for x in df["Country"]]
    return df
