"""
Show tile script
"""

import matplotlib.pyplot as plt
import numpy as np
import csv, time, sys
from os import path
from main_rev3 import max_tile, default_tile_size

min_x = 0
min_y = 0

col_colors = []
foot_colors = []

def press(event):
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)

def main():

    try:
        tile_csv = sys.argv[1]
    except:
        tile_csv = 'simulation_tile.csv'

    try:
        track_csv = sys.argv[2]
    except:
        track_csv = 'track.csv'


    if not path.exists(tile_csv):
        # Checking csv file exists or not
        print(tile_csv + " dose not exist")
        sys.exit(0)

    time = None
    ex = 0
    ey = 0
    total_weight = 0

    # Creating track csv file
    with open(track_csv, 'w') as trackcsvfile:
        csvwriter = csv.writer(trackcsvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["timestamp", "foot-x", "foot-y"])

    with open(tile_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count, row in enumerate(reader):
            if row_count == 0:
                # Skiping header row
                continue
            if row_count == 1:
                time = row[0]
            tile_x = int(float(row[1]))
            tile_x_center = (tile_x * default_tile_size)-(default_tile_size/2)
            tile_y = int(float(row[2]))
            tile_y_center = (tile_y * default_tile_size)-(default_tile_size/2)
            weight = float(row[3])

            if time and time == row[0]:
                ex += tile_x_center*(weight/100)
                ey += tile_y_center*(weight/100)
                total_weight += weight/100
                foot_time = time
            else:
                # Calculating foot center
                foot_x_center = ex/total_weight
                foot_y_center = ey/total_weight

                # Writing on track csv file
                with open(track_csv, 'a') as trackcsvfile:
                    csvwriter = csv.writer(trackcsvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow([foot_time, foot_x_center, foot_y_center])

                ex = tile_x_center*(weight/100)
                ey = tile_y_center*(weight/100)
                total_weight = weight/100
                                 
            time = row[0]

if __name__ == '__main__':
    main()
