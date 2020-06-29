"""
Aggregate two csv file 
"""

import matplotlib.pyplot as plt
import numpy as np
import csv, time, sys
from os import path

        
def main():
    
    try:
        tile_csv1 = sys.argv[1]
    except:
        tile_csv1 = 'simulation_tile1.csv'
    
    try:
        tile_csv2 = sys.argv[2]
    except:
        tile_csv2 = 'simulation_tile2.csv'  

    try:
        tile_csv3 = sys.argv[3]
    except:
        tile_csv3 = 'output.csv' 
        
    time1 = None
    time2 = None
    count = 0
    change_foot_dict = {}
    values = []
    keys = []
    aggregate_indeces = []

    if not path.exists(tile_csv1):
        # Checking csv file exists or not
        print(tile_csv1 + " dose not exist")
        sys.exit(0)
        
    if not path.exists(tile_csv2):
        # Checking csv file exists or not
        print(tile_csv2 + " dose not exist")
        sys.exit(0)    

    #Categorize rows in second csv file by time.  
    with open(tile_csv2, 'r') as csvfile2:
        reader2 = csv.reader(csvfile2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count2, row2 in enumerate(reader2):     
            if row_count2 == 0:
                # Skiping header row
                continue
                 
            if row_count2 == 1:
                time2 = row2[0]
                key = 1
                keys.append(key)
            
            if row2[0] != time2:
                change_foot_dict[key] = values
                values = []
                key += 1
                keys.append(key)
                values.append(row2)
                time2 = row2[0]
                continue
            
            values.append(row2)
                
        # Set value for last key     
        change_foot_dict[key] = values 
        
    last_key = key               

    # Categorize rows in first csv file by time 
    # and aggregate wieghts from two diffrent files into a single file.
    with open(tile_csv1, 'r') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row_count1, row1 in enumerate(reader1): 
            if row_count1 == 0:
                # Creating output CSV file "outputsimulation_tile.csv"
                with open(tile_csv3, 'w') as csvfile3:
                    csvwriter = csv.writer(csvfile3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow(["timestamp", "tile-x", "tile-y", "weight%"])
                # Skiping header row
                continue

            if row_count1 == 1:
                time1 = row1[0]
                key = 1
               
            if row1[0] != time1:
                if key in change_foot_dict:
                    for count, f in enumerate(change_foot_dict[key]):
                        if not (count in aggregate_indeces):
                            with open(tile_csv3, 'a') as csvfile3:
                                csvwriter = csv.writer(csvfile3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                csvwriter.writerow([key, f[1], f[2], f[3]])
                        
                key += 1
                aggregate_indeces = []
                time1 = row1[0]
                
            weight = row1[3]
            if key in change_foot_dict:               
                for count, f in enumerate(change_foot_dict[key]):
                    if row1[1] == f[1] and row1[2] == f[2]:
                        aggregate_indeces.append(count)
                        weight = row1[3]+f[3]
            
            with open(tile_csv3, 'a') as csvfile3:
                csvwriter = csv.writer(csvfile3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow([key, row1[1], row1[2], weight])
        
        if key in change_foot_dict and key < last_key:
            for count, f in enumerate(change_foot_dict[key]):
                if not (count in aggregate_indeces):
                    with open(tile_csv3, 'a') as csvfile3:
                        csvwriter = csv.writer(csvfile3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        csvwriter.writerow([key, f[1], f[2], f[3]])
    
        while key < last_key:
            key+=1                 
            for f in change_foot_dict[key]:
                with open(tile_csv3, 'a') as csvfile3:
                    csvwriter = csv.writer(csvfile3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow([key, f[1], f[2], f[3]])
            

if __name__ == '__main__':
    main()
