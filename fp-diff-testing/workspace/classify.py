import ctypes
import os
import sys
import subprocess
import random
import pickle
import numpy as np
from header import *
import csv
import itertools
import math
from pprint import pprint
from difflib import SequenceMatcher
import pdb
import traceback

SIZE_OF_INPUTS = 8
NUMBER_OF_DIFFERENT_INTEGER_INPUTS = 3
NUMBER_OF_DIFFERENT_DOUBLE_INPUTS = 10
TOLERANCE = 0.00001


def generateElementaryInputs():
    ELEMENTARY_INPUTS = {}

    inputNo = 0

    for i in range(NUMBER_OF_DIFFERENT_DOUBLE_INPUTS):
        random.seed(i)

        doubles=[random.uniform(0,3) for j in range(SIZE_OF_INPUTS)]

        # if i%4 == 0:
        #     doubles=[random.uniform(1,2) for j in range(SIZE_OF_INPUTS)]
        # elif i%4 == 1:
        #     doubles=[random.uniform(-2,2) for j in range(SIZE_OF_INPUTS)]
        # elif i%4 == 2:
        #     doubles=[random.uniform(2,10) for j in range(SIZE_OF_INPUTS)]
        # else:
        #     doubles=[random.uniform(-2,-1) for j in range(SIZE_OF_INPUTS)]

        for k in range(NUMBER_OF_DIFFERENT_INTEGER_INPUTS):  
            ints = [(x+k)%NUMBER_OF_DIFFERENT_INTEGER_INPUTS for x in range(SIZE_OF_INPUTS)]

            ELEMENTARY_INPUTS["elementaryInput_num{:0>3}".format(inputNo)] = (doubles, ints)
            inputNo += 1

    with open("__temp/__elementaryInputs", 'wb') as f:
        pickle.dump(ELEMENTARY_INPUTS, f)

    return ELEMENTARY_INPUTS


def classify(CLASSES, DRIVER_LIST, ELEMENTARY_INPUTS):

    # for each elementary input
    for elementaryInput in ELEMENTARY_INPUTS.values():
        
        # for each driver in the DRIVER_LIST, run on the elementary input and accumulate result
        for driver in DRIVER_LIST.values():

            result = driver.run_driver(elementaryInput[0], elementaryInput[1])

            if isinstance(result, str):
                driver.add_exceptionMessage(result)
                driver.add_classificationOutput(0)
            elif np.isfinite(result):    
                driver.add_classificationOutput(result)
            else:
                driver.add_classificationOutput(0)

    validDriverLists = {}

    # classify each driver based on the accumulated result (also tally how many valid drivers we got)            
    for driver in DRIVER_LIST.values():

        # if the driver didn't throw an exception on every attempt to
        # evaluate it over elementary inputs...
        if len(driver.get_exceptionMessages()) != len(ELEMENTARY_INPUTS.values()):
            
            # accumulate lists of unique functions per library
            if driver.get_libraryName() not in validDriverLists.keys():
                validDriverLists[driver.get_libraryName()] = []
            if driver.get_funcName() not in validDriverLists[driver.get_libraryName()]:
                validDriverLists[driver.get_libraryName()].append(driver.get_funcName())

            # insert first class
            if len(CLASSES) == 0:
                CLASSES[driver.get_id()] = [driver]

            # otherwise compare against all outputs to find its equivalence class
            else:
                match = False
                
                # go through the existing classKeys
                for classKey, equivalenceClass in CLASSES.items():

                    # if the current tuple is close enough to the class key, add it to the equivalence class
                    if isSameNumber(driver.get_id(), classKey) and equivalenceClass[0].get_numberOfArgs() == driver.get_numberOfArgs():
                        if all(x == True for x in list(map(isSameNumber, driver.get_classificationOutputs(), equivalenceClass[0].get_classificationOutputs()))):
                            match = True
                            
                            # conditional added to remove duplicate functions
                            if driver.get_libraryName() + driver.get_funcName() not in [f.get_libraryName() + f.get_funcName() for f in equivalenceClass]:
                                CLASSES[classKey].append(driver)
                            
                            break

                # otherwise, add a new equivalence class        
                if not match:
                    CLASSES[driver.get_id()] = [driver]

    total = 0
    with open("ori/__statistics.txt", 'a') as f:
        for libraryName in validDriverLists.keys():
            temp = "Generated {} executable drivers of unique functions from {}\n".format(len(validDriverLists[libraryName]), libraryName)
            total += len(validDriverLists[libraryName])
            f.write(temp)
        f.write("\n\tTOTAL DRIVER COUNT: {}\n".format(total))

    ''' code to write out the executable driver lists ''' 
    with open("ori/__executableDrivers.txt", 'w') as f:
        for libraryName in validDriverLists.keys():
            for funcName in sorted(validDriverLists[libraryName]):
                f.write("{} : {}\n".format(libraryName, funcName))


def isSameNumber(x,y):
    if np.isfinite(np.array([x,y])).prod():
        return 2 * (abs(x - y))/max((abs(x) + abs(y) ), TOLERANCE) < TOLERANCE
    else:
        return False

def isSameOutput(x,y):

    # if they are different types, return false
    if type(x) != type(y):
        return False

    # if they are both exceptions, consider them the same
    elif type(x) == type("hello"):
        return True

    # if they are all finite, call isSameNumber
    elif np.isfinite(np.array([x,y])).prod():
        return isSameNumber(x,y)

    # if they are all non-finite, return True
    elif np.isfinite(np.array([x,y])).sum() == 0:
        return True

    return False

def findClassesWithDuplicates(CLASSES):

    classesWithDuplicates = []

    # in each equivalence class...
    for classKey, equivalenceClass in CLASSES.items():
        perLib = {}

        # for each driver in that equivalence class...
        for driver in equivalenceClass:

            # if we haven't already counted that libraries drivers, do
            # so and store the count
            if driver.get_libraryName() not in perLib.keys():
                perLib[driver.get_libraryName()] = len([x for x in equivalenceClass if x.get_libraryName() == driver.get_libraryName()])
                
            if any(f > 1 for f in perLib.values()) and classKey not in classesWithDuplicates:
                classesWithDuplicates.append(classKey)

    return classesWithDuplicates

def manualRemoveDuplicates(CLASSES):

    keys = findClassesWithDuplicates(CLASSES)

    for key in keys:

        deleteList = []

        for i, driver in enumerate(CLASSES[key]):
            print("{}) Library: {}, Function Name: {}".format(i,driver.get_libraryName(), driver.get_funcName()))

        userInput = 0

        while True:
            userInput = input("Enter # of function to remove from equivalence class (or 'stop' to end): ")

            try:
                userInput = int(userInput)
            except:
                break

            deleteList.append(CLASSES[key][userInput])

        for x in deleteList:
            CLASSES[key].remove(x)


def autoStressTestDuplicates(CLASSES):

    keys = findClassesWithDuplicates(CLASSES)

    while keys:
        # for each equivalence class with duplicates
        for classKey in keys:

            # gather all drivers from the same library together into perLib
            perLib = {}
            for driver in CLASSES[classKey]:
                if driver.get_libraryName() not in perLib.keys():
                    perLib[driver.get_libraryName()] = [x for x in CLASSES[classKey] if x.get_libraryName() == driver.get_libraryName()]

            divergingInputs = []

            # for each perLibrary list of length greater than 1, we
            # attempt to find all inputs that cause the apparently
            # identical functions to diverge
            for lib,perLibList in perLib.items():
                if len(perLibList) > 1:
                    #print("{} from {} are purportedly equivalent".format([x.get_driverName() for x in perLibList], lib ))

                    # gather all migrated test inputs
                    with open("__temp/__testInputs", 'rb') as f:
                        TEST_INPUTS = pickle.load(f)

                    for driver in perLibList:
                        stressTestInputs = [TEST_INPUTS[f] for f in TEST_INPUTS.keys() if driver.get_driverName() in f]
                        
                    # generate a fixed number of other inputs that span
                    # ever-increasing ranges of positive and negative doubles
                    for i in range(10):
                        random.seed(7)
                        doubles = [random.uniform(-(i+1), i+1) for x in range(SIZE_OF_INPUTS)]

                        # if i%2 == 0:
                        #     doubles = [random.uniform(-(i+1), i+1) for x in range(SIZE_OF_INPUTS)]
                        # else:
                        #     doubles = [abs(random.uniform(-(i+1), i+1)) for x in range(SIZE_OF_INPUTS)]
                        ints = [int(math.floor(random.uniform(0,NUMBER_OF_DIFFERENT_DOUBLE_INPUTS)))%NUMBER_OF_DIFFERENT_INTEGER_INPUTS + 1 for x in range(SIZE_OF_INPUTS)]

                        stressTestInputs.append((doubles,ints))

                    #print("found stressTest inputs {}".format(stressTestInputs))
                
                    # for each of those inputs, see if it makes
                    # the functions diverge and save if so
                    for inputTuple in stressTestInputs:
                        outputs = []
                        for driver in perLibList:
                            outputs.append(driver.run_driver(inputTuple[0], inputTuple[1]))
                            
                        for pair in itertools.combinations(outputs, 2):
                            
                            if not isSameOutput(pair[0],pair[1]) and inputTuple not in divergingInputs:
                                divergingInputs.append(inputTuple)

                    # if we couldn't find any diverging inputs, we
                    # conclude that the two functions from the library are
                    # in fact the same so we just take the one with the
                    # most similar name to the others
                    if not divergingInputs:
                        mostSimilarName = None
                        maximumSimilarityRatio = 0
                        for driver in perLibList:
                            temp = sum([SequenceMatcher(None, driver.get_funcName(), x.get_funcName()).ratio() for x in CLASSES[classKey] if x not in perLibList])
                            if temp > maximumSimilarityRatio:
                                mostSimilarName = driver
                                maximum = temp

                        if not mostSimilarName:
                            mostSimilarName = perLibList[0]

                        CLASSES[classKey] = [f for f in CLASSES[classKey] if f.get_libraryName() != mostSimilarName.get_libraryName()]
                        CLASSES[classKey].append(mostSimilarName)

            # if we found divergingInputs...
            if divergingInputs:
                #print("found diverging inputs {}".format(divergingInputs))

                newClasses = {}

                # for each driver
                for driver in CLASSES[classKey]:
                    output = 0
                    
                    # run each divergingInput and accumulate the result
                    for inputTuple in divergingInputs:
                        
                        temp = driver.run_driver(inputTuple[0], inputTuple[1])
                        
                        if isinstance(temp, float) and np.isfinite(temp):
                            output += temp

                    # reclassify
                    if output != 0:
                        if newClasses == {}:
                            newClasses[output] = [driver]
                        else:
                            match = False
                            for newClassKey in newClasses.keys():
                                if isSameNumber(newClassKey, output):
                                    match = True
                                    newClasses[newClassKey].append(driver)
                                    break
                            
                            if not match:
                                newClasses[output] = [driver]

                del CLASSES[classKey]

                CLASSES.update(newClasses)

        keys = findClassesWithDuplicates(CLASSES)
            
def pruneClasses(CLASSES):

    deleteList = []

    # figure out which classes have only one library and delete them
    for classKey, equivalenceClass in CLASSES.items():

        librariesPresent = []

        for driver in equivalenceClass:
            if driver.get_libraryName() not in librariesPresent:
                librariesPresent.append(driver.get_libraryName())
        
        if len(librariesPresent) < 2:
            deleteList.append(classKey)

    for x in deleteList:
        del CLASSES[x]

    # dict to keep track of what funcmappings have been found across
    # all classes and which classes to keep (if there is an overlap in
    # mappings between classes, we keep the largest and throw out all others)
    mappingsDict = {}

    for classKey, equivalenceClass in CLASSES.items():

        # for each pair in the class...
        for pair in itertools.combinations(equivalenceClass,2):

            # create a unique id for the mapping made up of the library names and funcNames
            x = sorted((pair[0].get_libraryName() + pair[0].get_funcName(),pair[1].get_libraryName() + pair[1].get_funcName()))
            x = x[0] + x[1]

            # if we haven't found that specific mapping, save the id
            # to funcMappings and save the classKey to remember which
            # class has that mapping
            if x not in mappingsDict.keys():
                mappingsDict[x] = classKey

            # otherwise, check which equivalence class is larger and
            # save the larger one
            else:
                if len(equivalenceClass) > len(CLASSES[mappingsDict[x]]):
                    mappingsDict[x] = classKey
    
    # go through the mappingsDict and grab all of the classKeys we want
    reallySaveThese = []
    for classKey in mappingsDict.values():
        if classKey not in reallySaveThese:
            reallySaveThese.append(classKey)

    deleteList = [f for f in CLASSES.keys() if f not in reallySaveThese]

    for x in deleteList:
        del CLASSES[x]

def tallyMappings(CLASSES):
    
    mappings = {}
    functionsWithMappings = {}

    for equivalenceClass in CLASSES.values():
            # count up number of mappings
            for pair in itertools.combinations(equivalenceClass, 2):
                libraries = sorted([pair[0].get_libraryName(), pair[1].get_libraryName()])
                functionNames = sorted([pair[0].get_funcName(), pair[1].get_funcName()])
                functionNames = functionNames[0] + '/' + functionNames[1]

                if libraries[0] == libraries[1]:
                    print("Found a mapping between the {} functions {}".format(libraries[0], functionNames))

                libraries = libraries[0] + '/' + libraries[1]
                if libraries not in mappings.keys():
                    mappings[libraries] = [functionNames]
                elif functionNames not in mappings[libraries]:
                        mappings[libraries].append(functionNames)
            
            # count up the number of functions with mappings
            for driver in equivalenceClass:
                if driver.get_libraryName() not in functionsWithMappings.keys():
                    functionsWithMappings[driver.get_libraryName()] = [driver.get_funcName()]
                elif driver.get_funcName() not in functionsWithMappings[driver.get_libraryName()]:
                    functionsWithMappings[driver.get_libraryName()].append(driver.get_funcName())

    with open("functions/gsl_sf_lnsinh/__statistics.txt", 'a') as f:
        interLibraryTotal = 0
        intraLibraryTotal = 0
        f.write("\n")
        for libraries, functionNames in mappings.items():
            tally = len(functionNames)
            f.write("Found {} {} mappings\n".format(tally, libraries))

            if libraries.split(sep='/')[0] == libraries.split(sep='/')[1]:
                intraLibraryTotal += tally
            else:
                interLibraryTotal += tally
        f.write("\n\t INTRA-LIBRARY MAPPING COUNT: {}\n".format(intraLibraryTotal))
        f.write("\t INTER-LIBRARY MAPPING COUNT: {}\n\n".format(interLibraryTotal))

        total = 0
        for library, listOfFuncs in functionsWithMappings.items():
            f.write("{} functions from {} were assigned mappings\n".format(len(listOfFuncs), library))
            total += len(listOfFuncs)

        f.write("\n\t TOTAL # OF FUNCS WITH MAPPINGS: {}\n\n".format(total))


def prettyPrintClasses(CLASSES):
    print("==================================================")

    for counter, classKey in enumerate(CLASSES.keys()):
        print("Class {}:\n".format(counter))
        for driver in CLASSES[classKey]:
            print("{:<35} => {}".format(driver.get_driverName(), driver.get_id()))
        print()
        print("==================================================")


if __name__ == "__main__":
    try:
        with open("__temp/__driverCollection", 'rb') as fp:
            DRIVER_LIST = pickle.load(fp)

        try:
            with open("__temp/__elementaryInputs", 'rb') as f:
                ELEMENTARY_INPUTS = pickle.load(f)
        except:
            ELEMENTARY_INPUTS = generateElementaryInputs()

        CLASSES = {}

        classify(CLASSES, DRIVER_LIST, ELEMENTARY_INPUTS)
        pruneClasses(CLASSES)
        manualRemoveDuplicates(CLASSES)
        pruneClasses(CLASSES)
        tallyMappings(CLASSES)
        
        temp = {}
        for classKey in sorted(CLASSES.keys()):
            temp[classKey] = CLASSES[classKey]

        CLASSES = temp

        prettyPrintClasses(CLASSES)

        with open("__temp/__equivalenceClasses", 'wb') as fp:
            for equivalenceClass in CLASSES.values():
                for driver in equivalenceClass:
                    driver.reset_callableDriver()
            pickle.dump(CLASSES, fp)

        with open("functions/gsl_sf_lnsinh/equivalenceClasses.csv", 'w') as fp:

            fieldnames = ['classNo', 'driverName', 'funcName']
            writer = csv.DictWriter(fp, fieldnames=fieldnames)

            writer.writeheader()
            
            for classNo, equivalenceClass in enumerate(CLASSES.values()):
                for driver in equivalenceClass:
                    writer.writerow({'classNo':classNo,
                                        'driverName':driver.get_driverName(),
                                        'funcName':driver.get_funcName()})

    except:
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)