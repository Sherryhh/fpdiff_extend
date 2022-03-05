import ctypes
import os
import sys
import threading
import time
import csv
import subprocess
import struct
import signal
import warnings
import numpy as np
import multiprocessing
import itertools

# set working directory
WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)

# put drivers directory in path
sys.path.insert(0, './spFunDrivers')

# input category macros
POSITIVE_INPUT = 0
NEGATIVE_INPUT = 1
ZERO_INPUT = 2
INF_INPUT = 3
NAN_INPUT = 4

# discrepancy category macros
TIMEOUT = 1
DOUBLES_FROM_NAN = 2    
DOUBLES_FROM_INF = 3
INACCURACY = 4
MIX_OF_DOUBLES_EXCEPTIONS_SPECIAL_VALUES = 5
MIX_OF_EXCEPTIONS_SPECIAL_VALUES = 6

TIMELIMIT = 60

TOLERANCE = 0.00000001


class Driver:

    def __init__(self, driverName, funcName, libraryName, language, numberOfParameters, callName):
        self.driverName = driverName
        self.funcName = funcName
        self.libraryName = libraryName
        self.language = language
        self.driverText = ""
        self.classificationOutputs = []
        self.exceptionMessages = []
        self.callableDriver = None
        self.numberOfDoubles = 0
        self.numberOfInts = 0
        self.numberOfParameters = numberOfParameters
        self.callName = callName

    def get_callName(self):
        return self.callName

    def get_numberOfParameters(self):
        return self.numberOfParameters

    def get_funcName(self):
        return self.funcName

    def set_numberOfInts(self, x):
        self.numberOfInts = x

    def get_numberOfInts(self):
        return self.numberOfInts

    def get_numberOfDoubles(self):
        return self.numberOfDoubles

    def set_numberOfDoubles(self, x):
        self.numberOfDoubles = x

    def get_numberOfArgs(self):
        return self.numberOfDoubles + self.numberOfInts

    def add_line(self, line):
        self.driverText += line

    def get_driverText(self):
        return self.driverText

    def get_driverName(self):
        return self.driverName

    def run_driver(self, doubles, ints):

        if not self.callableDriver:
            # import the libraries of functions
            import mpmath_drivers as mpmath
            import scipy_drivers as scipy
            gsl = ctypes.CDLL('./spFunDrivers/gsl_drivers.so')

            # set the callable driver for the function
            self.set_callableDriver(getattr(locals()[self.libraryName], self.driverName))

        try:
            # set timeout handler
            signal.signal(signal.SIGALRM, timeoutHandler)

            # if it's python...
            if self.language == "python":            

                # catch warnings and throw exceptions instead
                warnings.simplefilter('error', np.ComplexWarning)
                warnings.simplefilter('error', RuntimeWarning)

                # run the test
                signal.alarm(TIMELIMIT)
                result = self.callableDriver(doubles, ints)
                signal.alarm(0)

                return result

            # if it's C...
            elif self.language == "c":
                # redirect stderr to out
                out = OutputGrabber(sys.stderr)
                out.start()

                # convert lists to c types
                c_doubles = (ctypes.c_double * len(doubles))(*doubles)
                c_ints = (ctypes.c_int * len(ints))(*ints)

                result = 0
                recv_end, send_end = multiprocessing.Pipe(False)
                p = multiprocessing.Process(target=lambda send_end, arg1, arg2: send_end.send(self.callableDriver(arg1, arg2)), args=(send_end, c_doubles, c_ints))
                p.start()

                if recv_end.poll(TIMELIMIT):
                    result = recv_end.recv()
                else:
                    result = "EXCEPTION: TIMEOUT"
                    p.terminate()

                out.stop()

                # if out captured an error...Process
                if out.capturedtext != '':
                    dic = []
                    errText = out.capturedtext.split("\n")
                    errInfo = ""
                    for text in errText:
                        if text not in dic:
                            dic.append(text)
                    for text in dic:
                        if text != '' and text.find("gsl_sf_") == -1:
                            errInfo += text + " "
                    result = "EXCEPTION: " + errInfo

                return result

        # catch python Exceptions and all timeouts
        except Exception as e:
            signal.alarm(0)
            if str(e) == '':
                return "EXCEPTION: " + str(type(e).__name__)
            else:
                return "EXCEPTION: " + str(e)            

    def add_classificationOutput(self, output):
        self.classificationOutputs.append(output)

    def get_classificationOutputs(self):
        return self.classificationOutputs

    def get_id(self):
        return sum(self.classificationOutputs)

    def add_exceptionMessage(self, message):
        self.exceptionMessages.append(message)

    def get_exceptionMessages(self):
        return self.exceptionMessages

    def get_libraryName(self):
        return self.libraryName

    def set_callableDriver(self, callable):
        self.callableDriver = callable
        if self.language == "c":
            self.callableDriver.restype = ctypes.c_double

    def reset_callableDriver(self):
        self.callableDriver = None

    def get_lang(self):
        return self.language


class Discrepancy:

    def __init__(self, classNo, inputName, inputTuple, driverOutputPairs):
        self.classNo = classNo
        
        self.inputName = inputName

        self.inputList = []
        for i in range(driverOutputPairs[0][0].get_numberOfInts()):
            self.inputList.append(inputTuple[1][i])
        for i in range(driverOutputPairs[0][0].get_numberOfDoubles()):
            self.inputList.append(inputTuple[0][i])
        
        self.driverOutputPairs = driverOutputPairs
        self.outputList = [f[1] for f in driverOutputPairs]

        self.inputCategory = categorizeInput(self.inputList)
        self.discrepancyCategory = categorizeDiscrepancy(self.inputCategory, self.outputList)
        self.id = (self.classNo, self.inputCategory, self.discrepancyCategory)

        self.discrepancyNo = 0

        self.absErrs = {}
        self.relErrs = {}

        if self.discrepancyCategory == INACCURACY:
            for pair in itertools.combinations(self.driverOutputPairs, 2):
                libraries = pair[0][0].get_libraryName() + "/" + pair[1][0].get_libraryName()
                absErr = abs(pair[0][1] - pair[1][1])
                relErr = 2 * absErr / max((abs(pair[0][1]) + abs(pair[1][1])), TOLERANCE)
                
                self.absErrs[libraries] = absErr
                self.relErrs[libraries] = relErr

    def set_discrepancyNo(self, x):
        self.discrepancyNo = x

    def get_discrepancyNo(self):
        return self.discrepancyNo

    def get_id(self):
        return self.id

    def get_driverOutputPairs(self):
        return self.driverOutputPairs

    def get_inputName(self):
        return self.inputName

    def get_discrepancyCategory(self):
        return self.discrepancyCategory
    
    def get_inputList(self):
        return self.inputList

    def get_classNo(self):
        return self.classNo

    def get_absErrs(self):
        if self.discrepancyCategory == INACCURACY:
            return self.absErrs
        else:
            return None

    def get_relErrs(self):
        if self.discrepancyCategory == INACCURACY:
            return self.relErrs
        else:
            return None

class OutputGrabber(object):
    """
    Class used to grab standard output or another stream.
    """
    escape_char = "\b"

    def __init__(self, stream=None, threaded=False):
        self.origstream = stream
        self.threaded = threaded
        if self.origstream is None:
            self.origstream = sys.stdout
        self.origstreamfd = self.origstream.fileno()
        self.capturedtext = ""
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        """
        Start capturing the stream data.
        """
        self.capturedtext = ""
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)
        # Replace the original stream with our write pipe:
        os.dup2(self.pipe_in, self.origstreamfd)
        if self.threaded:
            # Start thread that will read the stream:
            self.workerThread = threading.Thread(target=self.readOutput)
            self.workerThread.start()
            # Make sure that the thread is running and os.read() has executed:
            time.sleep(0.01)

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)
        # Flush the stream to make sure all our data goes in before
        # the escape character:
        self.origstream.flush()
        if self.threaded:
            # wait until the thread finishes so we are sure that
            # we have until the last character:
            self.workerThread.join()
        else:
            self.readOutput()
        # Close the pipe:
        os.close(self.pipe_in)
        os.close(self.pipe_out)
        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)
        # Close the duplicate stream:
        os.close(self.streamfd)

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while True:
            char = os.read(self.pipe_out, 1).decode(self.origstream.encoding)
            if not char or self.escape_char in char:
                break
            self.capturedtext += char

            import csv


def prettyPrintClasses(logName):
    with open("logs/{}".format(logName)) as csvfile:
        reader = csv.DictReader(csvfile)

        currentClassNo = -1
        currentTestInput = ''
        for row in reader:
            if int(row["classNo"]) != currentClassNo:
                currentClassNo = int(row["classNo"])
                print()
                print("========================================")
                print("Class {}".format(currentClassNo))
            if row["testInputSource"] != None:
                if row["testInputSource"] != currentTestInput:
                    currentTestInput = row["testInputSource"]
                    print()
                    print("Test input source: <{}>".format(currentTestInput))
                    if int(row['numberOfDoubles']) > 0:
                        doubles = []
                        with open(row['doubleInputPath'], 'rb') as f:
                            for i in range(int(row['numberOfDoubles'])):
                                doubles.append(struct.unpack('d', f.read(8))[0])
                            print("Doubles: {}".format(doubles), end='')
                        
                        if int(row['numberOfInts']) > 0:
                            ints = []
                            with open(row['intInputPath'], 'rb') as f:
                                for i in range(int(row['numberOfInts'])):
                                    ints.append(struct.unpack('i', f.read(4))[0])
                                print(", Integers: {}".format(ints), end='')
                    elif int(row['numberOfInts']) > 0:
                            ints = []
                            with open(row['intInputPath'], 'rb') as f:
                                for i in range(int(row['numberOfInts'])):
                                    ints.append(struct.unpack('i', f.read(4))[0])
                            print("Integers: {}".format(row['intInputPath']), end='')
                    print()

                print()

            if "EXCEPTION" in row['resultFilePath']:
                with open(row['resultFilePath'], 'r') as f:
                    result = f.read()
            else:
                with open(row['resultFilePath'], 'rb') as f:
                    result = struct.unpack('d', f.read(8))[0]

            print("\t{:<35} => {}".format(row['driverName'], result))


def sort_csv(csvFileName):

    with open("{}".format(csvFileName), newline='') as f:
        reader = csv.DictReader(f)
        sortedlist = sorted(reader, key=lambda row:(row['classNo'],row['inputName']), reverse=False)

    subprocess.call(["rm", "-f", "logs/{}".format(csvFileName)])

    with open("{}".format(csvFileName), 'w') as f:
        fieldnames = ['discrepancyNo', 'classNo', 'discrepancyCategory', 'inputName', 'inputList', 'libraryName', 'driverName', 'funcName', 'output', 'absErrs', 'relErrs']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)


''' called when a call to a driver exceeds the TIMELIMIT above '''
def timeoutHandler(num, stack):
    raise Exception("TIMEOUT")


def categorizeDiscrepancy(inputCategory, outputList):

    doubleTally = 0
    exceptionTally = 0
    specialValueTally = 0

    for output in outputList:
        if isinstance(output, str):
            exceptionTally += 1
            
            if "TIMEOUT" in output:
                return TIMEOUT

        elif np.isfinite(output):
            doubleTally += 1
        
        else:
            specialValueTally += 1

    if doubleTally > 0:

        if doubleTally == len(outputList) and inputCategory != NAN_INPUT and inputCategory != INF_INPUT:
            return INACCURACY

        elif inputCategory == NAN_INPUT:
            return DOUBLES_FROM_NAN
            
        elif inputCategory == INF_INPUT:
            return DOUBLES_FROM_INF

        elif (exceptionTally > 0 or specialValueTally > 0):
            return MIX_OF_DOUBLES_EXCEPTIONS_SPECIAL_VALUES

    elif doubleTally == 0:
        if (exceptionTally > 0 or specialValueTally > 0):
            return MIX_OF_EXCEPTIONS_SPECIAL_VALUES

    else:
        raise Exception("UNCLASSIFIABLE DISCREPANCY")

def categorizeInput(inputList):

    if np.isnan(inputList).sum() > 0:
        return NAN_INPUT
    elif np.isinf(inputList).sum() > 0:
        return INF_INPUT
    elif np.isfinite(inputList).prod() != 0:
        if np.array(inputList).prod() == 0:
            return ZERO_INPUT
        else:
            for number in inputList:
                if number < 0:
                    return NEGATIVE_INPUT
            return POSITIVE_INPUT
    else:
        raise Exception("UNCLASSIFIABLE INPUT")