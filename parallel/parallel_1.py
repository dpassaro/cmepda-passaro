"""
Esercizio 1 di parallel computing
"""

import os

from multiprocess import Process

def f0(name):
    print()
    print(f"-------> function {name}")
    print(f"process with ID {os.getpid()}, my father ID is {os.getppid()}") #verifico qual è il processo in esecuzione

def f1(name):
    print()
    print(f"-------> function {name}")
    print(f"process with ID {os.getpid()}, my father ID is {os.getppid()}") #verifico qual è il processo in esecuzione

    f2("two")

def f2(name):
    print()
    print(f"-------> function {name}")
    print(f"process with ID {os.getpid()}, my father ID is {os.getppid()}") #verifico qual è il processo in esecuzione


if __name__ == "__main__":
    print(f"I am in the process with ID {os.getpid()}")
    f0("zero")
    p = Process(target = f1, args = ("one", ))
    p.start()
    p.join()
