import pyautogui as control
import random
import time
from game_detector import GameDetector
import matplotlib.pyplot as plt

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


class Genetic:
    def __init__(self, p_size, crossover_rate, mutation_rate, chrom_size):
        self.population = []
        self.p_size = p_size
        self.c_rate = crossover_rate
        self.m_rate = mutation_rate
        self.chrom_size = chrom_size
        self.game = GameDetector()
        self.generation = 0
        self.evals = []
        self.counters = []
        self.counter = 0

    def evaluate(self, ch):
        control.click(70*2+40, 308*2+40)
        control.press('space')

        start_time = time.time()
        score = 0
        end_loop = False
        timeout = 60

        while not self.game.is_end():
            for i in range(0, len(ch.genome)-1):
                press = ch.genome[i:i+1]
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
                time.sleep(.15)
                for key in k:
                    control.keyUp(key)

                if (time.time() - start_time > 60 and score < 5) or self.game.is_end():
                    end_loop = True
                    break

                score = self.game.get_score()

            if end_loop:
                break

        self.game.new_game()
        end_time = time.time()

        ch.fitness += (score * 1000)

        time_diff = end_time - start_time
        ch.fitness -= (int(time_diff))

        # taking too long
        if time.time() - start_time > timeout and score < 5:
            control.press('browserrefresh')
            ch.fitness = -1000

        print ch.genome + ':' + str(score) + ':' + str(ch.fitness)
        self.evals.append(ch.fitness)
        self.counters.append(self.counter)
        self.counter += 1

    def eval_all(self):
        for c in self.population:
            self.evaluate(c)

    def gen_chrom(self):
        bs = ''
        for j in range(self.chrom_size):
            key = random.choice('abcdefghijklmnop')
            bs = bs + key
        return Chromosome(bs)

    def init_population(self):
        for i in range(self.p_size):
            c = self.gen_chrom()
            while self.population.__contains__(c):
                c = self.gen_chrom()
            self.population.append(c)

    def mutate(self, ch):
        if random.randint(0, 100) <= random.randint(0, int(self.m_rate * 100)):
            m_index = random.randint(1, len(ch.genome))
            c1 = ch.genome[0:m_index-1]
            c2 = ch.genome[m_index:]
            random_key = random.choice('abcdefghijklmnop')
            print 'MUTATE'
            return Chromosome(c1+random_key+c2)
        else:
            ch.fitness = 0
            return ch

    def single_point_crossover(self, ch1, ch2):
        if random.randint(0, 100) <= random.randint(0, int(self.c_rate * 100)):
            c_index = random.randint(0, len(ch1.genome))
            c11 = ch1.genome[0:c_index]
            c12 = ch1.genome[c_index:]
            c21 = ch2.genome[0:c_index]
            c22 = ch2.genome[c_index:]
            print 'CROSS'
            return Chromosome(c11+c22), Chromosome(c21+c12)
        else:
            ch1.fitness = 0
            ch2.fitness = 0
            return ch1, ch2

    def two_point_crossover(self, ch1, ch2):
        if random.randint(0, 100) <= random.randint(0, int(self.c_rate * 100)):
            i_1 = random.randint(0, len(ch1.genome))
            i_2 = random.randint(0, len(ch1.genome))
            if i_2 < i_1:
                i_1, i_2 = i_2, i_1
            c11 = ch1.genome[0:i_1]
            c12 = ch1.genome[i_1:i_2]
            c13 = ch1.genome[i_2:]
            c21 = ch2.genome[0:i_1]
            c22 = ch2.genome[i_1:i_2]
            c23 = ch2.genome[i_2:]

            print 'CROSS: ' + str(i_1) + '-'+ str(i_2)
            return Chromosome(c11+c22+c13), Chromosome(c21+c12+c23)
        else:
            ch1.fitness = 0
            ch2.fitness = 0
            return ch1, ch2

    def roulette(self):
        total_fitness = 0

        for c in self.population:
            total_fitness += c.fitness

        s = random.random() * total_fitness
        fitness_so_far = 0
        for c in self.population:
            fitness_so_far += c.fitness
            if fitness_so_far >= s:
                return c
        return None

    def repopulate(self):
        new_pop = []
        while len(new_pop) < self.p_size:
            offspring1 = self.roulette()
            offspring2 = self.roulette()
            offspring1, offspring2 = self.two_point_crossover(offspring1, offspring2)
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

        plt.scatter(self.counters, self.evals)
        plt.show()

    def print_pop(self):
        for p in self.population:
            print p.genome

if __name__ == '__main__':
    genetic = Genetic(p_size=1, crossover_rate=.7, mutation_rate=.01, chrom_size=10)
    genetic.init_population()
    p1 = genetic.population[0]

    while True:
        p1 = genetic.mutate(p1)
        genetic.population = [p1]
        genetic.print_pop()