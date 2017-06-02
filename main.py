from genetic_algo import Genetic

if __name__ == '__main__':

    genetic = Genetic(p_size=10, crossover_rate=.7, mutation_rate=.01, chrom_size=10)
    genetic.run(50)
