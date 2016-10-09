import unittest
import Navigation.prod.Fix as Fix


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
        
    