import argparse
from datetime import datetime
import time
import os
import sys
 
class WordGenerator():
    # possible dictionaries in ascii codes
    dict_digits = range(48,58)
    dict_ucase = range(65,91)
    dict_lcase = range(97,123)
    dict_nonalpha = [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126]
    fWordList = 'wordgen.txt'
    fPath = ''
    def __init__(self):
        # set some initial settings
        self.Dictionary = range(10)
        self.StartWord = [0]
        self.EndWord = [9]
        self.Finished = False
    def __del__(self):
        pass
    def SetDict(self,Digits,UpperCase,LowerCase,NonAlpha):
        # set needed dictionaries
        self.Dictionary = []
        self.fWordList = 'wl'
        # add dictionary for all digits
        if Digits:
            self.Dictionary += self.dict_digits
            self.fWordList += '_num'
        # add dictionary for all upper case characters
        if UpperCase:
            self.Dictionary += self.dict_ucase
            self.fWordList += '_ucase'
        # add dictionary for all lower case characters
        if LowerCase:
            self.Dictionary += self.dict_lcase
            self.fWordList += '_lcase'
        # add dictionary for all special signs (non alphanumerics like !?+#().....)
        if NonAlpha:
            self.Dictionary += self.dict_nonalpha
            self.fWordList += '_nonalpha'
        self.Dictionary.sort()
    def SetPath(self,Path):
        # set the file path for the wordlist output
        self.fPath = Path
    def Start(self,Length):
        # initialize generating wordlist with given paramters (start, end, outputfile, length)
        self.StartWord = [self.Dictionary[0]]*Length
        self.EndWord = [self.Dictionary[len(self.Dictionary)-1]]*Length
        sFileName = os.path.join(self.fPath, self.fWordList) + '_' + str(Length) +'.txt'
        self.oFile = open(sFileName, 'w')
        bFinished = self.Generate(self.StartWord, 0)
        self.oFile.close()
    def Generate(self, GenWord, Dimension):
        # this method generates all possible words in the predefined range of dictionaries and length
        result = False
        ilower = self.Dictionary.index(GenWord[Dimension])
        iupper = self.Dictionary.index(self.EndWord[Dimension]) + 1
        NewWord = GenWord[:]
        for Number in self.Dictionary[ilower:iupper]:
            NewWord[Dimension] = Number
            if Dimension < (len(NewWord) - 1):
                if self.Generate(NewWord, Dimension + 1):
                    result = True
                    break
            else:
                # a generated word is here !!!
                # transform ascii to characters and store it in the wordlist file
                StrWord = ''
                for ASCII in NewWord:
                    StrWord += chr(ASCII)
                self.oFile.write(StrWord + '\n')
                # if the last word is reached, leave the for-loop
                if NewWord == self.EndWord:
                    result = True
                    self.Finished = True
                    break
        return result
 
# set up the argumentparser
parser = argparse.ArgumentParser(description='Generate a list of Words')
parser.add_argument('--length', dest='length', type=int, help='length of words')
parser.add_argument('--digits', dest='digits', action='store_true', help='activate using digits')
parser.add_argument('--ucase', dest='ucase', action='store_true', help='activate using uppercase')
parser.add_argument('--lcase', dest='lcase', action='store_true', help='activate using lowercase')
parser.add_argument('--nonalpha', dest='nonalpha', action='store_true', help='activate using nonalpha')
parser.add_argument('--path', dest='path', help='destination path for wordlist')
args = parser.parse_args()
 
# check for the length argument
if args.length==None:
    print('ERROR: missing required option\nlength of words is needed')
    exit()
 
# check if at least one dictionary is set
if args.digits==False and args.ucase==False and args.lcase==False and args.nonalpha==False:
    print('ERROR: missing required options\nuse at least one of these options: -d, -l, -u, -n\nuse -h or --help for more information')
    exit()
 
# check if the path exists if it is set
if args.path!=None:
    if os.path.exists(args.path)==False:
        print('ERROR: path does not exist')
        exit()
 
# Initial Data
wgen = WordGenerator()
wgen.SetDict(args.digits, args.ucase, args.lcase, args.nonalpha)
if args.path!=None:
    wgen.SetPath(args.path)
 
# Start Counting Time
print('start generating ...')
calcstart = datetime.now()
 
# Start Generating
wgen.Start(args.length)
 
# Finish Time Counting
calcend = datetime.now()
calcdif = calcend - calcstart
print('finished after:', calcdif)
