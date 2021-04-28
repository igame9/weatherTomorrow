import json
import re
import requests
import datetime

if __name__ == '__main__':
    listWithFindTemp = []
    listTomorrowWeather = []
    listWithDays = []
    listWIthData = []
    countryRequest = requests.get("https://www.meteoservice.ru/location/cities?country_id=1")
    jsonDecode = json.loads(countryRequest.text.encode('utf-8'))
    place = str(input())
    currentCity = jsonDecode.get(place)
    currentPoint = currentCity['point']

    xmlFile = requests.get('https://www.meteoservice.ru/export/gismeteo/',
                           params={'point': str(currentPoint) + ".xml"})
    stringWithXml = xmlFile.text
    patternMaxTemp = re.compile(r'(TEMPERATURE max="-?\d*" min="-?\d*")')
    patternNumbers = re.compile(r"(\d+)")
    patternForeCastDay = re.compile(r'<FORECAST day="\d*"')
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrowDay = tomorrow.strftime('%d')
    for find in patternMaxTemp.findall(stringWithXml):
        listWithFindTemp.append(find)
    for day in patternForeCastDay.findall(stringWithXml):
        listWithDays.append(patternNumbers.findall(day))
    flatList = [item for sublist in listWithDays for item in sublist]
    dictWithWeather = dict(zip(listWithFindTemp, flatList))
    dictWithTomorrowWeather = {}
    # print(dictWithWeather)
    for key, value in dictWithWeather.items():
        if int(value) == int(tomorrowDay):
            dictWithTomorrowWeather.setdefault(key, value)
    # print(dictWithTomorrowWeather)
    stringWithTomorrowWeather = str(dictWithTomorrowWeather)
    for formTemp in patternMaxTemp.findall(stringWithTomorrowWeather):
        listTomorrowWeather.append(formTemp)
    for numbers in patternNumbers.findall(str(listTomorrowWeather)):
        listWIthData.append(int(numbers))
    # print(listWIthData)
    averageTemp = round(sum(listWIthData) / len(listWIthData), 1)
    print(averageTemp)
    # print(len(listWIthData))
