import subprocess
import os
import struct
from pprint import pprint
import itertools
import numpy as np

# set working directory
WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)
TIMELIMIT = 60
TOLERANCE = 0.00000001

def reproducer(x):
    CWD = WD + "/spFunDrivers/{:0>3}_discrepancy".format(x)

    executables = [f for f in os.listdir(CWD) if "DRIVER" in f and ".c" not in f]

    for executable in executables:

        library = executable[:executable.index("_")]

        print("\n*************Testing {}... ".format(executable))

        try:
            if ".py" in executable:
                subprocess.call(["python3", executable], cwd=CWD, timeout=TIMELIMIT)
            else:
                subprocess.call(["./{}".format(executable)], cwd=CWD, timeout=TIMELIMIT)
        except subprocess.TimeoutExpired:
            print("EXCEPTION: operation timed out after {} seconds".format(TIMELIMIT))
    
    print()

if __name__ == "__main__":
    x = input("What discrepancy to reproduce? ")

    reproducer(x)