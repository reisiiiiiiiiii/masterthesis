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
        return parse(timeString).strftime(dateTimeMode)
    except ValueError:
        print(f"Warnung: Ungültiges Datum '{timeString}' kann nicht geparst werden.")
        return None

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
        currentDate = row[5]
        parsedDate = getDateFromTimeString(currentDate)
        if not parsedDate:  # Wenn das Datum ungültig ist, überspringe diesen Durchlauf
            continue
        dateString = parsedDate

        # Hier setzen wir die Stunde nicht, da der Datensatz täglich ist
        # Wetterbedingungen
        if dateString not in isBadDay:
            isBadDay[dateString] = 0
        weatherCondition = row[-2]  # Änderung gemäß Anweisung
        if weatherCondition != '':
            isBadDay[dateString] = 1
        # Temperatur
        if dateString not in temperature:
            temperature[dateString] = []
            # Stündliche Werte sind gleich den Tageswerten, daher speichern wir nur einen Wert
            temperatureHour[dateString] = [NO_TEM] * 24  
        if row[2] != '':  # Geändert von row[15] zu row[2]
            temp_val = float(row[2].replace('s', ''))
            temperature[dateString].append(temp_val)
            # Setzen aller stündlichen Werte auf den Tageswert
            temperatureHour[dateString] = [temp_val] * 24
        # Windgeschwindigkeit
        if dateString not in wind:
            wind[dateString] = []
            windHour[dateString] = [0] * 24  # Stündliche Werte gleich den Tageswerten
        if row[17] != '':  # Keine Änderung notwendig, da die Windspalte gleich bleibt
            wind_val = float(row[17].replace('s', ''))
            wind[dateString].append(wind_val)
            windHour[dateString] = [wind_val] * 24  # Setzen aller stündlichen Werte auf den Tageswert

for key, value in temperature.items():
    temperature[key] = NO_TEM if not value else np.mean(value)
for key, value in wind.items():
    wind[key] = NO_TEM if not value else np.mean(value)

weatherDict = {'isBadDay': isBadDay, 'temperature': temperature, 'wind': wind, 'temHour': temperatureHour,
               'windHour': windHour}

with open(os.path.join(jsonPath, 'weatherDict.json'), 'w') as f:
    json.dump(weatherDict, f)
