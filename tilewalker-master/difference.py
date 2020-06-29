"""
Show error graph between real foot position and detected foot position.
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import csv, sys

def press(event):
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)

time = []    
detected_x_list = []
detected_y_list = []

real_x_list = []
real_y_list = []

def main():
    
    try:
        real_csv = sys.argv[1]
    except:
        real_csv = 'simulation_feet.csv'
    
    try:
        detected_csv = sys.argv[2]
    except:
        detected_csv = 'track.csv'

    
    if not path.exists(real_csv):
        # Checking csv file exists or not
        print(real_csv + " dose not exist")
        sys.exit(0)

    if not path.exists(detected_csv):
        # Checking csv file exists or not
        print(detected_csv + " dose not exist")
        sys.exit(0)
        
    with open(detected_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count, row in enumerate(reader): 
            time.append(row_count)
            if row_count == 0:
                # Skiping header row
                continue 
            if row_count == 1:
                # Keeping detected x positions of feet in a list
                detected_x_list.append(row[1])
                # Keeping detected y positions of feet in a list
                detected_y_list.append(row[2])

        
    with open(real_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count, row in enumerate(reader):     
            if row_count == 0:
                # Skiping header row
                continue 
            if row_count == 1:
                # Keeping real x position of feet in a list
                real_x_list.append(row[1])
                # Keeping real x position of feet in a list
                real_y_list.append(row[2])
                
    # Retriving error between detected x position of feet and real x position of feet
    x_error_list = [float(x) - float(real_x_list[index]) for index, x in enumerate(detected_x_list) ]
    
    # Retriving error between detected y position of feet and real y position of feet
    y_error_list = [float(y) - float(real_y_list[index]) for index, y in enumerate(detected_y_list) ]

    
    fig, ax = plt.subplots()
    dt = 1
    
    
    x_cnse = np.convolve(x_error_list, time, mode='same') * dt   # colored x position of feet error
    y_cnse = np.convolve(y_error_list, time, mode='same') * dt  # colored y position of feet error
    
    x_error = x_cnse
    y_error = y_cnse
    
    ax.plot(time, x_error, time, y_error)
    ax.set_xlim(0, 10)
    ax.set_xlabel('Time')
    ax.set_ylabel('Error of x and y feet')

    ax.set_title('Blue: x position of feet Error \n   Orange: y position of feet Error')
    ax.grid(True)
    
    plt.show()
if __name__ == '__main__':
    main()
