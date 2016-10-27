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

class Fix():
    def __init__(self, logFile="log.txt"):
        if (type(logFile) != str or len(logFile) < 1):
            raise ValueError("Fix.__init__:  logFile should be a string with length greater than or equal to 1.")
        try:
            f = open(logFile, "a")
        except IOError:
            raise ValueError("Fix.__init__:  logFile could not be opened.")
        self.logFile = logFile
        self.log("Log File:\t" + os.path.abspath(logFile))
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
        self.log("Sighting File:\t" + os.path.abspath(sightingFile))
        output = os.path.abspath(sightingFile)
        return output
    
    def setAriesFile(self, ariesFile):
        if (type(ariesFile) != str or len(ariesFile) < 5):
            raise ValueError("Fix.setAriesFile:  ariesFile must be a string that is the filename of a .txt filetype.")
        if (ariesFile.find(".txt") == -1):
            raise ValueError("Fix.setAriesFile:  ariesFile must be a .txt file.")
        try:
            f = open(ariesFile, "r")
        except IOError:
            raise ValueError("Fix.setAriesFile:  ariesFile could not be opened.")
        self.ariesFile = ariesFile
        self.log("Aries File:\t" + os.path.abspath(ariesFile))
        output = os.path.abspath(ariesFile)
        return output
    
    def setStarFile(self, starFile):
        if (type(starFile) != str or len(starFile) < 5):
            raise ValueError("Fix.setStarFile:  starFile must be a string that is the filename of a .txt filetype.")
        if (starFile.find(".txt") == -1):
            raise ValueError("Fix.setStarFile:  starFile must be a .txt file.")
        try:
            f = open(starFile, "r")
        except IOError:
            raise ValueError("Fix.setStarFile:  starFile could not be opened.")
        self.starFile = starFile
        self.log("Star File:\t" + os.path.abspath(starFile))
        output = os.path.abspath(starFile)
        return output
    
    def getSightings(self):
        if (self.sightingFile == None):
            raise ValueError("Fix.getSightings:  no sightingFile has been set.")
        
        try:
            tree = ET.parse(self.sightingFile)
        except IOError:
            raise ValueError("Fix.getSightings:  could not parse xml file.")
        
        fix = tree.getroot()
        if (fix.tag != "fix"):
            raise ValueError("Fix.getSightings:  root tag is not fix.")
        
        sightingsList = []
        
        for sighting in fix.findall('sighting'):
            if (sighting.tag != "sighting"):
                raise ValueError("Fix.getSightings:  child tag of fix is not a sighting tag.")
            if (sighting.find('body') == None):
                raise ValueError("Fix.getSightings:  no body tag in sighting.")
            elif (sighting.find('body').text == None):
                raise ValueError("Fix.getSightings:  empty body tag in sighting.")
            else:
                body = sighting.find('body').text
            if (sighting.find('date') == None):
                raise ValueError("Fix.getSightings:  no date tag in sighting.")
            else:
                date = sighting.find('date').text
                datePattern = re.compile("^((19|20)\\d\\d)-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$")
                if (re.match(datePattern, date) == None):
                    raise ValueError("Fix.getSightings:  invalid date format.")
            if (sighting.find('time') == None):
                raise ValueError("Fix.getSightings:  no time tag in sighting.")
            else:
                time = sighting.find('time').text
                timePattern = re.compile("^([0-1]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)")
                if (re.match(timePattern, time) == None):
                    raise ValueError("Fix.getSightings:  invalid time format.")
            if (sighting.find('observation') == None):
                raise ValueError("Fix.getSightings:  no observation tag in sighting.")
            else:
                observation = sighting.find('observation').text
                obsPattern = re.compile("^(0[0-8]\d)d([0-5]\d)(\.[0-9]?)?")
                if (re.match(obsPattern, observation) == None):
                    raise ValueError("Fix.getSightings:  invalid observation format.")
                angle1 = Angle.Angle()
                angle1.setDegreesAndMinutes(observation)
                angle2 = Angle.Angle()
                angle2.setDegreesAndMinutes("0d0.1")
                if (angle1.getDegrees() <= angle2.getDegrees()):
                    raise ValueError("Fix.getSightings:  observed altitude is less than 0d0.1.")
            if (sighting.find('height') == None):
                height = 0
            else:
                height = sighting.find('height').text
                heightPattern = re.compile("^\d*\.?\d*$")
                if (re.match(heightPattern, height) == None):
                    raise ValueError("Fix.getSightings:  invalid height.")
                height = float(height)
            if (sighting.find('temperature') == None):
                temperature = 72
            else:
                temperature = int(sighting.find('temperature').text)
                if (temperature > 120 or temperature < -20):
                    raise ValueError("Fix.getSightings:  temperature is out of range.")
            if (sighting.find('pressure') == None):
                pressure = 1010
            else:
                pressure = sighting.find('pressure').text.strip()
                presPattern = re.compile("^\d*$")
                if (re.match(presPattern, pressure) == None):
                    raise ValueError("Fix.getSightings:  invalid pressure.")
                pressure = int(pressure)
                if (pressure < 100 or pressure > 1100):
                    raise ValueError("Fix.getSightings:  pressure is out of range.")
            if (sighting.find('horizon') == None):
                horizon = "natural"
            else:
                horizon = sighting.find('horizon').text.lower()
                horizonPattern = re.compile("(artificial|natural)")
                if (re.match(horizonPattern, horizon) == None):
                    raise ValueError("Fix.getSightings:  invalid horizon.")
                
            adjAltitude = self.adjustAltitude(horizon, height, pressure, temperature, observation)
                
            sightingsListLine = [body, date, time, observation, height, temperature, pressure, horizon, adjAltitude]
            sightingsList.append(sightingsListLine)
            
        sightingsList.sort(key=lambda x: (x[1], x[2], x[0]))
        
        for sightingEntry in sightingsList:
            self.log(sightingEntry[0] + '\t' + sightingEntry[1] + '\t' + sightingEntry[2] + '\t' + sightingEntry[8])
            
        self.log("End of sighting file " + self.sightingFile)
        
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        return (approximateLatitude, approximateLongitude)
    
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
        if (horizon == "natural" or "Natural"):
            dip = (-0.97 * math.sqrt(height)) / 60
        else:
            dip = 0
            
        altitude = Angle.Angle()
        altitude.setDegreesAndMinutes(observation)
            
        refraction = (-0.00452 * pressure) / (273 + ((temperature - 32) * 5 / 9)) / math.tan(altitude.getDegrees() / 180 * math.pi)
        
        adjustedAltitude = altitude.getDegrees() + dip + refraction
        
        altitude.setDegrees(adjustedAltitude)
        
        return altitude.getString()
        