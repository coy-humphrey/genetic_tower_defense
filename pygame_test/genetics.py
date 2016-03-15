import random
import math

def crossover (array1, array2):
	return [random.choice(t) for t in zip(array1, array2)]

def mutate (array1):
	a = array1[:]
	i = random.randint(0, len(array1) - 1)
	a[i] = random.random()
	return a

def normalize (a):
	return [x / float(sum(a)) for x in a]

def fitness(m):
	return m.distance_traveled