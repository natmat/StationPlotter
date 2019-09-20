import pandas as pd

data = pd.read_csv("stadler_station_data.csv", header=None)

import folium

folium_map = folium.Map(location=[51.648611,  -0.052778],
                        zoom_start=10)
                        # tiles="CartoDB dark_matter")
for index, coord in data.iterrows():
    print (index, coord[0], coord[1])
    x, y = coord
    marker = folium.CircleMarker(location=coord)
    marker.add_to(folium_map)

folium_map.save("my_map.html")
