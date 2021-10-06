"""
Assignment 1
"""

import argparse
import logging
import os
import sys
import time
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
    logging.error("Path \"{args.path}\" doesn't exist")
    sys.exit()

my_dict = {
        'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0,
        'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0,
        's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0
        }

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
CHARS = 0

with open(args.path, "rt") as file:
    for line in file:
        for x in line:
            if str.lower(x) in ALPHABET:
                my_dict[str.lower(x)] += 1
                CHARS += 1

file.close()

for x, y in my_dict.items():
    print(f"{x}:{y*100/CHARS:.3f}%")

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
