from multiprocessing import Process, Array, BoundedSemaphore, Semaphore, Lock
from random import randint

#constantes
Crec = 9
Nproc = 3
Mprod = 10

#minimo distinto de -1
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
    
def endMerge(storage):
    n = 0
    f = True
    while n < len(storage) and f:
        f = storage[n] == -1
        n = n+1
    return f
    
def productor(storage, pid, empty, nonEmpty, mutex):
    for i in range(Mprod):
        d = randint(0, Crec)
        
        
        
        empty.acquire()
        
        print(f"Productor {pid} produciendo...")
        
        mutex.acquire()
        storage[pid] = storage[pid] + d
        mutex.release()
        
        nonEmpty.release()
        print(f"Productor {pid} almacenado...")
        
        
    empty.acquire()
    print(f'Produciendo {pid} final')
    
    mutex.acquire()
    storage[pid] = -1
    mutex.release()
    
    nonEmpty.release()
    print(f"Productor {pid} terminado.")
    

def consumidor(storage, emptys, nonEmptys, mergedList):
    end = False
    while not end:
        #mutex.acquire()
        for i in range(Nproc):
            print('waiting... ' + str(i))
            nonEmptys[i].acquire()
        
        print(f"Consumiendo...")
        
        mindex = minIndex(storage)
        if mindex != -1:
            mergedList.append(storage[mindex])
            
            emptys[mindex].release()
        else:
            end = True
        #end = endMerge(storage)
        
        #emptys[mindex].release()
        
        for i in range(Nproc):
            if i != mindex:
                nonEmptys[i].release()
        
        #mutex.release()
        print(f"Consumido producto {mindex}")
    
    print(mergedList)
        

def main():
    mergedList = []
    storage = Array('i', [0]*Nproc)
    mutex = Lock()
    listEmpty = []
    listNonEmpty = []
    
    for i in range(Nproc):
        listEmpty.append(BoundedSemaphore(1))
        listNonEmpty.append(Semaphore(0))
    
    listProd = []
    for i in range(Nproc):
        listProd.append(Process(target=productor, 
                                args=(storage, i, listEmpty[i], listNonEmpty[i], mutex)))
        
    listCons = [Process(target=consumidor,
                        args = (storage, listEmpty, listNonEmpty, mergedList))]
    
    for p in listProd + listCons:
        p.start()
    
    for p in listProd + listCons:
        p.join()
        
    #print(mergedList)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
		
		
