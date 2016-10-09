'''
    
    Fix is a class for reading and adjusting star readings measurements.
    
    Created on Oct. 9, 2016
    
    @author: Jacob Varner

'''
import datetime

class Fix():
    def __init__(self, logFile="log.txt"):
        if (type(logFile) != str or len(logFile) < 1):
            raise ValueError("Fix.__init__:  logFile should be a string with length greater than or equal to 1")
        try:
            f = open(logFile, "a")
        except IOError:
            raise ValueError("Fix.__init__:  logFile could not be opened.")
        f.write(self.logPrefix() + "Start of log")
        pass
    
    def setSightingFile(self, sightingFile):
        pass
    
    def getSightings(self):
        pass
    
    def logPrefix(self):
        output = "LOG:\t"
        output += datetime.datetime.now().isoformat(' ')
        output += "-06:00"
        output += ":\t"
        return output