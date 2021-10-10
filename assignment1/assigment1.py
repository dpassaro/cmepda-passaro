"""
Assignment 1
"""

# pylint: disable=logging-fstring-interpolation

import argparse
import logging
import os
import sys
import time
import string

import matplotlib.pylab as plt

start_time = time.time()

parser = argparse.ArgumentParser()

parser.add_argument("path", type=str,  help = "Path to text file")
parser.add_argument("-hist", "--histogram", help = "Show frequencies histogram",action="store_true")
parser.add_argument("-skip", "--skip_parts", help = "Skip unuseful parts",action="store_true")
parser.add_argument("-stat", "--basic_statistics", help = "Basic statistics",action="store_true")

args = parser.parse_args()

if args.histogram :
    logging.info("Frequencies histogram set on")

if args.skip_parts:
    logging.info("Skip unuseful parts set on")

if args.basic_statistics:
    logging.info("Computing basic statistics")

if os.path.exists(args.path):
    logging.info("Correct Path")
else:
    logging.error(f"Path \"{args.path}\" doesn't exist")
    sys.exit()

my_dict = { key : 0 for key in string.ascii_lowercase }

CHARS = 0

with open(args.path, "rt", encoding = 'utf-8') as file:
    text = file.read()

for x in text:
    if str.lower(x) in my_dict:
        my_dict[str.lower(x)] += 1
        CHARS += 1

file.close()

for letter, occurences in my_dict.items():
    print(f"{letter}: {occurences*100/CHARS:.3f} %")

final_time = time.time()
print(f"Elapsed time: {final_time-start_time :.3f} s")

if args.histogram :
    keys = list(my_dict.keys())
    counts_ = list(my_dict.values())
    counts = []
    for el in counts_:
        counts.append(el*100/CHARS)

    plt.bar(keys, counts)
    plt.grid(True)
    plt.show()
