import csv
import pickle
with open("__temp/__testInputs", 'rb') as fp:
            TEST_INPUTS = pickle.load(fp)

with open('test_1.csv', 'w') as f:
    for key in TEST_INPUTS.keys():
        f.write("%s,%s\n"%(key,TEST_INPUTS[key]))