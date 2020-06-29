This projects includes seven scripts:

1.simulation.py
2.show_tile.py
3.show_feet.py
4.track.py
5.diffrence.py
6.aggregate.py
7.diffrence_all.py

1.simulation.py:
"simulation.py" should be run before runing the scripts "show_tile.py",
"show_foot.py" and "track.py".

"simulation.py" generates walking data on a random path. 
It gets two names as the parameters and generates two csv files 
with the same names.
For example:
>>python simulation.py "tilesim.csv" "feetsim.csv"

2.show_tile.py:
"show_tile.py" gets generated files by "simulation.py" that keeps 
information about tiles and its overlap-area between foot and tiles as argument.
It displays the tiles animation.
For example:
>>python show_tile.py "tilesim.csv"

3.show_feet.py:
"show_feet.py" gets generated file by "simulation.py" that keeps 
information about steps as argument.
It displays the steps animation.
>>python show_feet.py "feetsim.csv"

4.track.py:
"track.py" gets two arguments:
1.Generated file by "simulation.py" that  keeps 
information about tiles and its overlap-area between foot and tiles.
2.The output file name that keeps estimated feet coordinates.
It estimates feet coordinates(x,y).
For example:
>>python track.py "tilesim.csv" "track.csv"

5.diffrence.py:
It displays error graph between real foot position and detected foot position.
It gets two files as arguments:
1)The output file that keeps real feet position. It is generated simulation.py.
2)The output file that keeps detected feet position.It is generated by track.py.
>>python diffrence.py "feetsim.csv" "track.csv"

6.aggregate.py:
It gets two different files which generated by "simulation.py" that keeps 
information about tiles and aggregates the weights from two diffrent files into a single file.
Also It can get output file as third argument.
For example:
>>python aggregate.py "tilesim1.csv" "tilesim2.csv" “output.csv”

7.diffrence_all.py:
It displays error graph between real foot position and detected foot position for
all existed files in a specific directory.
It gets directory path as arguments:
The script read only files with “_real.csv” and “_detected.csv” suffixes.
For example:
>>python diffrence_all.py "/Users/FolderName”
