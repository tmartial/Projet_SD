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
    #print(type(mut_pop))
    #print(np.size(mut_pop,0))
    for i_genome in range(np.size(mut_pop,0)):
        #print("\ncurrent genome : ", mut_pop[i_genome])
        for i_gene in range(np.size(mut_pop,1)):
            #print(mut_pop[i_genome][i_gene])
            if rd.random() <= Tm:
                #print("mutation")
                #mut_pop[i_genome][i_gene] = 0
                sign = rd.choice([-1,1])
                mut_pop[i_genome][i_gene] = mut_pop[i_genome][i_gene] + sign*eps
                #print("mutated gene : ", mut_pop[i_genome][i_gene])
                #print("resulting genome : ", mut_pop[i_genome])
        #print("initial genome : ",pop[i_genome])
        #print("mutated genome : ",mut_pop[i_genome])
    return mut_pop

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




##### MAIN ######
#print(help(mutation))
if __name__=="__main__":
    pop = np.array([rd.choices([-1,1],k=10),rd.choices([-1,1],k=10)])
    print(pop,'\n')
    popm = noise(0.5, pop, 5)
    print(popm,'\n')
    popmc = crossing_over(popm, 0.5)
    print(popmc)

    print(mean_genome(popmc, 0.5))