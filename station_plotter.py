import pandas as pd

# data = pd.read_csv("stadler_station_data.csv", header=None)
data = pd.read_csv("gwr_station_data.csv", header=None)
print("Read {} waypoints".format(int(data.size/2)))

import folium
folium_map = folium.Map(location=[51.648611,  -0.052778],
                        zoom_start=10)
                        # tiles="CartoDB dark_matter")

print("Plotting points...")
for index, coord in data.iterrows():
    # print (index, coord[0], coord[1])
    marker = folium.CircleMarker(location=coord)
    marker.add_to(folium_map)

map_page = "my_map.html"
print("Output to page {}".format(map_page))
folium_map.save(map_page)
