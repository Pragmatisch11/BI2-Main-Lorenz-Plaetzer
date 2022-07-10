import requests
import pandas
import json
import country_converter as coco


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


def get_dataframe_by_indicatorcode(IndicatorCode):
    r = requests.get("https://ghoapi.azureedge.net/api/" + IndicatorCode)
    r = r.json()["value"]
    r = json.dumps(r)
    df = pandas.read_json(r)
    # df.set_index('SpatialDim', inplace=True)
    # df = pd.DataFrame(r, index="SpatialDim")
    return df


def get_dataframe_by_worldlifeexpectancy_com(url):
    # < !DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN" >
    # < html > < head >
    # < title > 403 Forbidden < / title >
    # < / head > < body >
    # < h1 > Forbidden < / h1 >
    # < p > You don't have permission to access this resource.</p>
    # < p > Additionally, a 403 Forbidden error was encountered
    # while trying to use an ErrorDocument to handle the request.< / p >
    # < / body > < / html >

    headers = {'UserAgent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/103.0.5060.53 Safari/537.36',
               'referer': 'https://www.worldlifeexpectancy.com/cause-of-death/alzheimers-dementia/by-country/'}

    r = requests.get(url, headers=headers, stream=True)
    # r = urllib.request.urlopen(url)
    print(r.content.decode())
    # r = r.json()["chart"]["countries"]["countryitem"]

    # r = json.dumps(r)
    # df = pandas.read_json(r)
    # return df


def get_dataframe_by_csv(path):
    return pandas.read_csv(path)
