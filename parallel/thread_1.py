"""
Come gestire i thread in python: bisogna aggirare il GIL
"""

import os

import threading as mt

def task1():
    print("Task1 ")

if __name__ == "__main__":
