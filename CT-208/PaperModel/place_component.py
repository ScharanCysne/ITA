from random import random
import numpy as np
from simple_evolution_strategy import SimpleEvolutionStrategy
from utils import rotateBinaryImage

class ComponentPlacing:
    """
    This class has methods to init, place component in page,
    provide intersection status and all the placing component
    status that is necessary
    """

    def __init__(self, page, component, num_iterations=200, m0 = None, population_size = 20, 
        mu = 10, covariance_constant = 1000, page_idx=0):
        """ 
        :param page: page where component will be placed
        :type page: 2d np int array
        :param component: component to be placed in page
        :type component: 2d np int array
        :param num_iterations: limit of iteration
        :type num_iterations: int
        :param m0: initial position guess - based on this position, the children 
            will be generetade according to covariance around m0
        :type m0: 2x0 int np array
        :param population_size: population size after generating children, before selecting bests
        :type population_size: int 
        :param mu: number of parents used for computing the mean and 
            covariance of the next generation
        :type param mu: int
        :param covariance_const: covariance constant. Assume C=identy(2x2)*const
        :type covariance_const: 2x2 float array
        """
        self.page = page
        self.page_idx = page_idx
        self.component = component[0]
        self.name = component[1]
        self.componentHeight = np.shape(self.component)[0]
        self.componentLength = np.shape(self.component)[1]
        self.area = self.componentHeight * self.componentLength
        self.num_iterations = num_iterations
        # defines initial guess if none was provided
        if m0 == None:
            self.m0 = np.random.uniform(np.array([0, 0]), 
                np.array([np.shape(self.page)[0]- np.shape(self.component)[0], 
                np.shape(self.page)[1] - np.shape(self.component)[1]]))
        else: self.m0 = m0
        self.population_size = population_size
        self.mu = mu
        self.C0 = np.identity(np.shape(self.m0)[0]) * covariance_constant
        # evolution strategy objetct
        self.es = SimpleEvolutionStrategy(self.m0, self.C0, self.mu, self.population_size)
        self.history_samples = []  # collect the samples of all iterations
        self.placedPosition = np.zeros(2,dtype=int)
        

    def component_cost(self, page, position, component):
        """inputs are equal size 2d arrays
        position is the position where component begins in page
        component is the 2d array of the component
        both are 1 to black and 0 to white
        The cost increases with intersection and with x and y position"""
        pageHeight, pageLength = np.shape(page)
        compHeight, compLength = np.shape(component)

        self.component

        if compHeight > pageHeight or compLength > pageLength:
            intersection_cost =  compHeight * compLength
        else:
            intersection_cost = np.sum(page[position[0]: position[0]+compHeight, position[1]:position[1]+compLength]*component)

        position_cost = np.sqrt((position[0] + compHeight) * (position[1] + compLength))
        cost = intersection_cost * np.sqrt(pageHeight*pageLength) + position_cost

        return cost


    def FindCandidatePosition(self):
        for i in range(self.num_iterations):
            # gets samples from es object
            samples = self.es.ask()

            maxWidth = min(max(self.page.shape[0]-self.component.shape[0],0), self.page.shape[0])
            maxHeight = min(max(self.page.shape[1]-self.component.shape[1],0), self.page.shape[1])
            # clips samples to fit the page:
            samples = np.clip(
                samples, 
                [0,0], 
                [maxWidth,maxHeight]
            )

            # calculates cost for each sample:
            fitnesses = np.zeros(np.size(samples, 0))
            for j in range(np.size(samples, 0)):
                fitnesses[j] = self.component_cost(self.page, samples[j,:], self.component)
            self.es.tell(fitnesses)

            self.history_samples.append(samples)

            # here I change covariance for a fine position tunning
            if i == int(0.7*self.num_iterations):
                self.es.setParameters(C0=self.C0*0.1)
            

    def getHistorySamples(self):
        return self.history_samples


    def getBestSample(self):
        """
        Gets best individual of the the last iteration evolution
        """
        fitnesses = np.zeros(np.size(self.history_samples[-1], 0))
        for j in range(np.size(self.history_samples[-1], 0)):
            fitnesses[j] = self.component_cost(self.page, self.history_samples[-1][j], self.component)
        idx_sorted_function = np.argsort(fitnesses)
        bestSample = self.history_samples[-1][idx_sorted_function[0]]

        return bestSample


    def NoIntersection(self, position = None):
        """
        check if component intersects wiht any other in the page
        True if not intersected, false otherwise
        """
        if position == None:
            position = self.getBestSample()

        pageHeight, pageLength = self.page.shape
        if self.componentHeight > pageHeight or self.componentLength > pageLength:
            qty_intersections =  self.componentHeight * self.componentLength
        else:
            qty_intersections = np.sum((self.page[position[0]:position[0]+self.componentHeight, position[1]:position[1]+self.componentLength]) * self.component)
        return False if qty_intersections else True
            

    def PlaceComponentInPage(self, position = None):
        if position == None:
            position = self.getBestSample()
        self.page[position[0]:position[0]+self.componentHeight, position[1]:position[1]+self.componentLength] = np.clip(
            self.page[position[0]:position[0]+self.componentHeight, position[1]:position[1]+self.componentLength] + self.component,
            0, 1)
        self.placedPosition = position

        return self.page


    def setParameters(self, page=np.array([]), num_iterations=None, m0=None, 
            population_size=None, mu=None, covariance_constant=None, page_idx=None):
        
        if page != np.array([]):
            self.page = page
        if page_idx:
            self.page_idx = page_idx
        if num_iterations:
            self.num_iterations = num_iterations
        if m0 == None:
            self.m0 = np.random.uniform(
                        np.array([0, 0]), 
                        np.array([self.page.shape[0]-self.component.shape[0], self.page.shape[1]-self.component.shape[1]])
                        )
        else: self.m0 = m0

        if population_size:
            self.population_size = population_size
        if mu:
            self.mu = mu
        if covariance_constant:
            self.C0 = np.identity(np.shape(self.m0)[0]) * covariance_constant
        
        self.es.setParameters(m0=self.m0, C0=self.C0, mu=self.mu, population_size=self.population_size)