import folium
import pandas
from folium import Popup, Tooltip

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])


def color_producer(elevation):
    if elevation < 1000:
        return "lightgreen"
    elif 1000 <= elevation <= 2000:
        return "orange"
    else:
        return "red"


m = folium.Map(location=[lat[10], lon[10]], zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, n in zip(lat, lon, elev, name):
    fgv.add_child(folium.CircleMarker(location=(lt, ln),
                                      radius=8,
                                      fill_color=color_producer(el),
                                      popup=Popup(str(n) + ": " + str(el) + " meters", parse_html=True, max_width=200,
                                                  min_width=120),
                                      tooltip=Tooltip(str(n), sticky=False),
                                      color="gray",
                                      fill_opacity=0.8))

fgp = folium.FeatureGroup(name="Population")


def population_colors(population):
    if population < 10000000:
        return {
            'fillColor': 'green',
            'fillOpacity': 0.7,
        }
    elif 10000000 <= population < 50000000:
        return {
            'fillColor': 'orange',
            'fillOpacity': 0.8,
        }
    else:
        return {
            'fillColor': 'red',
            'fillOpacity': 0.9,
        }


fgp.add_child(folium.GeoJson(data=(open("world.json", "r", encoding="utf-8-sig").read()),
                             style_function=lambda x: population_colors(x['properties']['POP2005'])))

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
)
state_geo = f"{url}/us-states.json"
state_unemployment = f"{url}/US_Unemployment_Oct2012.csv"
state_data = pandas.read_csv(state_unemployment)

fgw = folium.Choropleth(
    geo_data=state_geo,
    name="Unemployment Rate",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
)

m.add_child(fgp)
m.add_child(fgw)
m.add_child(fgv)
m.add_child(folium.LayerControl())
m.save("index.html")
