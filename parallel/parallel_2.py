
import os
import multiprocess as mp

#-------------------------------------------------------------------------------
"""
Come  chiamare più processi e collezionare i risultati
"""
def Hello(pos, name):
    msg = f"Hello {name}"
    output.put((pos, msg))

def ese1():
    output = mp.Queue() #creo coda, in cui sono collezionati i risultati di tutti i processi
    process = [mp.Process(target = Hello, args = (x, "Daniele"))  for x in range(4)]

    for p in process:
        p.start()
    for p in process:
        p.join()

    results = [output.get() for p in process] #prendo i risultati dalla coda; noto che non sono necessariamente ordinati
    print(results)

#-------------------------------------------------------------------------------
"""
Alto modo per chiamre più processi; osservo che i worker appena si liberano cominciano
a fare un altro task
"""
def cube(x):
    print(f"{os.getpid()} {os.getppid()}")
    return x**3

def ese2():
    #Altro modo per chiamare un processo: con pool, crea dei lavoratori allocati in core diversi
    proc = mp.Pool(processes = 8)
    results = proc.map(cube, range(1,10)) #map è sincrono: fa in automatico il join dei processi
    print("------SINCRONO------")
    print(results)

    results = proc.map_async(cube, range(1,10)) #map_async è asincrono: in questo modo per prendere i risultati bisogna fare un get()
    print("------ASINCRONO------")
    print(results.get(timeout=1)) #si può mettere un timeout per dare il tempo ai processi di sincronizzarsi

#-------------------------------------------------------------------------------

if __name__ == "__main__":

    #ese1()

    ese2()
