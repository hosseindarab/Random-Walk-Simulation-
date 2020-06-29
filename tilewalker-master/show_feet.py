"""
Show feet script
"""

import matplotlib.pyplot as plt
#import numpy as np
import math
import csv, time, sys
from os import path
from main_rev3 import Foot, min_path, max_path

def press(event):

    # for stopping simulation with key.
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)

def main():

    try:
        feet_csv = sys.argv[1]
    except:
        feet_csv = 'simulation_feet.csv'


    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)

    if not path.exists(feet_csv):
        # Checking csv file exists or not
        print(feet_csv + " dose not exist")
        sys.exit(0)

    right_feet = []
    left_feet = []
    plt.xlim(min_path, max_path)
    plt.ylim(min_path, max_path)
    with open(feet_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count, row in enumerate(reader):
            if row_count == 0:
                # Skiping header row
                continue
            foot_x = float(row[1])
            foot_y = float(row[2])
            foot_type = row[3]

            if foot_type == "right":
                right_feet.append((foot_x, foot_y))
            else:
                left_feet.append((foot_x, foot_y))

            if len(right_feet) >= 2 and row_count%2 != 0:
                # retriving angle of right foot by two points of foot position in path
                dx = right_feet[-1][0]-right_feet[-2][0]
                dy = right_feet[-1][1]-right_feet[-2][1]
                right_angle = math.degrees(math.atan2(dy, dx))
                if right_angle < 0:
                    right_angle = right_angle + 360

            elif len(left_feet) >= 2 and row_count%2 == 0:
                # Retriving angle of left foot by two points of foot position in path
                dx = left_feet[-1][0]-left_feet[-2][0]
                dy = left_feet[-1][1]-left_feet[-2][1]
                left_angle = math.degrees(math.atan2(dy, dx))
                if left_angle < 0:
                    left_angle = left_angle + 360

            if row_count == 5:

                # Plotting both right and left foot in start poing
                right_foot = Foot(x=right_feet[0][0], y=right_feet[0][1], alpha=right_angle)
                left_foot = Foot(x=left_feet[0][0], y=left_feet[0][1], alpha=left_angle)
                right_foot.plot(fig, ax, cover=None, show_animation=True)
                left_foot.plot(fig, ax, cover=None)
                plt.pause(0.2)

                #  Plotting right foot in first step
                right_foot.x=right_feet[1][0]
                right_foot.y=right_feet[1][1]
                right_foot.alpha=right_angle
                right_foot.plot(fig, ax, cover=None, show_animation=True)
                plt.pause(0.2)

                #  Plotting left foot in first step
                left_foot.x=left_feet[1][0]
                left_foot.y=left_feet[1][1]
                left_foot.alpha=left_angle
                left_foot.plot(fig, ax, cover=None, show_animation=True)
                plt.pause(0.2)

            if row_count > 5:

                if foot_type == "right":
                    #  Plotting right foot
                    right_foot.x=right_feet[-1][0]
                    right_foot.y=right_feet[-1][1]
                    right_foot.alpha=right_angle
                    right_foot.plot(fig, ax, cover=None, show_animation=True)
                    plt.pause(0.2)

                else:
                    # Plotting left foot
                    left_foot.x=left_feet[-1][0]
                    left_foot.y=left_feet[-1][1]
                    left_foot.alpha=left_angle
                    left_foot.plot(fig, ax, cover=None, show_animation=True)
                    plt.pause(0.2)

    plt.show()

if __name__ == '__main__':
    main()
