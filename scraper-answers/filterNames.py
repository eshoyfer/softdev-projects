# -*- coding: utf-8 -*-
import time
import re
from collections import Counter
nameList = []
namesListFile = "allNamesUppercase.txt"

LOWER_CASE_ALPHABET_RANGE = "[a-záààâçééèèêëíìîïñóòôúùùûü]"
UPPER_CASE_ALPHABET_RANGE = "[A-ZÛÚÙÙÜÁÀÀÂÇÉÉÈÈÊËÍÌÎÏÑÓÒÔ]"

def getFilteredInputList(s):
    global wordList
    results = Counter()
    # regex matches names such as:
    # Les Demoiselles d'Avignon, Mademoiselle de l'Amour, Abd el-Fattah, Jean-Jacques Rousseau, and James Bond
    regex_capitals_with_surname_epithet = "([A-Z][a-z]+[A-Z]?[a-z]+((( |-)[A-Z][a-z]+[A-Z]?[a-z]+){0,3})?((( ([a-z]{2,3}(?=\s|-))){1,2})?(( |-)([a-z]\')?[A-Z][a-z]+){1,3}}})?)"
    # expand alphabet with accent mark variations
    regex_capitals_with_surname_epithet = regex_capitals_with_surname_epithet\
        .replace('[A-Z]', UPPER_CASE_ALPHABET_RANGE)\
        .replace('[a-z]', LOWER_CASE_ALPHABET_RANGE)
    regex = re.compile(regex_capitals_with_surname_epithet)
    # find all matches, returns a tuple whose first element is the full match
    words = regex.findall(s)
    for _tuple in words:
        if len(_tuple) > 0:
            match = _tuple[0]
            # replace newlines with spaces
            match = match.replace('\r', ' ')\
                    .replace('\n', ' ')
            # strip extra whitespace
            match = match.strip()
            # check if match has multiple words 
            if match.find(' ') < 0:
                if (inNameList(match)):
                    #print "Matched: " + match
                    results[match] += 1
            else:
                # if match has multiple words, check each word against the name list
                each_part_is_valid_name = True
                valid_parts = []
                for part in match.split(" "):
                    if (not inNameList(part)):
                        each_part_is_valid_name = False
                    else:
                        if len(part) > 0 and part[0].isupper():
                            valid_parts.append(part)
                # if all words are valid, then add the entire match to results
                if each_part_is_valid_name:
                    #print "Matched multiword: " + match
                    results[match] += 1 + len(match.split(" ")) 
                # if not all words are valid, only add the valid ones to results
                else:
                    for valid_part in valid_parts:
                        #print "Matched substring: " + valid_part;
                        results[valid_part] += 1
    return results

def getNameList():
    #    startTime = time.time() * 1000
    global namesListFile, nameList
    if nameList == []:
        f = open(namesListFile, 'r')
        for line in f.readlines():
            nameList.append(line.strip())
        f.close()
    #    print "Read all names (" + str(len(nameList)) + ") in " + str(time.time() * 1000 - startTime) + " ms"
    #    startTime = time.time() * 1000
        # Name list should be pre-sorted, but this is run just in case
        # If it is pre-sorted, the runtime of this sort will be negligible 
        nameList.sort()
    #    print "Sorted all names in " + str(time.time() * 1000 - startTime) + " ms" 

def inNameList(word):
    global nameList
    word = word.upper()
    low = 0
    high = len(nameList) - 1
    # Use a binary search to find the word in the name list
    while (low <= high):
        middle = (low + high) / 2
        if (word > nameList[middle]):
            low = middle + 1;
        elif (word < nameList[middle]):
            high = middle - 1;
        else:
            return True
    return False

getNameList()

