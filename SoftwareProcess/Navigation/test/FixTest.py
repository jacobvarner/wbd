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
        self.assertNotEqual(str.find("Start of log"), -1)
        
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
#               boolean - true if f.xml is new, false if it already exists
#           state change:
#               writes to the log file
#
#    Happy path
    def test200_010_ShouldWriteToLogFile(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(str.find("Start of sighting file"), -1)
        
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
#                none
#            outputs:
#                Tuple with latitude and longitude of approximate location
#            state change:
#                Navigation calculations are written to the log file
#
#    Happy path
    def test300_010_ShouldReturnTuple(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        self.assertEquals(len(aFix.getSightings()), 2)
        
    def test300_020_ShouldWriteToLog(self):
        aFix = Fix.Fix("test.txt")
        aFix.setSightingFile("file.xml")
        aFix.getSightings()
        f = open("test.txt", "r")
        str = f.read()
        self.assertNotEqual(re.search(r'\d+-\d+-\d+\s\d+:\d+:\d', str), None)
        
    def test300_910_ShouldReturnValueErrorForNoSightingFile(self):
        expectedDiag = "Fix.getSightings:  "
        aFix = Fix.Fix("test.txt")
        with self.assertRaises(ValueError) as context:
            aFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    