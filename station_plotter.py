def waypoint_finder(file):
    for line in file:
        if 'INSERT INTO waypoint' in line:
            yield line


# Extract waypoint table INSERTs
source_data = open('stadler_station_data.sql','r')
csv_data = open('tmp_data.csv', 'w');
for wp in waypoint_finder(source_data):
    csv_data.write(wp)
csv_data.close()


# Read the CSV data
import pandas as pd
data = pd.read_csv('tmp_data.csv', header=None)
print("Reading waypoints")

import folium
folium_map = folium.Map(location=[51.648611,  -0.052778],
                        zoom_start=15)
                        # tiles="CartoDB dark_matter")

print("Plotting points...")
for v in data.values:
    import re
    match = re.split("\'", v[6])
    waypoint_name = match[1]

    coord = v[9],v[10]
    marker = folium.CircleMarker(location=coord)
    marker.add_to(folium_map)

    # Add geofence
    folium.Circle(
        radius=500,
        location=coord,
        popup=waypoint_name,
        color='crimson',
        fill=False,
    ).add_to(folium_map)

map_page = "my_map.html"
print("Output to page {}".format(map_page))
folium_map.save(map_page)
