"""
Assegnamento 1 di parallel computing: calcolare la somma dei numeri primi minori
di un numero, per ciascun numero contenuto in una lista.
"""

import os
import datetime
import math
import logging
import unittest

import multiprocess as mp
import threading    as thr
import matplotlib.pyplot as plt
import numpy as np

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

def is_prime(num):
    """ Cuore del calcolo: verifica se il numero è primo """
    if num == 0 or num == 1:
        return False
    if num == 2 or num == 3:
        return True
    if num % 2 == 0 :
        return False
    i = 3
    while True:
        if num % i == 0 :
            return False
        else:
            i += 2
            if i **2 > num :
                return True

def somma_primi(number, initial_point=0):
    """
    Ricerco i numeri primi < number con il metodo di Fermat e li sommo
    """
    sum = 0
    for num in range(initial_point,number+1):
        if is_prime(num):
            sum+=num
    return sum

def serial_primi(number_list):
    """
    Funzione che serializza in modo intelligente la somma dei numeri primi
    """
    number_list.sort()
    output_dict = {}
    output_dict[ number_list[0] ] = somma_primi( number_list[0] )
    initial_point = number_list[0]
    prec_num = number_list[0]
    for number in number_list[1:]:
        output_dict[number] = somma_primi(number, initial_point)+output_dict[prec_num]
        initial_point = number
        prec_num = number
    #print(output_dict)
    return output_dict

def mp_worker(number_list, initial_point, output_queue):
    """ Funzione lavoratrice per il multiprocessing. Mette i risultati in una que-
    que, organizzati in un dizionario, che viene poi gestita dal multiprocess.
    """
    outdict = {}
    for index, number in enumerate(number_list):
        if index == 0:
            outdict[number] = somma_primi(number, initial_point)
        else:
            outdict[number] = somma_primi(number, number_list[index-1])
    output_queue.put(outdict)

def multiprocess_primi(number_list, n_processes):
    """ Necessita di un lavoratore che produce i risultati, su cui poi viene cre-
    ato il processo.
    """
    output_queue = mp.Queue()
    #calcolo dimensione della lista da mandare ad ogni singolo processo, in modo
    #da sfruttare al meglio la vettorializzazione del problema
    dim = int(math.ceil(len(number_list) / float(n_processes)))
    processes = []
    for i in range (n_processes):
        if i == 0 :
            single_process = mp.Process(target = mp_worker, args = (number_list[dim*i
            : dim *(i+1)], 2, output_queue)) #parto dal 2
        elif dim*i-1<=len(number_list):
            single_process = mp.Process(target = mp_worker, args = (number_list[dim*i
            : dim *(i+1)], number_list[dim*i-1], output_queue))
        else:
            single_process = mp.Process(target = mp_worker, args = (number_list[dim*i
            : dim *(i+1)], 0, output_queue))

        #print(number_list[dim*i-1])
        #print(number_list[dim*i: dim *(i+1)])
        processes.append(single_process)
        #faccio partire il singolo processo
        single_process.start()
    #raccolgo i risultati e sincronizzo i processi
    resultdict = {}

    for i in range(n_processes):
        resultdict.update( output_queue.get() )

    for single_process in processes:
        single_process.join()

    resultdict_sorted = dict(sorted(resultdict.items(), key=lambda item:item[0]))
    final_result = {}
    final_result[number_list[0]] = resultdict_sorted[number_list[0]]
    prec_num = number_list[0]
    for number in number_list[1:]:
        final_result[number] = resultdict_sorted[number] + final_result[prec_num]
        prec_num = number
    return final_result

def plot_results(elapsed):
    """ Crea un plot """
    plt.rcdefaults()
    fig, ax = plt.subplots()
    laby = ('Process 8','Process 4','Process 2','Serial')#'Thread 2','Thread 4','Thread 8','Thread 16','Process 16'
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
    """
    Svolge il running degli algoritmi seriali e multiprocessing
    """
    print('Running benchmark...')
    elapsed_times=[]
    print("now computing multiprocess")
    for numparallel in [8, 4, 2]:
        #tthread=Timer('threaded %s' % numparallel)
        #with tthread as qq:
        #    t_d = multithread_factorize(nums, numparallel)
        #elapsed_times.append(tthread.output())
        tmpar=Timer('mp %s' % numparallel)
        with tmpar as qq:
            m_d = multiprocess_primi(nums, numparallel)#.sort(axis=0)
        if numparallel==8: print(m_d)
        elapsed_times.append(tmpar.output())
    tserial=Timer('serial')
    with tserial as qq:
        print("now computing serial")
        s_d = serial_primi(nums)
    elapsed_times.append(tserial.output())
    print(elapsed_times)
    plot_results(elapsed_times)


class TestPrime(unittest.TestCase):
    """ Class to test serial and multiprocessing algorithm
    """

    def test_serial_vs_multiprocessing(self):
        """Test di consistenza tra i due algoritmi"""
        number_list = [100001, 200003,300003, 400005,500005, 600007,700007, 800009,900009, 1000011]
        self.assertEqual(serial_primi(number_list), multiprocess_primi(number_list, 8))
    def test_serial(self):
        """ Test dell'algoritmo seriale """
        number_list = [100001, 200003,300003, 400005,500005, 600007,700007, 800009,900009, 1000011]
        output = {100001: 454396537, 200003: 1709800816, 300003: 3709707117, 400005: 6459101534,
         500005: 9914436198, 600007: 14072026348, 700007: 18911186316, 800009: 24465863441,
          900009: 30691332276, 1000011: 37551602029}
        self.assertEqual(serial_primi(number_list), output)#serial_primi(number_list)

    def test_multiprocessing(self):
        """ Test dell'algoritmo multiprocessing """
        n_processes = 8
        number_list = [100001, 200003, 300003, 400005,500005, 600007,700007, 800009,900009, 1000011]
        output = {100001: 454396537, 200003: 1709800816, 300003: 3709707117, 400005: 6459101534,
         500005: 9914436198, 600007: 14072026348, 700007: 18911186316, 800009: 24465863441,
          900009: 30691332276, 1000011: 37551602029}
        self.assertEqual(multiprocess_primi(number_list, n_processes), output)

    def test_isprime(self):
        """ Test per l'identificazione del numero primo """
        self.assertEqual(is_prime(290837), True)

def assignment():
    nums = []
    for i in range(100000, 2500001, 100000):
        nums.append(i)
    #print(nums)
    benchmark(nums)

if __name__ == "__main__":
    unittest.main()
    #assignment()
