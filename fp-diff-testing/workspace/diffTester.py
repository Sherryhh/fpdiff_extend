import os
import pickle
import sys
import subprocess
import ctypes
import signal
import time
import struct
import csv
import itertools
import traceback
import pdb
from header import *

# set working directory
WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)


'''
takes in an equivalence class, gathers all test inputs to be used 
with that equivalence class, and creates/saves discrepancy objects
'''
def diffTester(classNo, totalClassCount, equivalenceClass, TEST_INPUTS, UNIQUE_DISCREPANCIES, ALL_DISCREPANCIES):

    print("Testing Class {}/{}".format(classNo, totalClassCount - 1))

    # grab all inputs tagged with "all_"
    inputNames = [x for x in TEST_INPUTS.keys() if "all_" in x]

    # add all inputs tagged with the name of a driver in the equivalence class
    for driver in equivalenceClass:
        inputNames.extend([x for x in TEST_INPUTS.keys() if driver.get_driverName() in x])

    # test each of those inputs
    for inputName in sorted(inputNames):

        inputTuple = TEST_INPUTS[inputName]
        outputDriverPairs = []

        # collect tuples of the form (driver, output)
        for driver in equivalenceClass:
            outputDriverPairs.append((driver, driver.run_driver(inputTuple[0], inputTuple[1])))

        # if the outputs are not consistent...
        if not isConsistent([f[1] for f in outputDriverPairs]):

            # create and save a discrepancy object
            x = Discrepancy(classNo, inputName, inputTuple, outputDriverPairs)
            
            if x.get_id() not in UNIQUE_DISCREPANCIES.keys():
                discrepancyNo = len(UNIQUE_DISCREPANCIES.keys())
                UNIQUE_DISCREPANCIES[x.get_id()] = x
                UNIQUE_DISCREPANCIES[x.get_id()].set_discrepancyNo(discrepancyNo)
            
            ALL_DISCREPANCIES.append(x)
        

def isConsistent(outputs):
    
    exceptionCount = 0

    # count up the number of exceptions
    for output in outputs:
        if isinstance(output, str):
            exceptionCount += 1

    # if all drivers threw exceptions, consider them consistent
    if exceptionCount == len(outputs):
        return True

    # if there weren't any exceptions...
    elif exceptionCount == 0:

        # if they're all nan, return True            
        if np.isnan(outputs).prod():
            return True

        # if they're all positive infinity, return True
        elif np.isposinf(outputs).prod():
            return True

        # if they're all negative infinity, return True
        elif np.isneginf(outputs).prod():
            return True

        # if they're all negative zero, return True
        elif np.array([x is np.NZERO for x in outputs]).prod():
            return True

        # otherwise, if they're all proper doubles...
        elif np.isfinite(outputs).prod():

            # check whether the double outputs are within the
            # specified epsilon neighborhood
            for pair in itertools.combinations(outputs, 2):

                # if they're both zero, move on
                if abs(pair[0]) + abs(pair[1]) == 0:
                    continue

                # otherwise, if the relative error is greater than
                # TOLERANCE, return false
                elif 2 * abs(pair[0] - pair[1]) / (abs(pair[0]) + abs(pair[1])) > TOLERANCE:
                    return False
                
                # otherwise, move on
                else:
                    continue

            # if we made it through the accuracy check, return True
            return True

        else:
            return False

    # otherwise, it's a mix of exceptions and other values, so return False
    else:
        return False


''' function to write out a csv file of the results '''
def writeOutCSVfile(DISCREPANCIES):

    with open("diffTestingResults.csv", 'w') as f:

        fieldnames = ['discrepancyNo', 'classNo', 'discrepancyCategory', 'inputName', 'inputList', 'libraryName', 'driverName', 'funcName', 'output', 'absErrs', 'relErrs']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for discrepancy in DISCREPANCIES.values():
            for pair in discrepancy.get_driverOutputPairs():
                    writer.writerow({'discrepancyNo' : discrepancy.get_discrepancyNo(),
                                'classNo': "{:0>3}".format(discrepancy.get_classNo()),
                                'discrepancyCategory': discrepancy.get_discrepancyCategory(),
                                'inputName': discrepancy.get_inputName(),
                                'inputList': discrepancy.get_inputList(),
                                'libraryName': pair[0].get_libraryName(),
                                'driverName': pair[0].get_driverName(),
                                'funcName': pair[0].get_funcName(),
                                'output': pair[1],
                                'absErrs' : discrepancy.get_absErrs(),
                                'relErrs' : discrepancy.get_relErrs()})

    sort_csv("diffTestingResults.csv")


def getStats(UNIQUE_DISCREPANCIES, ALL_DISCREPANCIES):

    total_discrepancyTally = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    specialValue_discrepancyTally = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    testMigration_discrepancyTally = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

    for discrepancy in ALL_DISCREPANCIES:
        if "_pos" in discrepancy.get_inputName():
            specialValue_discrepancyTally[discrepancy.get_discrepancyCategory()] += 1
        if "_num" in discrepancy.get_inputName():
            testMigration_discrepancyTally[discrepancy.get_discrepancyCategory()] += 1
            
    for discrepancy in UNIQUE_DISCREPANCIES.values():
        total_discrepancyTally[discrepancy.get_discrepancyCategory()] += 1

    with open("__statistics.txt", 'a') as f:
        f.write("\nspecialValue_discrepancyTally: {}\n".format(list(specialValue_discrepancyTally.values())))
        f.write("testMigration_discrepancyTally: {}\n".format(list(testMigration_discrepancyTally.values())))
        f.write("\nTIMEOUTS: {}\n".format(total_discrepancyTally[1]))
        f.write("DOUBLES FROM NAN: {}\n".format(total_discrepancyTally[2]))
        f.write("DOUBLES FROM INF: {}\n".format(total_discrepancyTally[3]))
        f.write("INACCURACIES: {}\n".format(total_discrepancyTally[4]))
        f.write("MIX OF DOUBLES, EXCEPTIONS, SPECIAL VALUES: {}\n".format(total_discrepancyTally[5]))
        f.write("MIX OF EXCEPTIONS AND SPECIAL VALUES: {}\n".format(total_discrepancyTally[6]))
        f.write("\n\t TOTAL # OF DISCREPANCIES: {}\n".format(sum(list(total_discrepancyTally.values()))))

def createIndividualPrograms(UNIQUE_DISCREPANCIES):
    
    CWD = WD + "/spFunDrivers/"

    for discrepancy in UNIQUE_DISCREPANCIES.values():
        
        # create a directory to hold the programs that reproduce the discrepancy
        subprocess.call(["rm", "-rf", "{:0>3}_discrepancy".format(discrepancy.get_discrepancyNo())], cwd=CWD)
        subprocess.call(["mkdir", "{:0>3}_discrepancy".format(discrepancy.get_discrepancyNo())], cwd=CWD)

        # set working directory
        tempCWD = CWD + "{:0>3}_discrepancy".format(discrepancy.get_discrepancyNo())
        
        # get inputList
        inputList = discrepancy.get_inputList()

        for driverOutputPair in discrepancy.get_driverOutputPairs():

            driver = driverOutputPair[0]
            expectedOut = driverOutputPair[1]

            # load imports
            with open(WD + "/__temp/__{}_imports".format(driver.get_libraryName()), 'rb') as f:
                imports = pickle.load(f)
            with open(WD + "/__temp/__{}_fromImports".format(driver.get_libraryName()), 'rb') as f:
                fromImports = pickle.load(f)
            
            if driver.get_lang() == "python":

                pythonInputs = []

                # convert special value inputs to numpy form
                for i in range(len(inputList)):
                    if str(inputList[i]) == "inf":
                        pythonInputs.append("np.inf")
                    elif str(inputList[i]) == "-inf":
                        pythonInputs.append("np.NINF")
                    elif str(inputList[i]) == "nan":
                        pythonInputs.append("np.nan")
                    elif str(inputList[i]) == "-0":
                        pythonInputs.append("np.NZERO")
                    else:
                        pythonInputs.append(str(inputList[i]))

                # write the program
                with open(tempCWD + "/{}.py".format(driver.get_driverName()), 'w') as f:
                    for x in imports:
                        if len(x) == 1:
                            f.write("import {}\n".format(x[0]))
                        elif len(x) == 2:
                            f.write("import {} as {}\n".format(x[0],x[1]))
                    for x in fromImports:
                        f.write("from {} import {}\n".format(x[0], x[1]))

                    f.write("import {}\n".format(driver.get_libraryName()))
                    f.write("import numpy as np\n\n")
                    f.write("print('{} version: {{}}'.format({}.__version__))\n".format(driver.get_libraryName(), driver.get_libraryName()))
                    f.write("print({}({}".format(driver.get_callName(),pythonInputs[0]))
                    for i in range(1,len(inputList)):
                        f.write(", {}".format(pythonInputs[i]))
                    f.write("))\n\n")

            
            if driver.get_lang() == "c":

                cInputs = []

                # convert special value inputs to numpy form
                for i in range(len(inputList)):
                    if str(inputList[i]) == "inf":
                        cInputs.append("GSL_POSINF")
                    elif str(inputList[i]) == "-inf":
                        cInputs.append("GSL_NEGINF")
                    elif str(inputList[i]) == "nan":
                        cInputs.append("GSL_NAN")
                    elif str(inputList[i]) == "-0":
                        cInputs.append("-0")
                    else:
                        cInputs.append(str(inputList[i]))

                # write the program
                with open(tempCWD + "/{}.c".format(driver.get_driverName()), 'w') as f:
                    
                    f.write("#include <gsl/gsl_sf.h>\n")
                    f.write("#include <gsl/gsl_errno.h>\n")
                    f.write("#include <stdio.h>\n\n")
                    f.write("#include <gsl/gsl_math.h>\n")

                    f.write("int main (void){\n")

                    f.write("\tdouble out;\n")
                    f.write("\tout = {}({}".format(driver.get_funcName(),cInputs[0]))
                    for i in range(1,len(inputList)):
                        f.write(", {}".format(cInputs[i]))
                    if driver.get_numberOfParameters() > len(cInputs):
                        f.write(", GSL_PREC_DOUBLE")
                    f.write(");\n\n")

                    f.write('\tprintf("%f\\n", out);')
                    f.write('}')

                subprocess.call(["cp", "spFunDrivers/Makefile", tempCWD])
                subprocess.call(["make", "{}".format(driver.get_driverName())], cwd=tempCWD)
                    

if __name__ == "__main__":

    try:
        # try:
        #     with open("__temp/__uniqueDiscrepancies", 'wb') as fp:
        #         UNIQUE_DISCREPANCIES = pickle.load(UNIQUE_DISCREPANCIES)
        
        # except:
        UNIQUE_DISCREPANCIES = {}
        ALL_DISCREPANCIES = []

        with open("__temp/__equivalenceClasses", 'rb') as fp:
            CLASSES = pickle.load(fp)

        with open("__temp/__testInputs", "rb") as fp:
            TEST_INPUTS = pickle.load(fp)

        for classNo, classKey in enumerate(sorted(list(CLASSES.keys()))):
            diffTester(classNo, len(list(CLASSES.keys())), CLASSES[classKey], TEST_INPUTS, UNIQUE_DISCREPANCIES, ALL_DISCREPANCIES)

        writeOutCSVfile(UNIQUE_DISCREPANCIES)
        getStats(UNIQUE_DISCREPANCIES, ALL_DISCREPANCIES)

        # with open("__temp/__uniqueDiscrepancies", 'wb') as fp:
        #     pickle.dump(UNIQUE_DISCREPANCIES, fp)

        createIndividualPrograms(UNIQUE_DISCREPANCIES)

    except:
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)