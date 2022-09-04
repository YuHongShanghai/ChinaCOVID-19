# ChinaCOVID-19
Data analysis of daily new cases of COVID-19 in China based on Python
## environment
* Python 3.9
* beautifulsoup4 4.11.1
* pandas 1.4.4
* pyecharts 1.9.1
## description
Use the network spider to obtain daily new report text of COVID-19 from the official website of the China Health and Health Commission. Then process the text to get the data. Finally, draw line diagrams and maps with a timeline based on data.
## usage
Just run main.py. The result is saved in floder data and plot:
  * The row text data is in data/data.csv, and the data parsed is in data/result.csv.
  * plot/line.html is the line diagram, and the maps is plot/maps.html.
