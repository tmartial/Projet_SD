##### Librairies #####
import random as rd
import numpy as np

##### Mutation functions #####

def noise(Tm, pop, eps):
    ''' The noise function adds (or removes) epsilon to genes of the population's indivuals at rate Tm.

        Parameters
        ----------
        Tm : float between 0 and 1
            the mutation rate
        pop : np.array
            the selected individuals, whose genomes are lists of floats
        eps : float 
            the noise, amplitude of the mutation
        
        Returns
        -------
        mut_pop : np.array
            the population whose individuals underwent mutation
        
        >>> pop = np.array([rd.choices([-1,1],k=10),rd.choices([-1,1],k=10)])
        >>> pop
        [[ 1 -1 -1 -1  1  1 -1 -1 -1  1]
        [-1  1 -1 -1 -1  1 -1  1 -1  1]]
        >>> noise(0.5, pop, 5)
        [[ 1 -6  4  4  1  1 -1 -1  4  1]
        [-1  1 -6  4 -1  6 -6  6 -1  1]]
    '''
    mut_pop = np.copy(pop)
    #print(mut_pop)
    #print(np.size(mut_pop,0))
    for i_genome in range(np.size(mut_pop,0)):
        #print("\ncurrent genome : ", mut_pop[i_genome])
        #print(mut_pop)
        for i_gene in range(np.size(mut_pop,1)):
            #print(mut_pop[i_genome][i_gene])
            if rd.random() <= Tm:
                #print("mutation")
                #mut_pop[i_genome][i_gene] = 0
                c = eps*np.random.normal(loc=0.0, scale=1.0, size=None) # à remplacer par np.random.randn ?
                mut_pop[i_genome][i_gene] = abs(mut_pop[i_genome][i_gene] + c)
                #print("mutated gene : ", mut_pop[i_genome][i_gene])
                #print("resulting genome : ", mut_pop[i_genome])
        #print("initial genome : ",pop[i_genome])
        #print("mutated genome : ",mut_pop[i_genome])
    return mut_pop

def noise_gene(gene, eps, Tm):
    if rd.random() <= Tm:
        #print("mutation")
        #mut_pop[i_genome][i_gene] = 0
        c = eps*np.random.normal(loc=0.0, scale=1.0, size=None) # à remplacer par np.random.randn ?
        gene = abs(gene + c)
    return gene

def crossing_over(P, Tc):
    ''' The crossing_over function does a crossing-over between two individuals' genomes at rate Tc.

        If there is crossing-over, there is an exchange between the genes of the genomes i and indc, chosen pseudo-randomly, from the posc position to the end of the genome.
        The posc position is also chosen pseudo-randomly.
        The genomes keep their initial length, because posc is identical for the genomes i and ind.

        Parameters
        ----------
        P : np.array
            the selected individuals, whose genomes are lists of floats
        Tc : float between 0 and 1
            the crossing-over rate

        Returns
        -------
        new_P : np.array
            the population whose individuals underwent crossing-over phenomenons. 
        
        >>> crossing_over(...) #A REMPLIR
    '''
    new_P = np.copy(P)
    
    for i in range(0,len(new_P)):
        if rd.random() < Tc:
            #print("it happened, at : ", i)
            #print(" before : ", new_P)
        
            indc = rd.randint(0, new_P.shape[0]-1) 
            #print("indc : ", indc)
            if indc == i :
                break
            posc = rd.randint(0, new_P.shape[1]-1) 
            #print("posc : ", posc)

            tmp = np.copy(new_P[i,posc:new_P.shape[1]])
            #print("tmp : \n", tmp)
            new_P[i,posc:new_P.shape[1]] = new_P[indc,posc:new_P.shape[1]]
            #print("during \n", new_P)
            #print("tmp : \n", tmp)
            #print("new_P[indc,posc:new_P.shape[1]]\n", new_P[indc,posc:new_P.shape[1]])
            new_P[indc,posc:new_P.shape[1]] = tmp
            #print("after : \n", new_P)
    return new_P

def crossing_over2(parents, Tc):
    ''' The crossing_over function does a crossing-over between two individuals' genomes at rate Tc.
        A METTRE A JOUR 
        If there is crossing-over, there is an exchange between the genes of the genomes i and indc, chosen pseudo-randomly, from the posc position to the end of the genome.
        The posc position is also chosen pseudo-randomly.
        The genomes keep their initial length, because posc is identical for the genomes i and ind.

        Parameters
        ----------
        Parents : list
            parents, list of np.arrays
        Tc : float between 0 and 1
            the crossing-over rate

        Returns
        -------
        child : np.array
            the population whose individuals underwent crossing-over phenomenons. 
        
        >>> crossing_over(...) #A REMPLIR
    '''
    children = np.copy(parents)
    
    for pos in range(0,children.shape[1]-1): # on parcoure le génome du parent 1, avec une chance Tc d'avoir crossing-over
        if rd.random() < Tc:
            #print("it happened, at : ", pos)
            #print(" before : ", new_P)
            tmp = np.copy(children[0,pos:])
            #print("tmp : \n", tmp)
            children[0,pos:] = children[1,pos:]
            #print("during \n", new_P)
            #print("tmp : \n", tmp)
            #print("new_P[indc,posc:new_P.shape[1]]\n", new_P[indc,posc:new_P.shape[1]])
            children[1,pos:] = tmp
            #print("after : \n", new_P)
    return rd.choice(children) # on a créé 2 enfants, on en choisit un pseudo-aléatoirement


def mean_genome(pop, Tmoy):
    ''' The mean_genome function returns the mean of random pairs of genomes from the selected population.
        
        Parameters
        ----------
        pop : np.array
            the selected individuals, whose genomes are lists of ints
        
        Returns
        -------
        mean_pop : np.array
            the population of mean individuals
    '''
    mean_pop = []
    for i in range(0,len(pop)):
            if rd.random() < Tmoy:
                #print("it happened, at : ", i)
                #print(" before : ", new_P)
            
                indc = rd.randint(0, pop.shape[0]-1) 
                #print("indc : ", indc)

                if indc == i :
                    break
                

                mean_pop.append(np.mean(k) for k in zip(pop[i], pop[indc]))

    return list(set(mean_pop))

def mean_genome2(parents):
    return np.mean(parents, axis=0)

##### POPULATION FUNCTION #####

# on ne veut pas reproposer les mêmes images que la génération précédente -> on doit s'assurer que les images de la nouvelle génération sont bien nouvelles
# critère de distance ? sur + d'images générées que nécessaire
# population qu'on va muter -> images sélectionnées 
# une image -> que bruit
# 2 images -> multiplier par 3 pour avoir 6 images -> bruit sur tout -> crossing over -> + 1 enfant qui remplace une des images ?
# fonction coût qui détermine la distance des images générées à celles sélectionnées -> 

def cost(l1,l2):
    ''' The cost function returns the distance (Frobenius Norm) between two numpy.arrays, using the function numpy.linalg.norm.
        
        Parameters
        ----------
        l1 : np.array
            a selected genome
        l2 : np.array
            another selected genome
        
        Returns
        -------
        np.linalg.norm(l1 - l2) : float
            Frobenius norm between l1 and l2
    '''
    return np.linalg.norm(l1 - l2)

def cost_pop(pop1, pop2):
    ''' The cost_pop function returns the distance matrix af two population containing numpy.arrays, using the function numpy.linalg.norm.
        
        Parameters
        ----------
        pop1 : np.array
            a population, whose genomes are np.arrays
        pop2 : np.array
            another population, whose genomes are np.arrays
        
        Returns
        -------
        distance_matrix : 2D np.array
            matrix whose values represent distances between pop1 and pop2 genomes
    '''
    distance_matrix = np.zeros((len(pop1), len(pop2))) # lignes : len(pop1) ; colonnes : len(pop2)
    for l in len(pop1):
        for c in len(pop2):
            if pop1[l] != pop2[c]:
                distance_matrix[l,c] = cost(pop1[l],pop2[c])
    return distance_matrix

# cost between selected and generated pop, or also within generated pop ?


def children_selection(parents, new_pop):
    ''' The children_selection function returns the .
        
        Parameters
        ----------
        parents : np.array
            a population, whose genomes are np.arrays
        new_pop : np.array
            a population, whose genomes are np.arrays, generated with mutations
        
        Returns
        -------
        children : np.array
            matrix whose values represent distances between pop1 and pop2 genomes
    '''
    children = []
    # is a genome too close to others in general ? -> sum 
    
    # is a genome too close to another generated genome ?
    distance_parents = cost_pop(parents, new_pop) # distances between the parents' genomes and the generated ones
    distance_children = cost_pop(new_pop, new_pop) # distances among the generated genomes
    index = []
    # à compléter
    return np.array(children)

def add_ind(pop, ind, pop_size):
    ''' The add_ind function adds a np.array to another np.array, in function of what the additional one contains.
        
        The np.array we want to add to the list can contain one or more genomes. How we add those genomes to the given list depends on this number of genomes. 
        We distinguish the way we add 1 genome and at least 2 genomes. 

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
    '''
    # we check we want to add multiple individuals, which are in a np.array, or just one individual
    # there is a maximum of pop_size individuals we want to add
    # if the length of the "ind" is superior to pop_size, it means what's inside is the genes (64) of the individual and not a np.array reprensenting the genome
    # pop is  a list
    new_pop = pop.copy()
    if (len(ind)>=6): # one individual in a list
        new_pop.append(ind)
    #elif (len(ind)==1): # one individual in a np.array
    #    for i in ind:
    #       for j in i:
    #            new_pop.append(j)
    else : # there are multiple individuals
        for individual in ind:
            new_pop.append(individual)
    return new_pop

#def new_generation(pop, Tm, Tc, Tmoy, eps):
def new_generation(parents_pop, fitness, eliteCount, crossoverFraction, Tc, Tm, pop_size, eps):
    ''' The new_generation function returns the newly generated population according to the choices the user made and given rates.

        The new generation is composed of a given number of elite children, crossing-over children and mutation children. 
        
        
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
        Tc : float between 0 and 1 
            crossing-over rate
        Tm : float between 0 and 1
            mutation rate, usually around 1/length of the genome
        pop_size : int
            the number of picture presented to the user at each generation
        eps : float
            the noise, amplitude of the mutation
        
        Returns
        -------
        new_pop : np.array
           the generated next generation, containing pop_size genomes
    '''
    # fitness: list of fitness -> link with the IHM (selected -> 9, not selected -> 1 for example) in the same order as the pop individuals
    pop = np.copy(parents_pop)
    new_pop = []
    # Elite individuals
    Pc=np.copy(pop)
    index_sort = np.argsort(fitness,axis=0)
    sorted_pop = Pc[index_sort] # on trie les individus par fitness décroissante
    elite_pop = sorted_pop[0:eliteCount] # elite_pop should be a np.array containing np.arrays
                                        # -> raise error if > len(pop) ?
    #print(type(elite_pop))
    new_pop = add_ind(new_pop, np.array(elite_pop), pop_size)
    # THINK OF A MORE EFFICIENT WAY + make a function ?
    #print(new_pop)

    # Crossing over children
    nb_crossover = int((len(pop)-eliteCount)*crossoverFraction)
    for i in range(nb_crossover):
        parents = rd.choices(pop, weights=fitness, k=2) # parents is a list of np.arrays
        new_pop = add_ind(new_pop, crossing_over2(parents, Tc), pop_size)
    #print(new_pop)
    # Fill the new pop
    nb_mutated = int(pop_size + 1 - eliteCount - nb_crossover) #number of individuals who only undergo mutation
    mutated = rd.choices(pop, weights=fitness, k=nb_mutated) # mutated is a list of np.arrays
    new_pop = add_ind(new_pop, mutated, pop_size)
    #print(new_pop)
    # Apply mutation (noise)
    # usually, Tm = 1/len(genome)
    new_pop = noise(Tm, new_pop[eliteCount:], eps)
    #print(new_pop)
    return np.array(new_pop)

def first_generation(pop_size, ind_length, mu, sigma):
    ''' The first_generation function creates a population composed of pseudo-randomly generated vectors.
        
        Parameters
        ----------
        pop_size : int
            size of the population, number of individuals it contains
        ind_length: int
            length of one individual's genome
        E : float
            the noise, amplitude of the values the genes can take
        
        Returns
        -------
        np.array(pop) : np.array
           the generated population, containing pop_size individuals whose genomes contain ind_length genes
    '''
    pop = []
    for ind in range(pop_size):
        pop.append([abs(np.random.normal(loc=mu, scale=sigma, size=None) for i in range(ind_length))])
    return np.array(pop)


##### MAIN ######
#print(help(mutation))
if __name__=="__main__":
    #pop = [np.array(rd.choices([-2,2],k=10)),np.array(rd.choices([-1,1],k=10))]
    pop2 = np.array([np.array(rd.choices([-3,3],k=10)),np.array(rd.choices([-4,4],k=10)),np.array(rd.choices([-6,6],k=10)),np.array(rd.choices([-9,9],k=10)),np.array(rd.choices([-5,5],k=10))]) #elitepop
    #pop3 = rd.choices(pop2, k=2) # parents
    #pop4 = rd.choices(pop2, k=2) #[np.array([rd.choices([-5,5],k=10)])] # one mutation
    #pop4 = [np.array([])]
    #print("pop", pop)
    #print("\npop2", pop2)
    #print("\npop3", pop3)
    #print("\npop4", pop4)
    fitness = [0.9 , 0.5, 0.1, 0.1, 0.9]
    eliteCount = 1
    crossoverFraction = 0.8
    Tc = 0.3
    Tm = 0.1
    pop_size = 5
    eps = 20

    #pop2mut = noise(Tm, pop2, eps)
    

    #print(pop2.shape[0])
    new_pop = new_generation(pop2, fitness, eliteCount, crossoverFraction, Tc, Tm, pop_size, eps)
    print("old_pop\n", pop2)
    print("new_pop\n", new_pop)
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