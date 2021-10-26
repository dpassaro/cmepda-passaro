"""
Come far comunicare i processi tra loro e col programma principale
"""

import multiprocess as mp
 #------------------------------------------------------------------------------
 #SBAGLIATO USARE LE GLOBAL, siccome i processi stanno su processori diversi e così
 #le variabili non sono condivise
def square_list(myList):
    global result
    for num in myList:
        result.append(num**2)
    print(f"Result in process p1: {result}")

p1 = mp.Process(target = square_list, args = ([1,2,3,4],) )
p1.start()
p1.join()
print(f"Result in main program: {result}")
#-------------------------------------------------------------------------------

def square_list(myList, result, square_num):
    for idx
    for num in myList:
        result.append(num**2)
    print(f"Result in process p1: {result}")

result = mp.Array("i", 4) # sta nella shared memory, quindi viene condiviso tra processi diversi
square_sum = mp.Value("i") # sta nella shared memory

p1 = mp.Process(target = square_list, args = ([1,2,3,4],) )
p1.start()
p1.join()
print(f"Result in process p1: {result}")


if __name__ == "__main__":
