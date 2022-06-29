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
        self.population = population
        self.component = component[0]
        self.name = component[1]
        self.area = np.shape(self.component)[0] * np.shape(self.component)[1]
        self.num_iterations = num_iterations
        
        self.maxWidth = min(max(page.shape[0] - self.component.shape[0],0), page.shape[0])
        self.maxHeight = min(max(page.shape[1] - self.component.shape[1],0), page.shape[1])
            
        # defines initial guess
        m0 = np.random.uniform(
                np.array([0, 0, 0]),                                                                                                  # min
                np.array([np.shape(page)[0]- np.shape(self.component)[0], np.shape(page)[1] - np.shape(self.component)[1], 1]),       # max
            )
        
        # CMA-ES
        self.es = cma.CMAEvolutionStrategy(m0, sigma, {"popsize": self.population})
        self.history_samples = []
        self.placedPosition = np.zeros(3)
        

    def componentCost(self, page, position):
        """
        Inputs are equal size 2D Arrays: 
        'position' is the position where component begins in page
        'component' is the 2D Array of the component (both are 1 to black and 0 to white)
        
        The cost increases with intersection and with x and y position
        """
        rotated = False
        position = np.round(position)
        positionX = int(position[0])
        positionY = int(position[1])
        angle = int(position[2])

        component = self.component.copy()
        if angle:
            component = np.rot90(component, k=1, axes=(1,0))
            rotated = True 

        pageHeight, pageLength = np.shape(page)
        compHeight, compLength = np.shape(component)

        if compHeight > pageHeight or compLength > pageLength or positionX+compHeight > pageHeight or positionY+compLength > pageLength:
            intersection_cost =  compHeight * compLength
        else:
            intersection_cost = np.sum(page[positionX:positionX+compHeight, positionY:positionY+compLength]*component)

        position_cost = np.sqrt(positionX * positionY)
        cost = intersection_cost * np.sqrt(pageHeight*pageLength) + position_cost

        return cost, rotated


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
                [0, 0, 0], 
                [self.maxWidth, self.maxHeight, 1]
            )
            # calculates cost for each sample:
            fitnesses = [self.componentCost(self.page, sample)[0] for sample in samples]
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
        fitnesses = [self.componentCost(self.page, sample)[0] for sample in self.history_samples[-1]]
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

        position = np.round(position)
        positionX = int(position[0])
        positionY = int(position[1])
        angle = int(position[2])

        component = self.component.copy()
        if angle:
            component = np.rot90(component, k=1, axes=(1,0))

        pageHeight, pageLength = np.shape(self.page)
        componentHeight, componentLength = np.shape(component)

        if componentHeight > pageHeight or componentLength > pageLength or positionX+componentHeight > pageHeight or positionY+componentLength > pageLength:
            qty_intersections =  componentHeight * componentLength
        else:
            qty_intersections = np.sum((self.page[positionX:positionX+componentHeight, positionY:positionY+componentLength]) * component)
        
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
        angle = int(position[2]) 

        component = self.component.copy()
        if angle:
            component = np.rot90(component, k=1, axes=(1,0))

        componentHeight = np.shape(component)[0]
        componentLength = np.shape(component)[1]

        self.page[positionX:positionX+componentHeight, positionY:positionY+componentLength] = np.clip(
            self.page[positionX:positionX+componentHeight, positionY:positionY+componentLength] + component,
            0, 1)
        self.placedPosition = position

        return self.page

    
    def resetParameters(self):
        # defines initial guess
        m0 = np.random.uniform(
                np.array([0, 0, 0]),                                                                                                        # min
                np.array([np.shape(self.page)[0]- np.shape(self.component)[0], np.shape(self.page)[1] - np.shape(self.component)[1], 1])    # max
            )
        
        # CMA-ES
        self.es = cma.CMAEvolutionStrategy(m0, 1.0, {"popsize": self.population})
        