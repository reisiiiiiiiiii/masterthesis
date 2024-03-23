from localPath import *
import os
import csv
import json
import numpy as np
from dateutil.parser import parse
from Utils.symbols import *
dateTimeMode = '%Y-%m-%d'

def getDateFromTimeString(timeString):
    try:
        return parse(timeString)  # parse() returns a datetime object
    except ValueError as e:
        print(f"Error parsing date: {e}: {timeString}")
        return None

isBadDay = {}
temperature = {}
#temperatureHour = {}
wind = {}
#windHour = {}

with open(os.path.join(csvDataPath), 'r') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    counter = 0
    for row in f_csv:
        print(counter)
        counter += 1
        
        # Parse the date using the getDateFromTimeString function
        currentDate = row[5]
        date_object = getDateFromTimeString(currentDate)  # Use date_object to store the datetime object
        if date_object is None:
            continue  # Skip this row if the date is invalid
        
        dateString = date_object.strftime(dateTimeMode) 
        
        # Weather condition
        isBadDay[dateString] = 0 if row[-2] == '' else 1  # Assuming the weather condition column is the second-to-last
        
        # Temperature
        if row[2] != '':
            try:
                temperature[dateString] = float(row[2].replace('s', ''))  # Assuming the temperature column is index 2
            except ValueError:
                print('Temperature parsing error', row[2])
        
        # Wind speed
        if row[17] != '':
            try:
                wind[dateString] = float(row[17].replace('s', ''))  # Assuming the wind column is index 17
            except ValueError:
                print('Wind speed parsing error', row[17])

weatherDict = {'isBadDay': isBadDay, 'temperature': temperature, 'wind': wind}

# Assuming jsonPath is correctly defined to point to your desired output directory
with open(os.path.join(jsonPath, 'weatherDict.json'), 'w') as f:
    json.dump(weatherDict, f)