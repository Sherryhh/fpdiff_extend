import csv
import pickle
import ast
import os

d_p = "./per_function/"

# def convert(filename, i):
#     reader = csv.reader(open(d_p+filename, 'r'))
#     d = {}
#     for row in reader:
#         k, v = row[0], row[1]
#         for r in row[2:]:
#             v = v+","+r
#         d[k] = ast.literal_eval(v)

#     with open("one_inputs/__testInputs"+str(i), 'wb') as fp:
#         pickle.dump(d, fp)

# directory = os.fsencode(d_p)
# i = 0
# for file in os.listdir(directory):
#      filename = os.fsdecode(file)
#      convert(filename, i)
#      i += 1
reader = csv.reader(open('./test.csv', 'r'))
d = {}
for row in reader:
    k, v = row[0], row[1]
    for r in row[2:]:
        v = v+","+r
    # print(v)
    d[k] = ast.literal_eval(v)

with open("__temp/__testInputs", 'wb') as fp:
    pickle.dump(d, fp)