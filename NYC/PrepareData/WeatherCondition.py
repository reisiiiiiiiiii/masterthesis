from localPath import *
import os
import csv
import json
import numpy as np
from dateutil.parser import parse
from Utils.symbols import *
dateTimeMode = '%Y-%m-%d'

def getDateFromTimeString(timeString):
    return parse(timeString).strftime(dateTimeMode)

isBadDay = {}
temperature = {}
temperatureHour = {}
wind = {}
windHour = {}
with open(os.path.join(csvDataPath, 'weather_2015.csv'), 'r') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    counter = 0
    for row in f_csv:
        print(counter)
        counter += 1
        # date 05
        currentDate = row[5]
        date = parse(currentDate)
        dateString = date.strftime(dateTimeMode)
        hour = date.hour
        # Weather condition
        if dateString not in isBadDay:
            isBadDay[dateString] = 0
        weatherCondition = row[-2]  # Changed from row[9] to row[-2]
        if weatherCondition != '':
            isBadDay[dateString] = 1
        # Temperature
        if dateString not in temperature:
            temperature[dateString] = []
            temperatureHour[dateString] = [NO_TEM for e in range(24)]
        if row[2] != '':  # Changed from row[15] to row[2]
            try:
                temp_val = float(row[2].replace('s', ''))
                temperature[dateString].append(temp_val)
                temperatureHour[dateString] = [temp_val for e in range(24)]  # Set hourly values to daily value
            except:
                print('Tem', row[2])
        # Wind speed
        if dateString not in wind:
            wind[dateString] = []
            windHour[dateString] = [0 for e in range(24)]
        if row[17] != '':  # Wind is the same column
            try:
                wind_val = float(row[17].replace('s', ''))
                wind[dateString].append(wind_val)
                windHour[dateString] = [wind_val for e in range(24)]  # Set hourly values to daily value
            except:
                print('Wind', row[17])

for key, value in temperature.items():
    temperature[key] = NO_TEM if len(value) == 0 else np.mean(value)
for key, value in wind.items():
    wind[key] = NO_TEM if len(value) == 0 else np.mean(value)

weatherDict = {'isBadDay': isBadDay, 'temperature': temperature, 'wind': wind, 'temHour': temperatureHour,
               'windHour': windHour}

with open(os.path.join(jsonPath, 'weatherDict.json'), 'w') as f:
    json.dump(weatherDict, f)
