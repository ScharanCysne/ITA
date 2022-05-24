import numpy as np

class SimpleEvolutionStrategy:
    """
    Represents a simple evolution strategy optimization algorithm.
    The mean and covariance of a gaussian distribution are evolved at each generation.
    """
    def __init__(self, m0, C0, mu, population_size):
        """
        Constructs the simple evolution strategy algorithm.

        :param m0: initial mean of the gaussian distribution.
        :type m0: numpy array of floats.
        :param C0: initial covariance of the gaussian distribution.
        :type C0: numpy matrix of floats.
        :param mu: number of parents used to evolve the distribution.
        :type mu: int.
        :param population_size: number of samples at each generation.
        :type population_size: int.
        """
        self.m = m0
        self.C = C0
        self.mu = mu
        self.population_size = population_size
        self.samples = (np.random.multivariate_normal(self.m, self.C, self.population_size)).astype(int)

    def ask(self):
        """
        Obtains the samples of this generation to be evaluated.
        The returned matrix has dimension (population_size, n), where n is the problem dimension.

        :return: samples to be evaluated.
        :rtype: numpy array of floats.
        """
        return self.samples

    def tell(self, fitnesses):
        """
        Tells the algorithm the evaluated fitnesses. The order of the 
            fitnesses in this array
        must respect the order of the samples.

        :param fitnesses: array containing the value of 
            fitness of each sample.
        :type fitnesses: numpy array of floats.
        """
        # vetor de índice da função ordenada
        idx_sorted_function = np.argsort(fitnesses)
        # ordena os samples de acordo com o vetor anterior
        self.samples = self.samples[idx_sorted_function]
        # seleciona os mu melhores para gerarem a média 
        # da próxima geração
        parents = self.samples[0: self.mu]
        # calcula a média da próxima geração com os mu melhores
        self.m = np.average(parents, axis = 0)
        # evolui a covariância 
        """ self.C = np.zeros([2,2])
        for i in range(0, self.mu):
            aux = np.array([parents[i]-self.m])
            self.C += aux.T.dot(aux)
        self.C = self.C / self.mu """
        #print('cov:')
        #print(self.C)
        # gera a próxima geração baseado na média m, C e 
        # no tamanho da população
        self.samples = (np.random.multivariate_normal(self.m, self.C, self.population_size)).astype(int)


    def setParameters(self, m0 = np.array([]), C0 = np.array([]), mu = None, population_size = None):
        if m0 != np.array([]):
            self.m = m0
        if C0 != np.array([]):
            self.C = C0
        if mu:
            self.mu = mu
        if population_size:
            self.population_size = population_size            
        self.samples = (np.random.multivariate_normal(self.m, self.C, self.population_size)).astype(int)