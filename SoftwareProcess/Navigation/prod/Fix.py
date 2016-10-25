'''
    
    Fix is a class for reading and adjusting star readings measurements.
    
    Created on Oct. 9, 2016
    
    @author: Jacob Varner

'''
import datetime
import xml.etree.ElementTree as ET
import math
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
        self.log("Log File:" + '\t' + os.path.abspath(logFile))
        self.sightingFile = None
    
    def setSightingFile(self, sightingFile):
        if (type(sightingFile) != str or len(sightingFile) < 5):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a string that is the filename of a .xml filetype.")
        if (sightingFile.find(".xml") == -1):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a .xml file.")
        try:
            f = open(sightingFile, "r")
        except IOError:
            raise ValueError("Fix.setSightingFile:  sightingFile could not be opened.")
        if (self.sightingFile == sightingFile):
            output = False
        else:
            self.sightingFile = sightingFile
            output = True
        self.log("Sighting File:" + '\t' + os.path.abspath(sightingFile))    
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
            else:
                body = sighting.find('body').text
            if (sighting.find('date') == None):
                raise ValueError("Fix.getSightings:  no date tag in sighting.")
            else:
                date = sighting.find('date').text
            if (sighting.find('time') == None):
                raise ValueError("Fix.getSightings:  no time tag in sighting.")
            else:
                time = sighting.find('time').text
            if (sighting.find('observation') == None):
                raise ValueError("Fix.getSightings:  no observation tag in sighting.")
            else:
                observation = sighting.find('observation').text
                angle1 = Angle.Angle()
                angle1.setDegreesAndMinutes(observation)
                angle2 = Angle.Angle()
                angle2.setDegreesAndMinutes("0d0.1")
                if (angle1.getDegrees() <= angle2.getDegrees()):
                    raise ValueError("Fix.getSightings:  observed altitude is less than 0d0.1.")
            if (sighting.find('height') == None):
                height = 0
            else:
                height = float(sighting.find('height').text)
                if (height < 0):
                    raise ValueError("Fix.getSightings:  height must be greater than or equal to zero.")
            if (sighting.find('temperature') == None):
                temperature = 72
            else:
                temperature = int(sighting.find('temperature').text)
                if (temperature > 120 or temperature < -20):
                    raise ValueError("Fix.getSightings:  temperature is out of range.")
            if (sighting.find('pressure') == None):
                pressure = 1010
            else:
                pressure = int(sighting.find('pressure').text)
                if (pressure < 100 or pressure > 1100):
                    raise ValueError("Fix.getSightings:  pressure is out of range.")
            if (sighting.find('horizon') == None):
                horizon = "natural"
            else:
                horizon = sighting.find('horizon').text
                
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
        