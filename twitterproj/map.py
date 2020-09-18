import json
import sys
sys.path.append('..')
import folium
print (folium.__file__)
print (folium.__version__)
from branca.colormap import linear
import statistics as stats
from pymongo import MongoClient

statesDict = {
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO',
    'Wyoming': 'WY'
}

def get_boundary(info):
        value_list = list(info.values())
        mean = stats.mean(value_list)
        # print(str(mean))
        std = stats.stdev(value_list)
        # print(str(std))
        low = mean-3*std
        high = mean + 3*std
        return low, high

def normalize(value, low, high):
    return float((value-low)/(high-low))


def Mapping():
    client = MongoClient()
    cs562 = client['cs562']

    dbresults = cs562['stateResult'].find()

    result = []
    for info in dbresults:
        state = info['state']
        for s,abbr in statesDict.items():
            if state == abbr:
                state = s
        total = info['totalTweets']
        result.append((state, total))
    result.append(('AK',1))

    low, high = get_boundary(dict(result))
    normresult = []
    for k,v in result:
        normV = normalize(v,low, high) * 100
        normresult.append((k,normV))


    sortresult = sorted(normresult, key=lambda x: x[1], reverse=True)
    dictR = dict(sortresult)
    print(dictR)


    # import geo json data
    geo_json_data = json.load(open('usstate.geojson'))


    colormap = linear.PuRd.scale(
        sortresult[-1][1],
        sortresult[0][1]
    )


    m = folium.Map([42.324725, -71.093327], tiles='CartoDB Positron', zoom_start=7)


    def styleFunc(feature):
        x = dictR.get(feature['properties']['NAME'],None)
        return {
            'fillColor': '#ffffff' if x is None else colormap(x),
            'color': 'black',
            'weight': 0.1,
            'dashArray': '5, 5',
            'fillOpacity': .9,
        }



    # apply the Boston zipcode areas outlines to the map
    folium.GeoJson(geo_json_data,
                  style_function= styleFunc
                  ).add_to(m)

    # display map
    m.save("stateHeatMap.html")


def MapSupport():
    client = MongoClient()
    cs562 = client['cs562']

    dbresults = cs562['stateResult'].find()

    result = []
    for info in dbresults:
        state = info['state']
        for s, abbr in statesDict.items():
            if state == abbr:
                state = s
        total = info['support']
        result.append((state, total))

    dictR = dict(result)
    print(dictR)

    # import geo json data
    geo_json_data = json.load(open('usstate.geojson'))


    m = folium.Map([42.324725, -71.093327], tiles='CartoDB Positron', zoom_start=7)

    def styleFunc(feature):
        x = dictR.get(feature['properties']['NAME'], None)
        return {
            'fillColor': '#9d1309' if x == "west" else '#27408b',
            'color': 'black',
            'weight': 0.7,
            'dashArray': '',
            'fillOpacity': .9,
        }

    folium.GeoJson(geo_json_data,
                   style_function=styleFunc
                   ).add_to(m)

    # display map
    m.save("stateSupportMap.html")



if __name__ == "__main__":
    Mapping()
    MapSupport()
