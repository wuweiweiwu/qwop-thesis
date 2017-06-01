import pyautogui as control
import random
import time
import multiprocessing
from game_detector import GameDetector

key_comb = {
    'a': (1, 1, 1, 1),
    'b': (1, 1, 1, 0),
    'c': (1, 1, 0, 1),
    'd': (1, 1, 0, 0),
    'e': (1, 0, 1, 1),
    'f': (1, 0, 1, 0),
    'g': (1, 0, 0, 1),
    'h': (1, 0, 0, 0),
    'i': (0, 1, 1, 1),
    'j': (0, 1, 1, 0),
    'k': (0, 1, 0, 1),
    'l': (0, 1, 0, 1),
    'm': (0, 0, 1, 1),
    'n': (0, 0, 1, 0),
    'o': (0, 0, 0, 1),
    'p': (0, 0, 0, 0)}


class Chromosome:
    def __init__(self, bs):
        # sequence of q w o p and no keypresses
        # takes roughly 1 second for full range of motion
        self.genome = bs
        self.fitness = 0

    def increment(self, i):
        self.fitness += i

    def decrement(self, i):
        self.fitness -= i


class Genetic:
    def __init__(self, p_size, crossover_rate, mutation_rate, chrom_size):
        self.population = []
        self.p_size = p_size
        self.c_rate = crossover_rate
        self.m_rate = mutation_rate
        self.chrom_size = chrom_size
        self.game = GameDetector()
        self.generation = 0

    def evaluate(self, ch):
        control.click(70*2+40, 308*2+40)
        control.press('space')

        start_time = time.time()

        while not self.game.is_end():
            for i in range(len(ch.genome)/2):
                press = ch.genome[i*2:i*2+1]
                dura = float(ch.genome[i*2+1:i*2+2])
                (q, w, o, p) = key_comb.get(press)
                k = []
                if q:
                    k.append('q')
                if w:
                    k.append('w')
                if o:
                    k.append('o')
                if p:
                    k.append('p')
                for key in k:
                    control.keyDown(key)

                time.sleep(3/dura)
                for key in k:
                    control.keyUp(key)
                if self.game.is_end():
                    break

        end_time = time.time()

        score = self.game.get_score()
        ch.increment(score * 1000)

        time_diff = end_time - start_time
        ch.decrement(int(time_diff))

        print ch.genome + ':' + str(ch.fitness)

    def eval_all(self):
        for c in self.population:
            self.evaluate(c)

    def gen_chrom(self):
        bs = ''
        for j in range(self.chrom_size/2):
            key = random.choice('abcdefghijklmnop')
            duration = random.randint(1, 9)
            bs = bs + key + str(duration)
        return Chromosome(bs)

    def init_population(self):
        for i in range(self.p_size):
            c = self.gen_chrom()
            while self.population.__contains__(c):
                c = self.gen_chrom()
            self.population.append(c)

    def mutate(self, ch):
        if random.randint(0, 100) <= random.randint(0, int(self.m_rate * 100)):
            m_index = random.randint(0, len(ch.genome)/2 - 2)
            c1 = ch.genome[0:m_index*2]
            c2 = ch.genome[m_index*2+2:]
            random_key = random.choice('abcdefghijklmnop')
            random_duration = random.randint(1, 9)
            # self.population.remove(ch)
            # self.population.append(Chromosome(c1+random_key+str(random_duration)+c2))
            # print 'pre: '+ch.genome
            # print 'pos: '+c1+random_key+str(random_duration)+c2
            return Chromosome(c1+random_key+str(random_duration)+c2)
        else:
            ch.fitness = 0
            return ch

    def crossover(self, ch1, ch2):
        if random.randint(0, 100) <= random.randint(0, int(self.c_rate * 100)):
            c_index = random.randint(0, len(ch1.genome)/2)
            c11 = ch1.genome[0:c_index*2]
            c12 = ch1.genome[c_index*2:]
            c21 = ch2.genome[0:c_index*2]
            c22 = ch2.genome[c_index*2:]
            # self.population.remove(ch1)
            # self.population.remove(ch2)
            # self.population.append(Chromosome(c11+c22))
            # self.population.append(Chromosome(c21+c12))

            return Chromosome(c11+c22), Chromosome(c21+c12)
            # print 'CROSS'
        else:
            ch1.fitness = 0
            ch2.fitness = 0
            return ch1, ch2

    def roulette(self):
        total_fitness = 0

        for c in self.population:
            total_fitness += c.fitness

        s = random.random() * total_fitness
        fitness_sofar = 0
        for c in self.population:
            fitness_sofar += c.fitness
            if fitness_sofar >= s:
                return c
        return None

    def repopulate(self):
        new_pop = []
        while len(new_pop) < self.p_size:
            offspring1 = self.roulette()
            offspring2 = self.roulette()
            offspring1, offspring2 = self.crossover(offspring1, offspring2)
            offspring1 = self.mutate(offspring1)
            offspring2 = self.mutate(offspring2)
            new_pop.append(offspring1)
            new_pop.append(offspring2)
        self.population = new_pop

    def run(self, i):
        self.init_population()
        while self.generation < i:
            print "GENERATION: "+str(self.generation)
            self.eval_all()
            self.repopulate()
            self.generation += 1

    def print_pop(self):
        for p in self.population:
            print p.genome
