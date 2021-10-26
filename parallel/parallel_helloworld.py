"""
Esercizio 1 di parallel computing
"""

from multiprocess import Process

def f(name):
    print(f"Hello {name}")

if __name__ == "__main__":
    p = Process(target = f, args = ("Daniele",)) #chiamata ad un processo differente: devo puntare una funzione con degli argomenti
    p.start() #faccio partire il processo in modo asincrono
    p.join() #aspetta il completamento del processo prima di uscire dal programma
