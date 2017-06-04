from genetic_algo import Genetic

if __name__ == '__main__':

    genetic = Genetic(p_size=20, crossover_rate=.8, mutation_rate=.1, chrom_size=20)
    genetic.run(5)
