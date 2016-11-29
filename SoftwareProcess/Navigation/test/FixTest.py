import unittest
import Navigation.prod.Fix as Fix
import re


class FixTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    
#   Acceptance Test 100
#       Analysis - Constructor
#           inputs:
#               logFile
#           outputs:
#               an instance of fix
#           state change:
#               starts the log file
#
#    Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
        
    def test100_020_ShouldCreateLogFile(self):
        aFix = Fix.Fix("test.txt")
        f = open("test.txt", "r")
        self.assertEquals("test.txt", f.name)
        
    def test100_030_ShouldContainInitialTextinLogFile(self):
        aFix = Fix.Fix("test.txt")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(str.find("Log file:\t"), -1)
        
#    Sad path        
    def test100_910_ShouldReturnValueErrorForWrongFileInputStringLength(self):
        expectedDiag = "Fix.__init__:  "
        with self.assertRaises(ValueError) as context:
            aFix = Fix.Fix(1)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test100_920_ShouldReturnValueErrorForFileError(self):
        expectedDiag = "Fix.__init__:  "
        with self.assertRaises(ValueError) as context:
            aFix = Fix.Fix(22)
            f = open("test", "r")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
#   Acceptance Test 200
#       Analysis - setSightingFile
#           inputs:
#               f.xml - sighting file where f is the filename
#           outputs:
#              absolute filepath of the file
#           state change:
#               writes to the log file
#
#    Happy path
    def test200_010_ShouldWriteToLogFile(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(str.find("Sighting file:\t"), -1)
        
#    Sad path
    def test200_910_ShouldRaiseValueErrorForWrongFileFormatt(self):
        expectedDiag = "Fix.setSightingFile:  "
        with self.assertRaises(ValueError) as context:
            aFix = Fix.Fix("test.txt")
            aFix.setSightingFile("test.txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
#    Acceptance Test 300
#        Analysis - getSightings
#            inputs:
#                assumedLatitude, assumedLongitude
#            outputs:
#                Tuple with latitude and longitude of approximate location
#            state change:
#                Navigation calculations are written to the log file
#
#    Happy path
    def test300_010_ShouldReturnTuple(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        aFix.setAriesFile("aries.txt")
        aFix.setStarFile("stars.txt")
        self.assertEquals(type(aFix.getSightings()), tuple)
        
    def test300_020_ShouldWriteToLog(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        aFix.setAriesFile("aries.txt")
        aFix.setStarFile("stars.txt")
        aFix.getSightings("S13d13.9", "32d32.2")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(re.search(r'\d+-\d+-\d+\s\d+:\d+:\d', str), None)
        
    def test300_910_ShouldReturnValueErrorForNoSightingFile(self):
        expectedDiag = "Fix.getSightings:  "
        aFix = Fix.Fix("test.txt")
        with self.assertRaises(ValueError) as context:
            aFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_920_ShouldReturnValueErrorForWrongFormatAssumedLatitude(self):
        expectedDiag = "Fix.getSightings:  "
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        aFix.setAriesFile("aries.txt")
        aFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            aFix.getSightings("test", "0d0.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_930_ShouldReturnValueErrorForWrongFormatAssumedLongitude(self):
        expectedDiag = "Fix.getSightings:  "
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        aFix.setAriesFile("aries.txt")
        aFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            aFix.getSightings("S10d1.5", "test")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
#   Acceptance Test 400
#       Analysis - setAriesFile
#           inputs:
#               f.txt - Aries file where f is the filename
#           outputs:
#               the absolute filepath of the file
#           state change:
#               writes to the log file
#
#    Happy path
    def test400_010_ShouldWriteToLogFile(self):
        aFix = Fix.Fix("test.txt")
        aFix.setStarFile("aries.txt")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(str.find("Aries file:\t"), -1)
        
#    Sad path
    def test400_910_ShouldRaiseValueErrorForWrongFileFormatt(self):
        expectedDiag = "Fix.setAriesFile:  "
        with self.assertRaises(ValueError) as context:
            aFix = Fix.Fix("test.txt")
            aFix.setAriesFile("aries.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

#   Acceptance Test 500
#       Analysis - setStarFile
#           inputs:
#               f.txt - Star file where f is the filename
#           outputs:
#               the absolute filepath of the file
#           state change:
#               writes to the log file
#
#    Happy path
    def test500_010_ShouldWriteToLogFile(self):
        aFix = Fix.Fix("test.txt")
        aFix.setStarFile("stars.txt")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(str.find("Star file:\t"), -1)
        
#    Sad path
    def test500_910_ShouldRaiseValueErrorForWrongFileFormatt(self):
        expectedDiag = "Fix.setStarFile:  "
        with self.assertRaises(ValueError) as context:
            aFix = Fix.Fix("test.txt")
            aFix.setStarFile("star.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    