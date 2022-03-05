import pickle
import os
import sys
import ast
import subprocess
import re
from pprint import pprint

# set working directory
WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

signatures = {}
imports = []
fromImports = []

def signature_extractor_c(inFile, libraryName):
    with open(inFile, "r") as source:
        code = source.readlines()

    for line in code:
        line = line.strip()
        if re.search('double(\s)+gsl_',line):
            if ")" in line:
                functionName = line[7:line.index('(')]

                # ignore functions that are breaking the pipeline
                if "hermite" in functionName or "mathieu" in functionName:
                    continue

                argumentList = line[line.index('(') + 1 : line.index(')')].split(',')
                for i in range(len(argumentList)):
                    argumentList[i] = argumentList[i].strip()

                    while argumentList[i][-1] != ' ':
                        argumentList[i] = argumentList[i][:-1]
                    argumentList[i] = argumentList[i].strip()

                if any("double" in arg for arg in argumentList):
                    signatures[functionName.strip()] = [argumentList]

def argument_extractor_gsl(inFile):
    
    with open(inFile, 'r') as f:
        code = f.readlines()

    for line in code:
        if "TEST_SF(" in line:

            line = line.split(sep='(')
            if len(line) < 3:
                continue

            funcName = line[1].split(sep=',')[-2].strip()
            
            # convert error checking version of function to normal version
            if funcName[-2:] == '_e':
                funcName = funcName[:-2]

            # get argList and remove the error handler argument
            argList = line[2].split(sep=')')[0].split(sep=',')
            for i in range(len(argList)):
                argList[i] = argList[i].strip()
            if '&r' in argList:
                argList = argList[:-1]

            # check to be sure the funcName has been extracted already
            if funcName not in signatures.keys():
                continue

            # get the list of argument types for the func
            argTypes = signatures[funcName][0]

            # check that the lengths are the same
            if len(argTypes) != len(argList):
                continue

            failConversion = False
            for i in range(len(argTypes)):
                if "int" in argTypes[i]:
                    try:
                        argList[i] = int(argList[i])
                    except:
                        failConversion = True
                elif "double" in argTypes[i]:
                    try:
                        argList[i] = float(argList[i])
                    except:
                        failConversion = True

            if not failConversion:
                signatures[funcName].append(argList)


def signature_extractor_python(inFile, libraryName):
    with open(inFile, "r") as source:
        tree = ast.parse(source.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if libraryName in alias.name:
                    if alias.asname and (alias.name, alias.asname) not in imports:
                        imports.append((alias.name, alias.asname))
                    elif (alias.name) not in imports:
                        imports.append((alias.name))

        if isinstance(node,ast.ImportFrom):
            if libraryName in node.module:
                for alias in node.names:
                    if (node.module, alias.name) not in fromImports:
                        fromImports.append((node.module, alias.name))

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                functionName = node.func.id
                literalArguments = []

                # ignore function that is breaking pipeline
                if "ellip_harm" in functionName:
                    continue

                # gather literal arguments
                for arg in node.args:
                    if isinstance(arg, ast.Num):
                        if not isinstance(arg.n, complex):
                            literalArguments.append(arg.n)
                    else:
                        literalArguments = []
                        break

                # if there are literal arguments
                if literalArguments:

                    # if the function is not already in the dict, add it
                    if functionName not in signatures.keys():
                        signatures[functionName] = [literalArguments]
                    # else if the same number of arguments but different arguments, collect them as well (for test migration)
                    elif len(literalArguments) == len(signatures[functionName][0]) and literalArguments not in signatures[functionName]:
                        signatures[functionName].append(literalArguments)
                    else:
                        # if there are a different number of arguments, tag the funcName with _alt
                        functionName = functionName + '_alt'

                        # if the alt funcName is not in the signatures, add a new entry
                        if functionName not in signatures.keys():
                            signatures[functionName] = [literalArguments]

            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    functionName = node.func.value.id + '.' + node.func.attr
                    literalArguments = []
                
                    # ignore function that is breaking pipeline
                    if "ellip_harm" in functionName:
                        continue

                    # gather literal arguments
                    for arg in node.args:
                        if isinstance(arg, ast.Num):
                            if not isinstance(arg.n, complex):
                                literalArguments.append(arg.n)
                            else:
                                literalArguments = []
                                break
                        else:
                            literalArguments = []
                            break

                    # if there are literal arguments
                    if literalArguments:

                        # if the function is not already in the dict, add it
                        if functionName not in signatures.keys():
                            signatures[functionName] = [literalArguments]
                        # else if the same number of arguments but different arguments, collect them as well (for test migration)
                        elif len(literalArguments) == len(signatures[functionName][0]) and literalArguments not in signatures[functionName]:
                            signatures[functionName].append(literalArguments)
                        else:
                            # if there are a different number of arguments, tag the funcName with _alt
                            functionName = functionName + '_alt'

                            # if the alt funcName is not in the signatures, add a new entry
                            if functionName not in signatures.keys():
                                signatures[functionName] = [literalArguments]


if __name__ == "__main__":
    # python3 extractor.py mpmath /usr/local/lib/python3.6/dist-packages/mpmath/tests/
    
    # grab command line arguments
    libraryName = sys.argv[1]
    directory1 = sys.argv[2]

    # grab all files that fit the criteria we're going for
    files = [f for f in os.listdir(directory1) if ("test" in f) or (".h" in f)]

    # make the temp directory to hold binary files
    subprocess.call(["mkdir", "__temp"])

    # for each file
    for file in files:
        if ".py" in file:
            signature_extractor_python(directory1 + file, libraryName)
        elif ".h" in file:
            signature_extractor_c(directory1 + file, libraryName)
        else:
            continue

    for file in files:
        if "test" and ".c" in file:
            argument_extractor_gsl(directory1 + file)

    pprint(signatures)
    
    with open("__temp/__" + libraryName + "_signatures", 'wb') as fp:
        pickle.dump(signatures, fp)

    with open("__temp/__" + libraryName + "_imports", 'wb') as fp:
        pickle.dump(imports, fp)

    with open("__temp/__" + libraryName + "_fromImports", 'wb') as fp:
        pickle.dump(fromImports, fp)