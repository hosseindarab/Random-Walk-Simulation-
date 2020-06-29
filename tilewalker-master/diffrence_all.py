"""
Show error graph between real foot position and detected foot position in several files.
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import csv, sys, os

def press(event):
    """Stop displaying graph with key 'q' or 'Q'"""
    if event.key == 'q' or event.key == 'Q':
        print('Quitting upon request.')
        sys.exit(0)
        
def main():
    
    try:
        directory_path = sys.argv[1]
        # CSV files are in the 'directory_path'
    except:
        print("Please specify directory path.")
        
    if not path.exists(directory_path):
        # Checking directory path exists or not
        print("'" + directory_path + "' dose not exist")
        sys.exit(0)

    #Retriving all files with '_real.csv' suffix
    files = os.listdir(directory_path)   
    files = list(filter(lambda f: f.endswith("_real.csv"), files))
    
    if not files or files == []:
        print("There is no proper csv file in this directory.")
        sys.exit(0)

    fig, ax = plt.subplots()    
    for file in files:
        real_csv = file
        detected_csv = file.replace("_real.csv","_detected.csv")
        
        # Full detected file path.
        detected_file_path = os.path.join(directory_path, detected_csv)
        # Checking if detected file exists in directory or not. 
        if not path.exists(detected_file_path):
            print("'" + detected_csv + "' dose not exist in '" + directory_path + "' directory.")
            continue
        
        detected_x_list = []
        detected_y_list = []
        real_x_list = []
        real_y_list = []
        
        with open(detected_csv, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row_count, row in enumerate(reader):
                if row_count == 0:
                    # Skiping header row
                    continue 
                # Keeping detected x positions of feet in a list
                detected_x_list.append(row[1])
                # Keeping detected y positions of feett in a list
                detected_y_list.append(row[2])

            
        with open(real_csv, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row_count, row in enumerate(reader):     
                if row_count == 0:
                    # Skiping header row
                    continue 
                # Keeping real x position of feet in a list
                real_x_list.append(row[1])
                # Keeping real x position of feet in a list
                real_y_list.append(row[2])
                
        # Retriving error between detected x position of feet and real x position of feet
        x_error_list = [float(x) - float(real_x_list[index]) for index, x in enumerate(detected_x_list) ]
        
        # Retriving error between detected y position of feet and real y position of feet
        y_error_list = [float(y) - float(real_y_list[index]) for index, y in enumerate(detected_y_list) ]
    
        ax.plot(x_error_list, label= file.replace("_real.csv","_X"))
        ax.plot(y_error_list, label= file.replace("_real.csv","_Y"))

        
    ax.set_xlabel('Time')
    ax.set_ylabel('Error (Meters)')
    
    ax.legend()
    ax.grid(True)

    plt.show()

    
if __name__ == '__main__':
    main()
