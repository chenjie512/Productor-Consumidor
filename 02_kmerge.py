from multiprocessing import Process, Array, BoundedSemaphore, Semaphore, Lock
from random import randint
'''
Merged con Producciones de longitud k
'''
#constantes
Crec = 9    #crecimiento de los valores
Nprod = 3  #numero de productores
Mprod = 10  #numero de producciones
K = 5

#funcion auxiliar para el calculo del minimo distinto de -1
#si es un un vector d -1, devuelve un -1
def minIndex(storage):
    m = 0
    for i in range(1,len(storage)):
        #if storage[m] == -1:
            #m = i
        if storage[m] == -1 or (storage[i]>=0 and storage[i] < storage[m]):
            m = i
    if storage[m] == -1:
        m = -1
    return m

def producer(storage, pid, empty, nonEmpty, mutex):
    d = randint(0, Crec)
    empty.acquire()
    print(f'Producer {pid} starting production')
    mutex.acquire()
    storage[pid*K]
    
    
    lastSaved = 0
    for i in range(Mprod):
        d = randint(0, Crec)
        
        empty.acquire()
        
        print(f"Producer {pid} producing...")
        
        mutex.acquire()
        storage[pid] = storage[pid] + d
        mutex.release()
        
        print(f"Producer {pid} stored {storage[pid]}...")
        nonEmpty.release()
        
        
    empty.acquire()
    print(f'Producer {pid} finishing...')
    
    mutex.acquire()
    storage[pid] = -1
    mutex.release()
    
    nonEmpty.release()
    print(f"Producer {pid} finished.")
    

def merger(storage, emptys, nonEmptys, mutex):
    mergedList = []
    print(f'Consumer start waiting all')
    
    for i in range(Nprod):
        print(f'Waiting for Producer {i}...')
        nonEmptys[i].acquire()
        print(f'Finished waiting {i}...')
    
    end = False
    while not end:
        #mutex.acquire()
        print(f'Starting to consume...')
        
        mutex.acquire()
        mindex = minIndex(storage)
        v = storage[mindex]
        mutex.release()
        
        if mindex != -1:
            print(f'Consumed element from {mindex}.')
            mergedList.append(v)
            emptys[mindex].release()
            
            print(f'Waiting for Producer {mindex}...')
            nonEmptys[mindex].acquire()
            print(f'Finished waiting Producer {mindex}...')
            
        else:
            end = True
            print(f'Finished consuming.')
    print(mergedList, len(mergedList))

def main():
    storage = Array('i', [0]*Nprod)
    mutex = Lock()
    
    listEmpty = [BoundedSemaphore(1) for _ in range(Nprod)]
    listNonEmpty = [Semaphore(0) for _ in range(Nprod)]
    
    listProd = [Process(target=producer, 
    args=(storage, i, listEmpty[i], listNonEmpty[i], mutex)) for i in range(Nprod)]
        
    listCons = [Process(target=merger,
                        args = (storage, listEmpty, listNonEmpty, mutex))]
    
    for p in listProd + listCons:
        p.start()
    
    for p in listProd + listCons:
        p.join()

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
		
		
