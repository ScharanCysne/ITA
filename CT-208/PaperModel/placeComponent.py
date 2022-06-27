import cma
import numpy as np

class ComponentPlacing:
    """
    This class has methods to init, place component in page,
    provide intersection status and all the placing component
    status that is necessary
    """

    def __init__(self, page, component, sigma=1.0, population=8, num_iterations=200, page_idx=0):
        """ 
        :param page: page where component will be placed
        :type page: 2d np int array
        :param component: component to be placed in page
        :type component: 2d np int array
        :param num_iterations: limit of iteration
        :type num_iterations: int
        """
        self.page = page
        self.page_idx = page_idx
        self.component = component[0]
        self.name = component[1]
        self.componentHeight = np.shape(self.component)[0]
        self.componentLength = np.shape(self.component)[1]
        self.area = self.componentHeight * self.componentLength
        self.num_iterations = num_iterations
        
        self.maxWidth = min(max(page.shape[0] - self.component.shape[0],0), self.page.shape[0])
        self.maxHeight = min(max(page.shape[1] - self.component.shape[1],0), self.page.shape[1])
            
        # defines initial guess
        m0 = np.random.uniform(
                np.array([0, 0]),                                                                                                 # min
                np.array([np.shape(page)[0]- np.shape(self.component)[0], np.shape(page)[1] - np.shape(self.component)[1]])       # max
            )
        
        # CMA-ES
        self.es = cma.CMAEvolutionStrategy(m0, sigma, {"popsize": population})
        self.history_samples = []
        self.placedPosition = np.zeros(3)
        

    def componentCost(self, page, position):
        """
        Inputs are equal size 2D Arrays: 
        'position' is the position where component begins in page
        'component' is the 2D Array of the component (both are 1 to black and 0 to white)
        
        The cost increases with intersection and with x and y position
        """
        position = np.round(position)
        positionX = int(position[0])
        positionY = int(position[1])

        pageHeight, pageLength = np.shape(page)
        compHeight, compLength = np.shape(self.component)

        if compHeight > pageHeight or compLength > pageLength:
            intersection_cost =  compHeight * compLength
        else:
            intersection_cost = np.sum(page[positionX:positionX+compHeight, positionY:positionY+compLength]*self.component)

        position_cost = np.sqrt((positionX + compHeight) * (positionY + compLength))
        cost = intersection_cost * np.sqrt(pageHeight*pageLength) + position_cost

        return cost


    def FindCandidatePosition(self):
        """
        Finds best position of component in page
        """
        for _ in range(self.num_iterations):
            # gets samples from es object
            samples = self.es.ask()
            # clips samples to fit the page:
            samples = np.clip(
                samples, 
                [0, 0], 
                [self.maxWidth, self.maxHeight]
            )
            # calculates cost for each sample:
            fitnesses = [self.componentCost(self.page, sample) for sample in samples]
            # Update CMA-ES
            self.es.tell(samples, fitnesses)
            self.history_samples.append(samples)


    def getHistorySamples(self):
        """
        Return history of samples
        """
        return self.history_samples


    def getBestSample(self):
        """
        Gets best individual of the the last iteration evolution
        """
        fitnesses = [self.componentCost(self.page, sample) for sample in self.history_samples[-1]]
        idx_sorted_function = np.argsort(fitnesses)
        bestSample = self.history_samples[-1][idx_sorted_function[0]]
        return bestSample


    def NoIntersection(self, position=None):
        """
        Checks if component intersects wiht any other in the page
        True if not intersects, false otherwise
        """
        if position == None:
            position = self.getBestSample()

        pageHeight, pageLength = np.shape(self.page)
        if self.componentHeight > pageHeight or self.componentLength > pageLength:
            qty_intersections =  self.componentHeight * self.componentLength
        else:
            position = np.round(position)
            positionX = int(position[0])
            positionY = int(position[1])
                
            qty_intersections = np.sum((self.page[positionX:positionX+self.componentHeight, positionY:positionY+self.componentLength]) * self.component)
        
        return False if qty_intersections else True
            

    def PlaceComponentInPage(self, position = None):
        """
        Places component in page and return current page
        """
        if position == None:
            position = self.getBestSample()

        position = np.round(position)
        positionX = int(position[0])
        positionY = int(position[1])

        self.page[positionX:positionX+self.componentHeight, positionY:positionY+self.componentLength] = np.clip(
            self.page[positionX:positionX+self.componentHeight, positionY:positionY+self.componentLength] + self.component,
            0, 1)
        self.placedPosition = position

        return self.page

    
    def resetParameters(self):
        # defines initial guess
        m0 = np.random.uniform(
                np.array([0, 0]),                                                                                                       # min
                np.array([np.shape(self.page)[0]- np.shape(self.component)[0], np.shape(self.page)[1] - np.shape(self.component)[1]])    # max
            )
        
        # CMA-ES
        self.es = cma.CMAEvolutionStrategy(m0, 1.0, {"popsize": 18})
        