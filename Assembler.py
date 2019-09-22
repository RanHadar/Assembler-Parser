"""
@file Assembler.py
holds the program main
translate *.asm file to *.hack file
"""

import sys
from Commands import *

SOURCE_TYPE = ".asm"
DEST_TYPE = ".hack"

NUM_OF_ARG = 1

ERROR_ARGS_NUM = -1
ERROR_FILE_TYPE = -2
ERROR_FILE_SYNTAX = -3
SUCCESS = 0

def parse(filename, symbolDict):
    """
    parse the commands in the given input file
    returns list of commands,
    on failure returns empty list
        :param filename: input file path
    """
    lineNum = 0
    commands = []
    file = open(filename, "r")
    for line in file.readlines():
        # remove comments and spaces from line
        line = "".join(line.split("//")[0].split())
        if not line:
            continue

        cmdA = Ains(symbolDict)
        cmdC = Cins(symbolDict)
        label = Label(symbolDict)

        if cmdA.parse(line, lineNum):
            lineNum += 1
            commands.append(cmdA)
        elif cmdC.parse(line, lineNum):
            lineNum += 1
            commands.append(cmdC)
        elif not label.parse(line, lineNum):
            file.close()
            return []

    file.close()
    return commands

def translate(commands, fileName):
    """
    translate this list of command to binary commands,
    outputs the translation to the new file at given file path
        :param commands: list of parsed commands
        :param filename: output file path
    """
    file = open(fileName, "w")
    for cmd in commands:
        file.write(cmd.translate() + "\n")

    file.close()

def main(filename):
    """
     parse the given filename and trnslate into new file
        :param filename: file path
    """

    if not filename.endswith(SOURCE_TYPE):
        print("invalid file type, should be *" + SOURCE_TYPE)
        return ERROR_FILE_TYPE

    commands = parse(filename, SymbolDict())

    if not commands:
        print("invalid asm syntax")
        return ERROR_FILE_SYNTAX

    translate(commands, filename[:-len(SOURCE_TYPE)] + DEST_TYPE)

    return SUCCESS

if __name__ == "__main__":
    if len(sys.argv) != NUM_OF_ARG + 1:
        print("invalid arguments number")
        print("Usage: Assembler [file" + SOURCE_TYPE+"]")
        exit(ERROR_ARGS_NUM)

    exit(main(sys.argv[NUM_OF_ARG]))