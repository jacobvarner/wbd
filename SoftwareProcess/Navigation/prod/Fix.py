'''
    
    Fix is a class for reading and adjusting star readings measurements.
    
    Created on Oct. 9, 2016
    
    @author: Jacob Varner

'''
import datetime
import xml.etree.ElementTree as ET

class Fix():
    def __init__(self, logFile="log.txt"):
        if (type(logFile) != str or len(logFile) < 1):
            raise ValueError("Fix.__init__:  logFile should be a string with length greater than or equal to 1.")
        try:
            f = open(logFile, "a")
        except IOError:
            raise ValueError("Fix.__init__:  logFile could not be opened.")
        self.logFile = logFile
        self.log("Start of log")
        self.sightingFile = None
    
    def setSightingFile(self, sightingFile):
        if (type(sightingFile) != str or len(sightingFile) < 5):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a string that is the filename of a .xml filetype.")
        if (sightingFile.find(".xml") == -1):
            raise ValueError("Fix.setSightingFile:  sightingFile must be a .xml file.")
        try:
            f = open(sightingFile, "a")
        except IOError:
            raise ValueError("Fix.setSightingFile:  sightingFile could not be opened.")
        if (self.sightingFile == sightingFile):
            output = False
        else:
            self.sightingFile = sightingFile
            output = True
        self.log("Start of sighting file " + sightingFile)    
        return output
    
    def getSightings(self):
        pass
    
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