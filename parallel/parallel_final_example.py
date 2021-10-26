"""
Confronto tra threads e processes, tratto da Final_example.py .
Obiettivo: fattorizzare una lista di numeri interi

"""

import os
import datetime
import math
import logging

import multiprocess as mp
import threading    as thr
import matplotlib.pyplot as plt
import numpy as np


def factorize(number):
    """
    Funzione che fattorizza (serialmente) un numero; ritorna la lista dei fattori
    del numero in input.
    """
    factors = []
    factor = 2
    i =1
    while True:
        #print(f"Iterazione {i}, factor = {factor}")
        #i += 1
        if number == 1 :
            return factors
        if number % factor == 0 :
            factors.append(factor)
            number = number // factor
        elif factor * factor >= number :
            factors.append(number)
            return factors
        elif factor > 2:
            factor += 2
        else:
            factor += 1

    assert False, "unreachable"

def test_factorize():
    """ Test per la funzione factorize(num) """
    num = 231243539
    factors = factorize(num)
    print(factors)
    prod =1
    for el in factors:
        prod = prod * el
    print(prod)

def serial_factorize(number_list):
    """ Serializzazione della fattorizzazione per una lista di numeri """
    return {number: factorize(number) for number in number_list}

def mp_worker(number_list, output_queue):
    """ Funzione lavoratrice per il multiprocessing. Mette i risultati in una que-
    que, organizzati in un dizionario, che viene poi gestita dal multiprocess.
    """
    outdict = {}
    for number in number_list:
        outdict[number] = factorize(number)
    output_queue.put(outdict)

def multiprocess_factorize(number_list, n_processes):
    """ Necessita di un lavoratore che produce i risultati, su cui poi viene cre-
    ato il processo.
    """
    output_queue = mp.Queue()
    #calcolo dimensione della lista da mandare ad ogni singolo processo, in modo
    #da sfruttare al meglio la vettorializzazione del problema
    dim = int(math.ceil(len(number_list) / float(n_processes)))
    processes = []
    for i in range (n_processes):
        single_process = mp.Process(target = mp_worker, args = (number_list[dim*i
        : dim *(i+1)], output_queue))
        processes.append(single_process)
        #faccio partire il singolo processo
        single_process.start()
    #raccolgo i risultati e sincronizzo i processi
    resultdict = {}
    for i in range(n_processes):
        resultdict.update(output_queue.get())
    for single_process in processes:
        single_process.join()
    return resultdict

def multithread_factorize(number_list, n_threads):
    """ Nel caso del threading, il threading deve essere interno alla funzione sic-
    come è un task di essa, non un processo separato.
    """
    def mt_worker(number_list, outdict):
        """ Lavoratore. Risultati messi in un dizionario, ma non in una coda"""
        for number in number_list:
            outdict[number] = factorize(number)
    #calcolo dimensione della lista da mandare ad ogni singolo thread, in modo
    #da sfruttare al meglio la vettorializzazione del problema
    chunksize = int(math.ceil(len(number_list) / float(n_threads)))
    threads = []
    outs = [{} for i in range(n_threads)]
    for i in range(n_threads):
    # Create each thread, passing it its chunk of numbers to factor
    # and output dict.
        t = thr.Thread(target=mt_worker, args=(number_list[chunksize * i:
        chunksize * (i + 1)], outs[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # Merge all partial output dicts into a single dict and return it
    return {k: v for out_d in outs for k, v in out_d.items()}

class Timer(object):
    """ Calcola tempo per fare i diversi task """
    def __init__(self, name=None):
        self.name = name
        self.timee=0
    def __enter__(self):
        self.tstart = datetime.datetime.now()
    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name, end=' ')
        self.timee=(datetime.datetime.now() - self.tstart).seconds + (datetime.datetime.now() - self.tstart).microseconds/1000000
        print('Elapsed: %s' % (self.timee))
        self.output()
    def output(self):
        return self.timee

def plot_results(elapsed):
    """ Crea un plot """
    plt.rcdefaults()
    fig, ax = plt.subplots()
    laby = ('Serial','Thread 2','Process 2','Thread 4','Process 4','Thread 8','Process 8','Thread 16','Process 16')
    y_pos = np.arange(len(laby))
    ax.barh(y_pos, elapsed, align='center') # align='center'
    ax.set_yticks(y_pos)
    ax.set_yticklabels(laby)
    ax.invert_yaxis() # labels read top-to-bottom
    ax.set_xlabel('Elapsed time')
    ax.set_title('Serial, threads, processes comparison')
    plt.show()
    wait()
def benchmark(nums):
    print('Running benchmark...')
    elapsed_times=[]
    tserial=Timer('serial')
    with tserial as qq:
        s_d = serial_factorize(nums)
    elapsed_times.append(tserial.output())
    for numparallel in [2, 4, 8, 16]:
        tthread=Timer('threaded %s' % numparallel)
        with tthread as qq:
            t_d = multithread_factorize(nums, numparallel)
        elapsed_times.append(tthread.output())
        tmpar=Timer('mp %s' % numparallel)
        with tmpar as qq:
            m_d = multiprocess_factorize(nums, numparallel)
        elapsed_times.append(tmpar.output())
    print(elapsed_times)
    plot_results(elapsed_times)

def test_multiprocessing():
    number_list = (20000001,20000003,20000005,20000007,20000009,200000011,20000011,20000013)
    print(multiprocess_factorize(number_list,2))

def test_multithreading():
    number_list = (20000001,20000003,20000005,20000007,20000009,200000011,20000011,20000013)
    print(multithread_factorize(number_list,2))

if __name__ == "__main__":
    #test_factorize()
    #test_multiprocessing()
    #test_multithreading()
    """N = 299
    nums = [999999999999]
    for i in range(N):
        nums.append(nums[-1] + 2)
    benchmark(nums)"""
