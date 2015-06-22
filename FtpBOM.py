__author__ = 'Dean'

import ftplib, io, json

# TODO Make this shit into a class
# TODO convert forecast into percentage based on prediction when dict is being created


keyList = ['loc_id', 'location', 'state', 'forecast_date', 'date', 'issue_time', 'min_0', 'max_0', 'min_1', 'max_1',
           'min_2', 'max_2', 'min_4', 'max_4', 'min_5', 'max_5', 'min_6', 'max_6', 'min_7', 'max_7', 'forecast_0',
           'forecast_1', 'forecast_2', 'forecast_3', 'forecast_4', 'forecast_5', 'forecast_6', 'forecast_7'
           ]

rawFile = ''


def main():
    weatherDataFile = "IDA00001.dat"
    uvdataFile = 'IDYGP007.txt'
    rawWeather = ftpGetFiles(weatherDataFile)
    rawUVData = ftpGetFiles(uvdataFile)
    weatherOutput = cleanRawWeather(rawWeather)
    uvOutput = processUVData(rawUVData)
    for city in uvOutput:
        if city[0] in weatherOutput:
            info = weatherOutput.get(city[0])
            reading = city[1]
            info['UVReading'] = reading
    print(weatherOutput["Townsville"])


def saveJSONFile(dict):
    """
    :param dict: Python Dictionary
    :return: Null
    """


def ftpGetFiles(retriveFile):
    global rawFile
    rawFile = ''
    BOMURL = 'ftp.bom.gov.au'
    ftp = ftplib.FTP(BOMURL)
    ftp.login()
    ftp.cwd('anon')
    ftp.cwd('gen')
    ftp.cwd('fwo')
    ftp.retrbinary('RETR %s' % retriveFile, filewriter)
    ftp.close()
    return rawFile


def cleanRawWeather(inputWeatherData):
    """
    :rtype : Returns A Dict that conforms to '"Location" : "Weather Data"'
    """
    global keyList
    endDict = {}
    inputWeatherData = inputWeatherData.split('\n')
    inputWeatherData.remove(inputWeatherData[0])
    inputWeatherData = formatOutput(inputWeatherData, '')
    for i in inputWeatherData:
        rowSet = i.split('#')
        counter = 0
        rowDict = {}
        for value in rowSet:
            try:
                heading = keyList[counter]
            except IndexError:
                break
            counter += 1
            rowDict[heading] = value
        endDict[rowDict['location']] = rowDict

    return endDict


def processUVData(uvfile):
    uvfile = uvfile.split('\n')
    uvfile = formatOutput(uvfile, '')
    uvfile.remove(uvfile[0])
    uvfile.remove('Copyright Commonwealth of Australia 2011, Bureau of Meteorology (ABN 92 637 533')
    uvfile.remove('conditions described in the Copyright, Disclaimer, and Privacy statements')
    uvfile.remove('532).  Users of these web pages are deemed to have read and accepted the')
    uvfile.remove('(http://www.bom.gov.au/other/copyright.shtml).')
    shinyCity = []

    for i in uvfile:
        UV = i[len(i) - 1]
        cityRaw = i[18:37].split(" ")
        cityRaw = formatOutput(cityRaw, '')
        if len(cityRaw) == 1:
            tempA = [cityRaw[0], UV]
            shinyCity.append(tempA)
        if len(cityRaw) == 2 or len(cityRaw) == 3:
            tempA = [" ".join(cityRaw), UV]
            shinyCity.append(tempA)
    return shinyCity


def formatOutput(array, removeVar):
    array[:] = (value for value in array if value != removeVar)
    return array


def filewriter(data):
    global rawFile
    rawFile += data


main()
