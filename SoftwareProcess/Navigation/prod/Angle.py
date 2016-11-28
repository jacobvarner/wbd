'''
    
    Angle is a class for performing operations on an Angle that contains degrees and minutes.
    
    Created on Sep 9, 2016
    
    @author: Jacob Varner

'''
from objc._objc import NULL
class Angle():
    def __init__(self):
        # self.angle = ...       set to 0 degrees 0 minutes
        self.angle = 0.0
        pass
    
    def setDegrees(self, degrees = 0):
        if (type(degrees) != int and type(degrees) != float):
            raise ValueError("Angle.setDegrees:  'degrees' must be either an integer or floating point value.")
        degrees = round(degrees * 60.0, 1) / 60.0
        degrees = float(degrees % 360)
        self.angle = degrees
        return self.angle
        pass
    
    def setDegreesAndMinutes(self, angleString):
        separator = angleString.find('d');
        if (separator == -1):
            raise ValueError("Angle.setDegreesAndMinutes:  'angleString' must contain a separator and take the form 'xdy.y' or 'xdy'.")
        if (separator == 0):
            raise ValueError("Angle.setDegreesAndMinutes:  The degree value is missing.")
        degrees = angleString[0:separator]
        if (degrees.find('.') != -1):
            raise ValueError("Angle.setDegreesAndMinutes:  The degree value must be an integer.")
        try:
            degrees = int(degrees)
        except ValueError:
            raise ValueError("Angle.setDegreesAndMinutes:  The degree value must be an integer.")
        minutes = angleString[separator + 1:]
        if (len(minutes) == 0):
            raise ValueError("Angle.setDegreesAndMinutes: The minutes value is missing.")
        minutesSeparator = minutes.find('.')
        if (minutesSeparator == -1):
            try:
                minutes = int(minutes)
            except ValueError:
                raise ValueError("Angle.setDegreesAndMinutes:  The minutes value must be an integer or a floating point value.")
        else:
            if (len(minutes[minutesSeparator + 1:]) > 1):
                raise ValueError("Angle.setDegreesAndMinutes:  The minute value may only have one digit to the right of the decimal point.")
            try:
                minutes = float(minutes)
            except ValueError:
                raise ValueError("Angle.setDegreesAndMinutes:  The minute value must be an integer or a floating point value.")
        if (minutes < 0):
            raise ValueError("Angle.setDegreesAndMinutes:  The minute value must be a positive value.")
        elif (minutes == 60):
            degrees = degrees + 1
            degrees = degrees % 360
            minutes = 0
        elif (minutes > 60):
            degrees = degrees + int(minutes / 60)
            degrees = degrees % 360
            minutes = minutes % 60
            
        minutesFraction = float(minutes) / 60
        if (degrees >= 0):
            degrees = degrees + minutesFraction
        else:
            degrees = (abs(degrees) + minutesFraction) * -1
        self.angle = degrees % 360
        return self.angle
        pass
    
    def add(self, angle=NULL):
        if (angle == NULL):
            raise ValueError("Angle.add:  You must pass a valid instance of Angle.")
        if (not isinstance(angle, Angle)):
            raise ValueError("Angle.add:  You must pass a valid instance of Angle.")
        totalDegrees = self.angle + angle.angle
        totalDegrees = totalDegrees % 360
        self.angle = totalDegrees
        return self.angle
        pass
    
    def subtract(self, angle=NULL):
        if (angle == NULL):
            raise ValueError("Angle.subtract:  You must pass a valid instance of Angle.")
        if (not isinstance(angle, Angle)):
            raise ValueError("Angle.subtract:  You must pass a valid instance of Angle.")
        totalDegrees = self.angle - angle.angle
        totalDegrees = totalDegrees % 360
        self.angle = totalDegrees
        return self.angle
        pass
    
    def compare(self, angle=NULL):
        if (angle == NULL):
            raise ValueError("Angle.compare:  You must pass a valid instance of Angle.")
        if (not isinstance(angle, Angle)):
            raise ValueError("Angle.compare:  You must pass a valid instance of Angle.")
        if (self.angle > angle.angle):
            return 1
        elif (self.angle < angle.angle):
            return -1
        elif (self.angle == angle.angle):
            return 0
        pass
    
    def getString(self):
        degrees = int(self.angle)
        minutesFraction = self.angle - degrees
        minutes = round(minutesFraction * 60, 1)
        string = str(degrees) + "d" + str(minutes)
        return string
        pass
    
    def getDegrees(self):
        return self.angle
        pass