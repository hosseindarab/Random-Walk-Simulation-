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
    # for stopping simulation with key.
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)

def main():

    try:
        tile_csv = sys.argv[1]
    except:
        tile_csv = 'simulation_tile.csv'

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    for col in np.arange(min_y, max_tile*default_tile_size, default_tile_size):
        row_colors = []
        row1_colors = []
        for row in np.arange(min_x, max_tile*default_tile_size, default_tile_size):
            row_colors.append(0)
            row1_colors.append(0)
        col_colors.append(row_colors)
        foot_colors.append(row1_colors)
    to_draw = None
    time = None
    count = 0
    foot_index = {"foot_"+str(count):[]}

    if not path.exists(tile_csv):
        # Checking csv file exists or not
        print(tile_csv + " dose not exist")
        sys.exit(0)

    with open(tile_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count, row in enumerate(reader):
            if row_count == 0:
                # Skiping header row
                continue
            if row_count == 1:
                time = row[0]

            tile_x = int(round(float(row[1])))
            tile_y = int(round(float(row[2])))
            weight = float(row[3])
            col_colors[tile_y-1][tile_x-1] = col_colors[tile_y-1][tile_x-1]+ weight

            if time and time == row[0]:
                if "foot_"+str(count-1) in foot_index.keys():
                    if (tile_y-1,tile_x-1) in foot_index["foot_"+str(count-1)]:
                        foot_colors[tile_y-1][tile_x-1] = foot_colors[tile_y-1][tile_x-1]+weight
                    else:
                        foot_colors[tile_y-1][tile_x-1] = weight
                else:
                    foot_colors[tile_y-1][tile_x-1] = foot_colors[tile_y-1][tile_x-1]+weight

                foot_index["foot_"+str(count)].append((tile_y-1, tile_x-1))

            else:
                if count >= 2:
                    if "foot_"+str(count-2) in foot_index.keys():
                        for i0,i1 in foot_index["foot_"+str(count-2)]:
                            if not (i0, i1) in foot_index["foot_"+str(count-1)] and not (i0, i1) in foot_index["foot_"+str(count)]:
                                foot_colors[i0][i1] = 0
                        foot_index.pop("foot_"+str(count-2), None)
                if count != 0:
                    ax.pcolormesh(foot_colors, cmap='Reds')
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    plt.pause(0.2)

                count += 1
                foot_colors[tile_y-1][tile_x-1] = foot_colors[tile_y-1][tile_x-1]+weight
                if not "foot_"+str(count) in foot_index.keys():
                    foot_index["foot_"+str(count)] = [(tile_y-1, tile_x-1)]

            time = row[0]


    ax.pcolormesh(col_colors, cmap='Reds')
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()

if __name__ == '__main__':
    main()
