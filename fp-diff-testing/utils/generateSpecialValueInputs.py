import random
import struct
import numpy as np
import subprocess
import pickle
import copy

NUMBER_OF_INPUTS = 8


def generateInfs(TEST_INPUTS, ELEMENTARY_INPUTS):
    for pos in range(NUMBER_OF_INPUTS):
        x = copy.deepcopy(ELEMENTARY_INPUTS[list(ELEMENTARY_INPUTS.keys())[pos]])
        x[0][pos] = np.inf

        TEST_INPUTS["all_infInput_pos{}".format(pos)] = x


def generateNegInfs(TEST_INPUTS, ELEMENTARY_INPUTS):
    for pos in range(NUMBER_OF_INPUTS):
        x = copy.deepcopy(ELEMENTARY_INPUTS[list(ELEMENTARY_INPUTS.keys())[pos]])
        x[0][pos] = np.NINF

        TEST_INPUTS["all_negInfInput_pos{}".format(pos)] = x


def generateNans(TEST_INPUTS, ELEMENTARY_INPUTS):
    for pos in range(NUMBER_OF_INPUTS):
        x = copy.deepcopy(ELEMENTARY_INPUTS[list(ELEMENTARY_INPUTS.keys())[pos]])
        x[0][pos] = np.nan

        TEST_INPUTS["all_nanInput_pos{}".format(pos)] = x
        

def generateNegZeros(TEST_INPUTS, ELEMENTARY_INPUTS):
    for pos in range(NUMBER_OF_INPUTS):
        x = copy.deepcopy(ELEMENTARY_INPUTS[list(ELEMENTARY_INPUTS.keys())[pos]])
        x[0][pos] = np.NZERO

        TEST_INPUTS["all_negZeroInput_pos{}".format(pos)] = x


if __name__ == "__main__":
    with open("__temp/__testInputs", 'rb') as f:
        TEST_INPUTS = pickle.load(f)

    with open("__temp/__elementaryInputs", 'rb') as f:
        ELEMENTARY_INPUTS = pickle.load(f)

    generateInfs(TEST_INPUTS, ELEMENTARY_INPUTS)
    generateNans(TEST_INPUTS, ELEMENTARY_INPUTS)
    generateNegInfs(TEST_INPUTS, ELEMENTARY_INPUTS)
    generateNegZeros(TEST_INPUTS, ELEMENTARY_INPUTS)

    with open("__temp/__testInputs", 'wb') as f:
        pickle.dump(TEST_INPUTS, f)