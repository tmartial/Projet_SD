######################
##### Librairies #####
######################

import random as rd
import numpy as np

##############################
##### Mutation functions #####
##############################

def noise(pop, eps, Tm):
    ''' The noise function adds noise to genes of the population's indivuals at rate Tm.

        The noise added is of amplitude eps multiplied by a random sample from the standard normal distribution.
        It does not directly modify the given population (np.array).

        Parameters
        ----------
        pop : np.array
            the selected individuals, whose genomes are lists of floats
        eps : float 
            the range, amplitude of the mutation
        Tm : float between 0 and 1
            the mutation rate, usually equal to the inverse of the length of an individual's genome
        
        Returns
        -------
        mut_pop : np.array
            the population whose individuals underwent mutation
        
        >>> pop = np.array([np.array(rd.choices([-1.,1.],k=10)),np.array(rd.choices([-1.,1.],k=10))])
        >>> pop
        array([[ 1., -1.,  1., -1.,  1.,  1.,  1., -1.,  1.,  1.],
               [ 1.,  1., -1., -1.,  1.,  1., -1., -1., -1., -1.]])
        >>> noise(pop, 5, 0.5)
        array([[ 5.78251086, -1.        ,  1.74370587, -1.        ,  0.31577936,
                 1.        ,  1.        , -1.        ,  1.04432812,  1.83107639],
               [ 2.30186641,  1.        , -1.        , -1.        ,  5.43954382,
                 1.        , -1.        , -1.        , -1.        ,  2.20666446]])
    '''
    mut_pop = np.copy(pop)
    for i_genome in range(np.size(mut_pop,0)):
        for i_gene in range(np.size(mut_pop,1)):
            if rd.random() <= Tm:
                c = eps*np.random.normal(loc=0.0, scale=1.0, size=None)
                mut_pop[i_genome][i_gene] = abs(mut_pop[i_genome][i_gene] + c)
    return mut_pop

def mean_genome(parents):
    ''' The mean_genome function returns the mean of pairs of genomes.
        
        Parameters
        ----------
        parents : np.array
            the selected individuals, whose genomes are np.arrays of ints
        
        Returns
        -------
        mean_pop : np.array
            the population of mean individuals
        
        >>> parents = np.array([np.array(rd.choices([-1.,1.],k=10)),np.array(rd.choices([-3.,3.],k=10))])
        >>> parents
        array([[-1.,  1., -1.,  1.,  1., -1., -1.,  1.,  1., -1.],
               [ 3.,  3.,  3.,  3., -3.,  3.,  3.,  3., -3., -3.]])
        >>> mean_genome(parents)
        array([ 1.,  2.,  1.,  2., -1.,  1.,  1.,  2., -1., -2.])
    '''
    return np.mean(parents, axis=0)

###############################
##### POPULATION FUNCTION #####
###############################

def add_ind(pop, ind, pop_size):
    ''' The add_ind function adds a np.array to a list of np.arrays.
        
        The np.array to be added to the list can contain one or more genomes. 
        How those genomes are added to the given list depends on their number, especially if there is 1 or at least 2 genomes.
        This function does not directly modify the given population (np.array).

        Parameters
        ----------
        pop : list
            a population, which can contain genomes as np.arrays
        ind : np.array
            a population, which contains one or more genomes as np.arrays
        pop_size : int
            the maximum number of individuals of the population
        
        
        Returns
        -------
        new_pop : list
            the newly created population which contains the genomes of pop and ind
        
        >>> pop = [np.array(rd.choices([-1.,1.],k=5)),np.array(rd.choices([-1.,1.],k=5))]
        >>> pop
        array([[ 1.,  1., -1., -1., -1.],
               [ 1., -1.,  1., -1., -1.]])
        
        >>> a = np.array([np.array(rd.choices([-2.,2.],k=5)),np.array(rd.choices([-2.,2.],k=5))])
        >>> a
        array([[-2., -2.,  2., -2.,  2.],
               [ 2., -2., -2.,  2., -2.]])
        >>> add_ind(pop, a, 6)
        [array([ 1., -1.,  1.,  1.,  1.]), array([ 1.,  1., -1., -1.,  1.]), array([-2.,  2., -2., -2.,  2.]), array([-2.,  2., -2.,  2., -2.])]
        
        >>> b = np.array(rd.choices([-4.,4.],k=10))
        >>> b
        array([ 4.,  4.,  4.,  4., -4.])
        >>>add_ind(pop, b, 6)
        [array([ 1.,  1., -1., -1., -1.]), array([ 1., -1.,  1., -1., -1.]), array([ 4.,  4.,  4.,  4., -4.])]
    '''
    # There is a maximum of pop_size individuals we want to add
    # If the length of the ind is superior to pop_size, it means what's inside is the genes (64) of the individual and not a np.array reprensenting the genome
    new_pop = pop.copy()

    if (len(ind)>=pop_size):    # In this cas, there is one individual in ind
        new_pop.append(ind)
    
    else :                      # In this case, there are multiple individuals in ind
        for individual in ind:
            new_pop.append(individual)
    
    return new_pop       
def new_generation(parents_pop, fitness_, eliteCount = 1, crossoverFraction = 0.8, pop_size = 6, Tm = 0.1, eps = 2.5, shuffle = False):
    ''' The new_generation function returns a newly generated population when given a parents' population, according to the choices the user made and given rates.

        The new generation is composed of a given number of elite children, crossing-over children and mutated parents. 
        This function does not affect the given data (parents_pop, fitness_)
        
        Parameters
        ----------
        pop : np.array
            a population of size pop_size, whose genomes are np.arrays
        fitness : np.array
            a np.array containing the fitness values of the individuals of the population, in the same order. The fitness is determined by the user choices.
        eliteCount : int
            number of individuals with the best fitness values that are guaranteed to survive to the next generation
        crossoverFraction : float between 0 and 1
            fraction of individuals in the new generation, other than elite children, that are created by crossover
        pop_size : int
            the number of picture presented to the user at each generation
        Tm : float between 0 and 1
            mutation rate, usually around 1/length of the genome
        eps : float
            the noise, amplitude of the mutation
        shuffle : boolean
            default is set to False, shuffles the new generated populated if set to True
        
        Returns
        -------
        new_pop : np.array
           the generated next generation, containing pop_size genomes
    '''
    pop = np.copy(parents_pop)
    fitness = np.copy(fitness_)
    new_pop = []

    # Elite individuals
    Pc=np.copy(pop)
    index_sort = np.argsort(fitness,axis=0)
    sorted_pop = Pc[index_sort] # the individuals are sorted by ascending fitness order
    elite_pop = sorted_pop[::-1][0:eliteCount] # elite_pop should be a np.array containing np.arrays
    new_pop = add_ind(new_pop, np.array(elite_pop), pop_size)
    #print("elite", new_pop)

    # Crossing over children
    nb_crossover = int((pop_size-eliteCount)*crossoverFraction) # number of individuals who are a result of crossing_over
    while (len(new_pop)< (eliteCount + nb_crossover)):
        i_parents = np.random.choice(len(pop), 2, replace=False, p=fitness/sum(fitness)) 
        child = mean_genome(pop[i_parents])
        if not np.any(np.all(child == new_pop, axis=1)): # only parents who don't already have a child together are selected
            new_pop = add_ind(new_pop, child, pop_size)
            #print("CO child", new_pop)

    # Fill the new population
    # we now want to select only individuals who are not elite children. 
    pop = np.delete(pop, index_sort[::-1][0:eliteCount], axis=0)
    fitness = np.delete(fitness, index_sort[::-1][0:eliteCount], axis=0)
    

    nb_mutated = int(pop_size - eliteCount - nb_crossover) #number of individuals who only undergo mutation
    i_mutated = np.random.choice(len(pop), nb_mutated, replace=False, p=fitness/sum(fitness))
    new_pop = add_ind(new_pop, pop[i_mutated], pop_size)
    #print("filled", new_pop)

    # Apply mutation (noise) on every children except elite children
    new_pop[eliteCount:] = noise(new_pop[eliteCount:], eps, Tm)
    #print("mutated", new_pop)

    if shuffle:
        #print("before shuffling", new_pop)
        rd.shuffle(new_pop)
        #print("shuffled", new_pop)

    return np.array(new_pop)

#################
##### MAIN ######
#################

#print(help(mutation))
if __name__=="__main__":
    #pop = [np.array(rd.choices([-2,2],k=10)),np.array(rd.choices([-1,1],k=10))]
    pop2 = np.array([np.array(rd.choices([-3,3],k=10)),np.array(rd.choices([-4,4],k=10)),np.array(rd.choices([-6,6],k=10)),np.array(rd.choices([-9,9],k=10)),np.array(rd.choices([-5,5],k=10))]) #elitepop
    #pop2 = [np.array(rd.choices([-3,3],k=10)),np.array(rd.choices([-4,4],k=10)),np.array(rd.choices([-6,6],k=10)),np.array(rd.choices([-9,9],k=10)),np.array(rd.choices([-5,5],k=10))] #elitepop
    #pop3 = rd.choices(pop2, k=2) # parents
    #pop4 = rd.choices(pop2, k=2) #[np.array([rd.choices([-5,5],k=10)])] # one mutation
    #pop4 = [np.array([])]
    #print("pop", pop)
    #print("\npop2", pop2)
    #print("\npop3", pop3)
    #print("\npop4", pop4)
    fitness = np.array([0.9 , 0.5, 0.1, 0.1, 0.9])
    eliteCount = 1
    crossoverFraction = 0.8
    Tm = 0.1
    pop_size = 6
    eps = 20

    #L = np.copy(pop2[1])
    #K = np.array(rd.choices([-10,10],k=10))

    #print("pop", pop2)
    #print("L",L)
    #print("K", K)
    #print("L in pop", np.any(np.all(L == pop2, axis=1)))
    #print("K in pop",np.any(np.all(K == pop2, axis=1)))
    
    #pop2mut = noise(Tm, pop2, eps)
    
    #print(pop2.shape[0])
    new_pop = new_generation(pop2, fitness, eliteCount, crossoverFraction, pop_size, Tm, eps, True)
    print("old_pop\n", pop2)
    print("new_pop\n", new_pop)
    #print(len(pop2))
    #print(type(pop2[0]))
    #print(type(pop2[0,0]))
    #print("\n")
    #print(len(new_pop))
    #print(type(new_pop[0]))
    #print(type(new_pop[0,0]))

    #pop_test1 = add_ind(pop, pop2, 6)
    #print("\npoptest1", pop_test1)
    
    #pop_test2 = add_ind(pop, pop3, 6)
    #print("\npoptest2", pop_test2)
    #print(len(pop3))
    #pop_test3 = add_ind(pop, pop4, 6)
    #print("\npoptest3", pop_test3)
    #print('\n',pop4)
    
    #print(pop,'\n')
    #popm = noise(0.5, pop, 5)
    #print("noise:\n",popm,'\n')
    #popmc = crossing_over2(pop, 0)
    #print("crossing over:\n",popmc)
   # print(mean_genome(popmc, 0.5))

    #pop = [np.array(rd.choices([-1.,1.],k=10)),np.array(rd.choices([-1.,1.],k=10))]
    #a = np.array([np.array(rd.choices([-2.,2.],k=10)),np.array(rd.choices([-2.,2.],k=10))])
    #print("pop", pop)
    #print("a", a)
    #print("add", add_ind(pop, a, 6))
    #print(help(noise))

   
   