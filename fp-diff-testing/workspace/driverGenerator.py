import pickle
import os
import sys
import ast
from header import Driver
import struct
import subprocess
import re
from pprint import pprint
import pandas as pd
from collections import defaultdict

# set working directory
WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)
d_p = "../../AutoRNP/experiments/testing_results/DEMC/"

def convert(filename):
    xsl_file = pd.read_excel(d_p+filename, usecols="C")
    l_val = xsl_file['input'].tolist()
    uni_val = set()
    for val in l_val:
        uni_val.add(round(val, 1))
    return list(uni_val)

def autoRNP():
    directory = os.fsencode(d_p)
    all_functions = defaultdict()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xls"): 
            all_functions[filename[:-4]+'_DRIVER'] = convert(filename)
        else:
            continue
    return all_functions

            
def gslGenerator(libraryName, DRIVER_LIST, signatures, imports, fromImports, TEST_INPUTS):
    all_functions = autoRNP()

    with open("spFunDrivers/" + libraryName + "_drivers.c", 'w') as f:
        
        f.write("#include <gsl/gsl_sf.h>\n")
        f.write("#include <gsl/gsl_errno.h>\n")
        f.write("#include <stdio.h>\n\n")
        f.write("void my_handler(const char * reason, const char * file, int line, int gsl_errno)\n")
        f.write("{\n")
        f.write("\tfprintf(stderr, \"%s\\n\", reason);\n")
        f.write("}\n\n")

        for funcName, args in signatures.items():

            driverName = "{}_DRIVER".format(funcName)
            thisDriver = Driver(driverName, funcName, libraryName, "c", len(args[0]), funcName)

            thisDriver.add_line("double {}(double * doubleInput, int * intInput)\n".format(driverName))
            thisDriver.add_line("{\n")
            thisDriver.add_line("\tdouble out;\n")

            # tally up number of ints and doubles
            numberOfInts = 0
            numberOfDoubles = 0
            for i in range(len(args[0])):
                if "int" in args[0][i]:
                    numberOfInts += 1
                elif "double" in args[0][i]:
                    numberOfDoubles += 1

            thisDriver.set_numberOfDoubles(numberOfDoubles)
            thisDriver.set_numberOfInts(numberOfInts)

            # for each extracted function, save all of its test arguments for test migration
            k = 1
            for j in range(1, len(args)):

                ints = []
                doubles = []

                for i in range(len(args[0])):
                    if "int" in args[0][i]:
                        ints.append(int(args[j][i]))
                    elif "double" in args[0][i]:
                        doubles.append(float(args[j][i]))

                TEST_INPUTS["{}~input_num{:0>3}".format(driverName, j-1)] = (doubles, ints)
                k += 1
            if driverName in all_functions.keys():
                for m in range(k, len(all_functions[driverName])):
                    TEST_INPUTS["{}~input_num{:0>3}".format(driverName, m-1)] = ([all_functions[driverName][m-k]], [])

            thisDriver.add_line("\tgsl_error_handler_t * old_handler = gsl_set_error_handler (&my_handler);\n\n")

            thisDriver.add_line("\tout = {}(".format(funcName))

            for i in range(numberOfInts):
                thisDriver.add_line('intInput[{}]'.format(i))
                if i + 1 != numberOfInts or numberOfDoubles != 0:
                    thisDriver.add_line(", ")

            for i in range(numberOfDoubles):
                thisDriver.add_line('doubleInput[{}]'.format(i))
                if i + 1 != numberOfDoubles:
                    thisDriver.add_line(", ")
            
            if numberOfDoubles + numberOfInts < len(args[0]):
                thisDriver.add_line(", GSL_PREC_DOUBLE")

            thisDriver.add_line(');\n\n')

            #thisDriver.add_line("\tgsl_set_error_handler (old_handler);\n\n")

            thisDriver.add_line("\treturn out;\n")
            thisDriver.add_line("}} //END_DRIVER {}\n\n".format(funcName))

            f.write(thisDriver.get_driverText())
            DRIVER_LIST[thisDriver.get_driverName()] = thisDriver


def pythonGenerator(libraryName, DRIVER_LIST, signatures, imports, fromImports, TEST_INPUTS):

    with open("spFunDrivers/" + libraryName + "_drivers.py", 'w') as f:

        # write all imports
        for x in imports:
            if len(x) == 1:
                f.write("import {}\n".format(x[0]))
            if len(x) == 2:
                f.write("import {} as {}\n".format(x[0], x[1]))
        for x in fromImports:
            f.write("from {} import {}\n".format(x[0], x[1]))

        # for each collected function signature
        for funcName, args in signatures.items():

            # for a varying number of integers...
            for numberOfInts in range(len(args[0])):

                # get the number of doubles
                numberOfDoubles = len(args[0]) - numberOfInts
                
                # form driverName
                driverName = "{}_{}_DRIVER{}".format(libraryName, funcName.replace('.', '_'), numberOfInts )

                # form unique funcName without "_alt" and namespace info
                temp = funcName
                callName = funcName
                if '_alt' in temp:
                    temp = temp[:temp.index("_alt")]
                    callName = temp
                if '.' in temp:
                    temp = temp[temp.index(".") + 1:]

                # construct driver object
                thisDriver = Driver(driverName, temp, libraryName, "python", len(args[0]), callName)

                thisDriver.add_line("def {}(doubleInput, intInput):\n".format(driverName))

               # for each extracted function, save all of its test arguments for test migration
                for j in range(len(args)):

                    ints = []
                    doubles = []

                    for k in range(numberOfInts):
                        ints.append(int(args[j][k]))
                    for k in range(len(args[0]) - numberOfInts):
                        doubles.append(float(args[j][k]))

                    TEST_INPUTS["{}~inputs_num{:0>3}".format(driverName,j)] = (doubles, ints)

                thisDriver.set_numberOfDoubles(numberOfDoubles)
                thisDriver.set_numberOfInts(numberOfInts)

                if "_alt" in funcName:
                    thisDriver.add_line("\tout = {}(".format(funcName[:funcName.find("_alt")]))
                else:
                    thisDriver.add_line("\tout = {}(".format(funcName))

                for i in range(numberOfInts):
                    thisDriver.add_line("intInput[{}]".format(i))
                    if i + 1 != numberOfInts or numberOfDoubles != 0:
                        thisDriver.add_line(", ")

                for i in range(numberOfDoubles):
                    thisDriver.add_line("doubleInput[{}]".format(i))
                    if i + 1 != numberOfDoubles:
                        thisDriver.add_line(", ")

                thisDriver.add_line(")\n\n")

                thisDriver.add_line("\treturn float(out) #END_DRIVER {}\n\n".format(funcName))

                f.write(thisDriver.get_driverText())
                DRIVER_LIST[thisDriver.get_driverName()] = thisDriver

if __name__ == "__main__":
    # python3 driverGenerator mpmath python

    libraryName = sys.argv[1]
    language = sys.argv[2]

    try:
        with open("__temp/__driverCollection", 'rb') as fp:
            DRIVER_LIST = pickle.load(fp)
    except:
        DRIVER_LIST = {}

    try:
        with open("__temp/__testInputs", 'rb') as fp:
            TEST_INPUTS = pickle.load(fp)
    except:
        TEST_INPUTS = {}

    # load information from signature extractor
    with open("__temp/__" + libraryName + "_signatures", 'rb') as fp:
        signatures = pickle.load(fp)
    with open("__temp/__" + libraryName + "_imports", 'rb') as fp:
        imports = pickle.load(fp)
    with open("__temp/__" + libraryName + "_fromImports", 'rb') as fp:
        fromImports = pickle.load(fp)

    if language == 'c':
        gslGenerator(libraryName, DRIVER_LIST, signatures, imports, fromImports, TEST_INPUTS)
        subprocess.call(['make'], cwd="spFunDrivers/")

    if language == 'python':
        pythonGenerator(libraryName, DRIVER_LIST, signatures, imports, fromImports,TEST_INPUTS)

    with open("__temp/__testInputs", 'wb') as fp:
        pickle.dump(TEST_INPUTS, fp)

    with open("__temp/__driverCollection", 'wb') as fp:
        pickle.dump(DRIVER_LIST, fp)