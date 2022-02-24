from multiprocessing import Process, Array, BoundedSemaphore, Semaphore
from random import randint

#constantes
Crec = 9
Nproc = 3
Mprod = 10

def minIndex(storage):
	m = 0
	for i in range(1, len(storage)):
		if storage[i] >= 0 and (storage[m] > storage[i]):
			m = i
	return m

def endMerge(storage):
    n = 0
    f = True
    while n < len(storage) and f:
        f = storage[n] == -1
        n = n+1
    return f
    
def productor(storage, pid, empty, nonEmpty):
	for i in range(Mprod):
		d = randint(0,Crec)
        
		empty.acquire()
        
		print(f"Productor {pid} produciendo...")
		storage[pid] = storage[pid] + d
        
		nonEmpty.release
		print(f"Productor {pid} almacenado...")
        
	empty.adquire()
	storage[pid] = -1
	nonEmpty.release
	print(f"Productor {pid} terminado.")

def consumidor(storage, emptys, nonEmptys, mergedList):
    end = False
    while not end:
        for i in range(Nproc):
            nonEmptys[i].acquire()
        print(f"Consumiendo...")
        mindex = minIndex(storage)
        mergedList.append(storage[mindex])
        end = endMerge(storage)
        emptys[mindex].release()
        print(f"Consumido producto {mindex}")
        

def main():
    mergedList = []
    storage = Array('i', [0]*Nproc)
    listEmpty = []
    listNonEmpty = []
    for i in range(Nproc):
        listEmpty.append(BoundedSemaphore(1))
        listNonEmpty.append(Semaphore(0))
    
    listProd = []
    for i in range(Nproc):
        listProd.append(Process(target=productor, 
                                args=(storage, i, listEmpty[i], listNonEmpty[i])))
        
    listCons = [Process(target=consumidor,
                        args = (storage, listEmpty, listNonEmpty, mergedList))]
    
    for p in listProd + listCons:
        p.start()
    
    for p in listProd + listCons:
        p.join()
        
    print(mergedList)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
		
		
