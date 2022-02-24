from multiproccesing import Process
from random import randint

#constantes
Crec = 9
Nproc = 3
Mprod = 10

def minIndex(storage):
	m = 0
	for i in range(1, Nprod):
		if storage[i] >= 0 and (storage[m] > storage[i]):
			m = i
	return m

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
	nonEnd = True
	while nonEnd:
		for i in range(Nproc):
			nonEmptys[i].acquire()
		print(f"Consumiendo...")
		mindex = minIndex(storage)
		mergedList.append(storage[mindex])
		emptys[mindex].release()
		print(f"Comsumido producto {mindex}")
		
		for i in range(Nproc):
			nonEmptys[i].acquire()
		nonEnd
