"""
Script to:
- read a station_data.sql file
- extract the waypoint table insertions from that file
- parset the waypoint information for name, lat, lon, geo
- plot pin on map
- plot shaded area for geofence, with popup label
"""

from sys import exit
import tkinter as tk
from tkinter import filedialog

lats = [180, -180]
longs = [180, -180]

#Method to update the lat/long bounds wrt to the args
def updateBounds(lat, lon):
    lats[0] = min(lat, lats[0])
    lats[1] = max(lat, lats[1])
    longs[0] = min(lon, longs[0])
    longs[1] = max(lon, longs[1])

# Popup to select input station_data.sql file
root = tk.Tk()
root.withdraw()
# station_data_sql = filedialog.askopenfilename()
station_data_sql = "/Users/Nathan/work/petards/customer-configurations/Test configs/QA/Stad_DB/sql/Stad/station_data.sql"
if not station_data_sql:
    print("Error: must select a station_data.sql file")
    exit(1)
print("Reading data from {}".format(station_data_sql))

# Set up the DataFrame for the oolumns to extract from the station_data.sql waypoint table data
import pandas as pd
df = pd.DataFrame(columns=['waypoint_name', 'waypoint_type', 'waypoint_id', 'waypoint_lat', 'waypoint_long', 'waypoint_radius', 'tap_tsi_code'])

# Create a basemap centred somewhere around East Anglia
import folium
# station_data_map = folium.Map(location=[51.648611, -0.052778], zoom_start=10, tiles="CartoDB dark_matter")
station_data_map = folium.Map(location=[51.648611, -0.052778], zoom_start=10,tiles='OpenStreetMap')

# Open station_data.sql file for parsing
import re
data_sql = open(station_data_sql, 'r')
for line in data_sql:
    # Regex for the DataFrame columns
    wp_line_re = re.match("^.*insert\s+into\swaypoint.*values\s*\((.*)\).*$", line, re.IGNORECASE)
    if wp_line_re:
        # Strip ' from the line, then split on ','
        data = wp_line_re.group(1).replace('\'', '')
        # print(data)
        nElem = len(data.split(','))
        if (nElem == 6):
            waypoint_name, waypoint_type, waypoint_id, waypoint_lat, waypoint_long, waypoint_radius = data.split(',')
        elif (nElem == 7):
            waypoint_name, waypoint_type, waypoint_id, waypoint_lat, waypoint_long, waypoint_radius, tap_tsi_code = data.split(',')
        else:
            waypoint_name, waypoint_type, waypoint_id, waypoint_lat, waypoint_long, waypoint_radius, tap_tsi_code, crs_code = data.split(',')

        # Add markers to the map
        lat, lon = float(waypoint_lat), float(waypoint_long)
        updateBounds(lat, lon)
        folium.Marker(location=[lat, lon], tooltip=waypoint_name).add_to(station_data_map)
        geofence = float(waypoint_radius)
        folium.Circle([lat, lon], radius=geofence, fill=True, fill_color='green', fill_opacity=0.25, tooltip=waypoint_name).add_to(station_data_map)

#Reset the map location
from statistics import mean
station_data_map.location = [mean(lats), mean(longs)]
station_data_map.zoom_start = 2

#Output the map
map_file = station_data_sql + ".map.html"
print("Writing to file {}".format(map_file))
station_data_map.save(map_file)

