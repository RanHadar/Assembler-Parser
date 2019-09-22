"""
@file Commands.py

defines commands classes:
1) Command: abstract class 
2) Ains: A-instruction command
3) Cins: C-instruction command
4) Label: label statement
"""

def int2Bin(num, bits):
    """
    convert number to string of binary digits in length of bits
    numer bits are cutted if needed or padded with zeroes
    
        :param num: integer 
        :param bits: number of bits required
    """
    binValue = bin(num)[2:]
    if len(binValue) > bits:
        binValue = binValue[-bits:]

    return '0'*(bits-len(binValue)) + binValue

class Command:
    """
    abstract class command, holds Symboldict instance,
    provides methods for parse and translate
    """
    def __init__(self,symbolsDict):
        """
        init Command, store the given symbolsDict
            :param symbolsDict: the symbolDict
        """   
        self._symbolsDict = symbolsDict

    def parse(self,line,numOfLine):
        """
        parse the line, return true if succeded, false otherwise
            :param line: line to parse
            :param numOfLine: current command number
        """
        pass

    def translate(self):
        """
        return translation of the line to string of bits 
        """
        pass

class Ains(Command):
    """
    A-instruction class, command should start with '@' 
    """
    __A_CMD = "0"
    __START_STRING = "@"
    __VALUE_BITS = 15

    def __init__(self, symbolsDict):
        """
        init Ains, store the given symbolsDict
            :param symbolsDict: the symbolDict
        """
        Command.__init__(self, symbolsDict)
        self.__value = None

    def parse(self,line,numOfLine):
        """
        parse the line, return true if succeded, false otherwise
        line should start with "@", and after it symbol name or integer
            :param line: line to parse
            :param numOfLine: current command number
        """
        if line.startswith(Ains.__START_STRING):
            try:
                # try parse the the value to integer
                self.__value = int(line[1:])
            except:
                # should be symbol
                self.__value = line[1:]
            return True
        return False

    def translate(self):
        """
        return translation of the line to string of bits 
        """
        # check if value type is string
        if type(self.__value) == str:
            # if symbol is not in _symbolsDict - add it
            if self.__value not in self._symbolsDict:
                self._symbolsDict.addSymbol(self.__value)
            # retreive symbol value 
            self.__value = self._symbolsDict[self.__value]

        return Ains.__A_CMD + int2Bin(self.__value, Ains.__VALUE_BITS)


class Cins(Command):
    """
    C-instruction class, command my have '=' or ';' 
    """

    __DEST2CODE = {"M":"001", "D":"010", "MD":"011", "A":"100",
                   "AM":"101", "AD":"110", "AMD":"111", "":"000"}

    __JMP2CODE = {'JGT':"001", 'JEQ':"010", 'JGE':"011", 'JLT':"100",
                  'JNE':"101", 'JLE':"110", 'JMP':"111", "":"000"}

    __COMP2CODE = {"0":"0101010", "1":"0111111", "-1":"0111010", 
                   "D":"0001100", "A":"0110000", "!D":"0001101",
                   "!A":"0110001", "-D":"0001111", "-A":"0110011",
                   "D+1":"0011111", "A+1":"0110111", "D-1":"0001110",
                   "A-1":"0110010", "D+A":"0000010", "D-A":"0010011",
                   "A-D":"0000111", "D&A":"0000000", "D|A":"0010101",
                   "M":"1110000", "-M":"1110011", "!M":"1110001",
                   "M+1":"1110111", "M-1":"1110010", "D+M":"1000010",
                   "D-M":"1010011", "M-D":"1000111", "D&M":"1000000",
                   "D|M":"1010101", "":"0000000", "D<<":"1010110000",
                   "D>>":"1010010000", "A<<":"1010100000", "A>>":"1010000000",
                   "M<<":"1011100000", "M>>":"1011000000"}

    __C_CMD = "111"

    def __init__(self, symbolsDict):
        """
        init Cins, store the given symbolsDict
            :param symbolsDict: the symbolDict
        """
        Command.__init__(self, symbolsDict)
        self.__dest = ""
        self.__comp = ""
        self.__jump = ""


    def parse(self,line,numOfLine):
        """
        parse the line, return true if succeded, false otherwise
            :param line: line to parse
            :param numOfLine: current command number
        """
        if "=" in line:
            self.__dest,line = line.split("=")
            if self.__dest not in Cins.__DEST2CODE:
                return False
        if ";" in line:
            line, self.__jump = line.split(";")
            if self.__jump not in Cins.__JMP2CODE:
                return False
        self.__comp = line

        return  self.__comp in Cins.__COMP2CODE

    def translate(self):
        """
        return translation of the line to string of bits 
        """
        dest = Cins.__DEST2CODE[self.__dest]
        jump = Cins.__JMP2CODE[self.__jump]
        comp = Cins.__COMP2CODE[self.__comp]
        if len(comp) == 10:
            return  comp + dest + jump

        return Cins.__C_CMD + comp + dest + jump

class Label(Command):
    """
    Label class, should be surrounded with (), numOfline will be symbol value  
    """

    def __init__(self, symbolsDict):
        """
        init Label, store the given symbolsDict
            :param symbolsDict: the symbolDict
        """
        Command.__init__(self, symbolsDict)
        self.__symbol = None

    def parse(self,line,numOfLine):
        """
        parse the line, return true if succeded, false otherwise
        label should be surrounded with ()
        numOfLine will be the symbol value
            :param line: line to parse
            :param numOfLine: current command number
        """
        if line.startswith("(") and line.endswith(")"):
            self._symbolsDict[line[1:-1]] = numOfLine
            return True
        return False

    def translate(self):
        """
        return translation of the line to string of bits 
        """
        return None

class SymbolDict(dict):
    """
    SymbolDict inherit from python dict,
    symbols can be added from outside the class,
    user symbols are added using addSymbol method and auto assignes value
    """
    __SYMBOLS = {"R0":0, "R1":1, "R2":2,"R3":3 , "R4":4, "R5":5, "R6":6,
                 "R7":7, "R8":8, "R9":9, "R10":10, "R11":11, "R12":12,
                 "R13":13, "R14":14, "R15":15, "SCREEN":16384, "KBD":24576,
                 "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4}

    __FIRST_USER_SYMBOL = 16

    def __init__(self):
        """
        init SymbolDict
        """
        dict.__init__(self, SymbolDict.__SYMBOLS)
        self.__counter = SymbolDict.__FIRST_USER_SYMBOL

    def addSymbol(self, symbol):
        """
        add user symbol to dict with the value of inner counter,
        and advance the counter
        """
        self[symbol] = self.__counter
        self.__counter += 1
