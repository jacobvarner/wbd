'''
    
    Fix is a class for reading and adjusting star readings measurements.
    
    Created on Oct. 9, 2016
    
    @author: Jacob Varner

'''
import datetime
import xml.etree.ElementTree as ET
import math
import re
import Navigation.prod.Angle as Angle
import os
from numpy import arcsin, sin, cos, pi, arccos, float64
import numpy as np

class Fix():
    def __init__(self, logFile="log.txt"):
        if (type(logFile) != str or len(logFile) < 1):
            raise ValueError("Fix.__init__:  logFile should be a string with length greater than or equal to 1.")
        try:
            f = open(logFile, "a")
        except IOError:
            raise ValueError("Fix.__init__:  logFile could not be opened.")
        self.logFile = logFile
        self.log("Log file:\t" + os.path.abspath(logFile))
        self.sightingFile = None
        self.ariesFile = None
        self.starFile = None
    
    def setSightingFile(self, sightingFile="0"):
        if (sightingFile == "0"):
            raise ValueError("Fix.setSightingFile:  a valid sighting file is required.")
        if (type(sightingFile) != str or len(sightingFile) < 5):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a string that is the filename of a .xml filetype.")
        if (sightingFile.find(".xml") == -1):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a .xml file.")
        try:
            f = open(sightingFile, "r")
        except IOError:
            raise ValueError("Fix.setSightingFile:  sightingFile could not be opened.")
        self.sightingFile = sightingFile
        self.log("Sighting file:\t" + os.path.abspath(sightingFile))
        output = os.path.abspath(sightingFile)
        return output
    
    def setAriesFile(self, ariesFile="0"):
        if (ariesFile == "0"):
            raise ValueError("Fix.setAriesFile:  a valid aries file is required.")
        if (type(ariesFile) != str or len(ariesFile) < 5):
            raise ValueError("Fix.setAriesFile:  ariesFile must be a string that is the filename of a .txt filetype.")
        if (ariesFile.find(".txt") == -1):
            raise ValueError("Fix.setAriesFile:  ariesFile must be a .txt file.")
        try:
            f = open(ariesFile, "r")
        except IOError:
            raise ValueError("Fix.setAriesFile:  ariesFile could not be opened.")
        self.ariesFile = ariesFile
        self.log("Aries file:\t" + os.path.abspath(ariesFile))
        output = os.path.abspath(ariesFile)
        return output
    
    def setStarFile(self, starFile="0"):
        if (starFile == "0"):
            raise ValueError("Fix.setStarFile:  a valid star file is required.")
        if (type(starFile) != str or len(starFile) < 5):
            raise ValueError("Fix.setStarFile:  starFile must be a string that is the filename of a .txt filetype.")
        if (starFile.find(".txt") == -1):
            raise ValueError("Fix.setStarFile:  starFile must be a .txt file.")
        try:
            f = open(starFile, "r")
        except IOError:
            raise ValueError("Fix.setStarFile:  starFile could not be opened.")
        self.starFile = starFile
        self.log("Star file:\t" + os.path.abspath(starFile))
        output = os.path.abspath(starFile)
        return output
    
    def getSightings(self, assumedLatitude="0d0.0", assumedLongitude="0d0.0"):
        if (self.sightingFile == None):
            raise ValueError("Fix.getSightings:  no sightingFile has been set.")
        if (self.ariesFile == None):
            raise ValueError("Fix.getSightings:  no ariesFile has been set.")
        if (self.starFile == None):
            raise ValueError("Fix.getSightings:  no starFile has been set.")
        
        if (type(assumedLatitude) != str or len(assumedLatitude) < 5):
            raise ValueError("Fix.getSightings:  assumedLatitude must be a string in the format h0d0.0")
        if (assumedLatitude.find("d") == -1):
            raise ValueError("Fix.getSightings:  assumedLatitude must be a string in the format h0d0.0")
        
        if (type(assumedLongitude) != str or len(assumedLongitude) < 5):
            raise ValueError("Fix.getSightings:  assumedLongitude must be a string in the format h0d0.0")
        if (assumedLongitude.find("d") == -1):
            raise ValueError("Fix.getSightings:  assumedLongitude must be a string in the format h0d0.0")
        
        if (len(assumedLatitude) == 5):
            if (assumedLatitude.find("0d0.0") == -1):
                raise ValueError("Fix.getSightings:  assumedLatitude must be 0d0.0 if h is missing.")
            
        if (assumedLatitude.find("0d0.0") != -1):
            if (len(assumedLatitude) != 5):
                raise ValueError("Fix.getSightings:  assumedLatitude must not have h if it's equal to 0d0.0.")
            
        assumedLatitudeHemi = ""
        if (assumedLatitude.find("S") == 0 or assumedLatitude.find("N") == 0):
            assumedLatitudeHemi = assumedLatitude[0];
            assumedLatitude = assumedLatitude[1:len(assumedLatitude)]
        
        try:
            tree = ET.parse(self.sightingFile)
        except IOError:
            raise ValueError("Fix.getSightings:  could not parse xml file.")
        
        fix = tree.getroot()
        if (fix.tag != "fix"):
            raise ValueError("Fix.getSightings:  root tag is not fix.")
        
        sightingsList = []
        numSightingErrors = 0
        
        for sighting in fix.findall('sighting'):
            if (sighting.tag != "sighting"):
                numSightingErrors = numSightingErrors + 1
                continue
            if (sighting.find('body') == None):
                numSightingErrors = numSightingErrors + 1
                continue
            elif (sighting.find('body').text == None):
                numSightingErrors = numSightingErrors + 1
                continue
            else:
                body = sighting.find('body').text
            if (sighting.find('date') == None):
                numSightingErrors = numSightingErrors + 1
                continue
            else:
                date = sighting.find('date').text
                datePattern = re.compile("^((19|20)\\d\\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$")
                if (re.match(datePattern, date) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
            if (sighting.find('time') == None):
                numSightingErrors = numSightingErrors + 1
                continue
            else:
                time = sighting.find('time').text
                timePattern = re.compile("^([0-1]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)")
                if (re.match(timePattern, time) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
            if (sighting.find('observation') == None):
                numSightingErrors = numSightingErrors + 1
                continue
            else:
                observation = sighting.find('observation').text
                obsPattern = re.compile("^(0[0-8]\d)d([0-5]\d)(\.[0-9]?)?")
                if (re.match(obsPattern, observation) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
                angle1 = Angle.Angle()
                angle1.setDegreesAndMinutes(observation)
                angle2 = Angle.Angle()
                angle2.setDegreesAndMinutes("0d0.1")
                if (angle1.getDegrees() <= angle2.getDegrees()):
                    numSightingErrors = numSightingErrors + 1
                    continue
            if (sighting.find('height') == None):
                height = 0
            else:
                height = sighting.find('height').text
                heightPattern = re.compile("^\d*\.?\d*$")
                if (re.match(heightPattern, height) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
                height = float(height)
            if (sighting.find('temperature') == None):
                temperature = 72
            else:
                temperature = int(sighting.find('temperature').text)
                if (temperature > 120 or temperature < -20):
                    numSightingErrors = numSightingErrors + 1
                    continue
            if (sighting.find('pressure') == None):
                pressure = 1010
            else:
                pressure = sighting.find('pressure').text.strip()
                presPattern = re.compile("^\d*$")
                if (re.match(presPattern, pressure) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
                pressure = int(pressure)
                if (pressure < 100 or pressure > 1100):
                    numSightingErrors = numSightingErrors + 1
                    continue
            if (sighting.find('horizon') == None):
                horizon = "natural"
            else:
                horizon = sighting.find('horizon').text.lower()
                horizonPattern = re.compile("(artificial|natural)")
                if (re.match(horizonPattern, horizon) == None):
                    numSightingErrors = numSightingErrors + 1
                    continue
                
            adjAltitude = self.adjustAltitude(horizon, height, pressure, temperature, observation)
            
            geoPosLocation = self.getGeoPosition(body, date, time)
            if (geoPosLocation == None):
                numSightingErrors = numSightingErrors + 1
                continue
            
            result = self.getAzimuthAndDistance(geoPosLocation, assumedLongitude, assumedLatitude, adjAltitude)
            azimuth = result[0]
            distance = result[1]
                
            sightingsListLine = [body, date, time, observation, height, temperature, pressure, horizon,
                                 adjAltitude, geoPosLocation, azimuth, distance]
            sightingsList.append(sightingsListLine)
            
        sightingsList.sort(key=lambda x: (x[1], x[2], x[0]))
        
        for sightingEntry in sightingsList:
            self.log(sightingEntry[0] + '\t' + sightingEntry[1] + '\t' + sightingEntry[2] + '\t' + sightingEntry[8]
                     + '\t' + sightingEntry[9][0] + '\t' + sightingEntry[9][1] + '\t' + assumedLatitudeHemi + assumedLatitude
                     + '\t' + assumedLongitude + '\t' + sightingEntry[10] + '\t' + str(sightingEntry[11]))
        
        self.log("Sighting errors:\t" + str(numSightingErrors))
        
        approximateLatitude = self.getApproximateLocation(sightingsList, assumedLatitude, assumedLongitude)[0]
        approximateLongitude = self.getApproximateLocation(sightingsList, assumedLatitude, assumedLongitude)[1]
        self.log("Approximate latitude:\t" + assumedLatitudeHemi + approximateLatitude + '\tApproximate longitude:\t' + approximateLongitude) 
        
        self.log("End of sighting file " + self.sightingFile)
        
        return (approximateLatitude, approximateLongitude)
    
    def getApproximateLocation(self, sightingsList, assumedLatitude, assumedLongitude):
        sumLatitude = 0
        for sighting in sightingsList:
            azimuthAngle = Angle.Angle()
            azimuthAngle.setDegreesAndMinutes(sighting[10])
            sumLatitude += np.float64((sighting[11] * pi / 180.0) * cos(azimuthAngle.getDegrees() * pi / 180.0)).item()
            
        approximateLatitudeAngle = Angle.Angle()
        approximateLatitudeAngle.setDegrees(sumLatitude / 60.0)
        assumedLatitudeAngle = Angle.Angle()
        assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        approximateLatitudeAngle.add(assumedLatitudeAngle)
        approximateLatitude = approximateLatitudeAngle.getString()
        
        sumLongitude = 0
        for sighting in sightingsList:
            azimuthAngle = Angle.Angle()
            azimuthAngle.setDegreesAndMinutes(sighting[10])
            sumLongitude += np.float64((sighting[11] * pi / 180.0) * sin(azimuthAngle.getDegrees() * pi / 180.0)).item()
            
        approximateLongitudeAngle = Angle.Angle()
        approximateLongitudeAngle.setDegrees(sumLongitude / 60.0)
        assumedLongitudeAngle = Angle.Angle()
        assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)
        approximateLongitudeAngle.add(assumedLongitudeAngle)
        approximateLongitude = approximateLongitudeAngle.getString()
        
        return [approximateLatitude, approximateLongitude]
    
    def getAzimuthAndDistance(self, geoPosLocation, assumedLongitude, assumedLatitude, adjAltitude):
        assumedLongitudeAngle = Angle.Angle()
        assumedLatitudeAngle = Angle.Angle()
        assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)
        assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        lhaAngle = Angle.Angle()
        lhaAngle.setDegreesAndMinutes(geoPosLocation[1])
        lhaAngle.subtract(assumedLongitudeAngle)
        geoLatitudeAngle = Angle.Angle()
        geoLongitudeAngle = Angle.Angle()
        geoLatitudeAngle.setDegreesAndMinutes(geoPosLocation[0])
        geoLongitudeAngle.setDegreesAndMinutes(geoPosLocation[1])
        
        correctedAltitudeRaw = arcsin((sin(geoLatitudeAngle.getDegrees() * pi / 180.0) * sin(assumedLatitudeAngle.getDegrees() * pi / 180.0)) + (cos(geoLatitudeAngle.getDegrees() * pi / 180.0) * cos(assumedLatitudeAngle.getDegrees() * pi / 180.0) * cos(lhaAngle.getDegrees() * pi / 180.0)))
        
        correctedAltitude = np.float64(correctedAltitudeRaw).item()
        
        correctedAltitudeAngle = Angle.Angle()
        correctedAltitudeAngle.setDegrees(correctedAltitude)
        
        adjustedAltitudeTemp = Angle.Angle()
        adjustedAltitudeTemp.setDegreesAndMinutes(adjAltitude)
        adjustedAltitudeTemp.subtract(correctedAltitudeAngle)
        distance = int(round(adjustedAltitudeTemp.getDegrees(), 0))
        
        azimuthRaw = arccos((sin(geoLatitudeAngle.getDegrees() * pi / 180.0) - sin(assumedLatitudeAngle.getDegrees() * pi / 180.0)) * sin(distance * pi / 180)) / (cos(assumedLatitudeAngle.getDegrees() * pi / 180.0) * cos(distance * pi / 180.0))
        
        azimuth = np.float64(azimuthRaw).item()
        azimuthAngle = Angle.Angle()
        azimuthAngle.setDegrees(azimuth)
        azimuth = azimuthAngle.getString()
        
        return [azimuth, distance]
    
    def log(self, logString):
        entry = "LOG:\t"
        entry += datetime.datetime.now().isoformat(' ')
        entry += "-06:00\t"
        entry += logString + "\n"
        
        try:
            f = open(self.logFile, "a")
        except IOError:
            raise ValueError("Fix.__init__:  logFile could not be opened.")
        
        f.write(entry)
        
    def adjustAltitude(self, horizon, height, pressure, temperature, observation):
        if (horizon == "natural"):
            dip = (-0.97 * math.sqrt(height)) / 60
        else:
            dip = 0
            
        altitude = Angle.Angle()
        altitude.setDegreesAndMinutes(observation)
            
        refraction = (-0.00452 * pressure) / (273 + ((temperature - 32) * 5 / 9)) / math.tan(altitude.getDegrees() / 180 * math.pi)
        
        adjustedAltitude = altitude.getDegrees() + dip + refraction
        
        altitude.setDegrees(adjustedAltitude)
        
        return altitude.getString()
    
    def getGeoPosition(self, body, date, time):
        with open(self.starFile) as starFile:
            starsList = starFile.readlines()
            
        starMatches = []
        for star in starsList:
            if (star.split('\t')[0] == body):
                starMatches.append(star)
                
        if (len(starMatches) == 0):
            return None
                
        starMatch = None
                
        for star in starMatches:
            starMatchDate = star.split('\t')[1]
            keyMonth = date.split('-')[1]
            keyDay = date.split('-')[2]
            starMatchMonth = starMatchDate.split('/')[0]
            starMatchDay = starMatchDate.split('/')[1]
            
            if (keyMonth >= starMatchMonth and keyDay >= starMatchDay):
                starMatch = star
            else:
                break
            
        latitude = starMatch.split('\t')[3].strip()
        shaStar = starMatch.split('\t')[2].strip()
        
        with open(self.ariesFile) as ariesFile:
            ariesList = ariesFile.readlines()
            
        ariesMatch = None
        index = 0
        
        for aries in ariesList:
            ariesMatchDate = aries.split('\t')[0]
            keyMonth = date.split('-')[1]
            keyDay = date.split('-')[2]
            keyHour = time.split(':')[0]
            if (keyHour[0] == '0'):
                keyHour = keyHour[1];
            ariesMatchMonth = ariesMatchDate.split('/')[0]
            ariesMatchDay = ariesMatchDate.split('/')[1]
            ariesMatchHour = aries.split('\t')[1]
            
            if (ariesMatchMonth == keyMonth and ariesMatchDay == keyDay and ariesMatchHour == keyHour):
                ariesMatch = aries
                break
            else:
                index = index + 1
                continue
            
        if (ariesMatch == None):
            return None
        
        ghaAries1 = ariesMatch.split('\t')[2].strip()
        ghaAries2 = ariesList[index + 1].split('\t')[2].strip()
        
        minutes = int(time.split(':')[1])
        seconds = int(time.split(':')[2])
        s = 60.0 * minutes + seconds
        
        ghaAriesAngle1 = Angle.Angle()
        ghaAriesAngle2 = Angle.Angle()
        ghaAriesAngle1.setDegreesAndMinutes(ghaAries1)
        ghaAriesAngle2.setDegreesAndMinutes(ghaAries2)
        ghaAriesAngle2.subtract(ghaAriesAngle1)
        tempAngle = ghaAriesAngle2.getDegrees()
        tempAngle = tempAngle * (s / 3600.0)
        ghaAriesAngle2.setDegrees(tempAngle)
        ghaAriesAngle1.add(ghaAriesAngle2)
        shaStarAngle = Angle.Angle()
        shaStarAngle.setDegreesAndMinutes(shaStar)
        shaStarAngle.add(ghaAriesAngle1)
        
        longitude = shaStarAngle.getString()
        
        output = [latitude, longitude]
        return output