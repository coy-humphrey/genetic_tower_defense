import random
import math
import mob
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
	return m.distance_traveled + 100 * m.attacked + (m.hp / m.max_health * 500)

def get_n_winners(breedlist, n):
	return sorted(breedlist, key=fitness, reverse=True)[:n]

def get_n_crossovers(parents, n, mob_start, mob_path):
	if not parents: return
	results = []
	for i in range(n):
		p1 = random.choice(parents)
		p2 = random.choice(parents)
		new_stats = crossover (p1.statArray, p2.statArray)
		results.append(mob.Mob(mob_start, (255,0,0), mob_path, new_stats))

	return results

def get_n_mutants(parents, n, mob_start, mob_path):
	if not parents: return
	results = []
	for i in range(n):
		p = random.choice(parents)
		new_stats = mutate(p.statArray)
		results.append(mob.Mob(mob_start, (255,0,0), mob_path, new_stats))

	return results