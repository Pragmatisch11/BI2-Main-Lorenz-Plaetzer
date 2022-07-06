import requests
import pandas
import json


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
