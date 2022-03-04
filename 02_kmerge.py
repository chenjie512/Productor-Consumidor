from multiprocessing import Process, Array, BoundedSemaphore, Semaphore, Lock
from random import randint
'''
Merged con Producciones de longitud k
'''
#constantes
Crec = 9    #crecimiento de los valores
Nprod = 10  #numero de productores
Mprod = 20  #numero de producciones
K = 10   #Capacidad del almacen para cada productor

#funcion auxiliar para el calculo del minimo distinto de -1
#si es un un vector d -1, devuelve un -1
def minIndex(storage):
    m = 0
    for i in range(1,len(storage)):
        if storage[m] == -1 or (storage[i]>=0 and storage[i] < storage[m]):
            m = i
    if storage[m] == -1:
        m = -1
    return m

def producer(storage, pid, empty, nonEmpty, mutex):
    #primera produccion
    d = randint(0, Crec)
    empty.acquire()
    print(f'Producer {pid} starting production')
    
    mutex.acquire()
    storage[pid*K] = d
    mutex.release()
    
    lastSaved = 0
    print(f'Producer {pid} stored {storage[pid*K]}...')
    nonEmpty.release()
    #siguientes producciones
    for i in range(Mprod-1):
        d = randint(0, Crec)
        
        empty.acquire()
        
        print(f"Producer {pid} producing...")
        
        mutex.acquire()
        v = storage[lastSaved + pid*K] + d
        lastSaved = (lastSaved + 1)%K
        storage[lastSaved + pid*K] = v
        mutex.release()
        
        print(f"Producer {pid} stored {v}...")
        nonEmpty.release()
        
    #ultima produccion
    empty.acquire()
    print(f'Producer {pid} finishing...')
    
    mutex.acquire()
    storage[((lastSaved+1)%K) + pid*K] = -1
    mutex.release()
    
    nonEmpty.release()
    print(f"Producer {pid} finished.")
    

def merger(storage, emptys, nonEmptys, mutex):
    mergedList = []
    indexlist = [i*K for i in range(Nprod)]    #lista de indices del producto a consumir
                                            # para cada productor
    print(f'Consumer start waiting all')
    
    for i in range(Nprod):
        print(f'Waiting for Producer {i}...')
        nonEmptys[i].acquire()
        print(f'Finished waiting {i}...')
    
    end = False
    while not end:
        print(f'Starting to consume...')
        
        mutex.acquire()
        i = minIndex([storage[j] for j in indexlist])
        mindex = indexlist[i]
        v = storage[mindex]
        mutex.release()
        
        indexlist[i] = (indexlist[i]+1)%K + i*K
        if i != -1:
            print(f'Consumed element from {i}.')
            mergedList.append(v)
            emptys[i].release()
            
            print(f'Waiting for Producer {i}...')
            nonEmptys[i].acquire()
            print(f'Finished waiting Producer {i}...')
            
        else:
            end = True
            print(f'Finished consuming.')
            
    print(mergedList, len(mergedList))

def main():
    storage = Array('i', [0]*Nprod*K)
    mutex = Lock()
    
    listEmpty = [BoundedSemaphore(K) for _ in range(Nprod)]
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
    
    
    
    
    
    
    
    
    
		
		
