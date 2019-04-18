import numpy as np
import random
from math import inf
        
class Particle:
    """
    Represents a particle of the Particle Swarm Optimization algorithm.
    """
    def __init__(self, lower_bound, upper_bound):
        """
        Creates a particle of the Particle Swarm Optimization algorithm.

        :param lower_bound: lower bound of the particle position.
        :type lower_bound: numpy array.
        :param upper_bound: upper bound of the particle position.
        :type upper_bound: numpy array.
        """
        
        delta = upper_bound - lower_bound
        self.lower_bound = np.copy(lower_bound)
        self.upper_bound = np.copy(upper_bound)

        self.position = np.copy(lower_bound)
        self.velocity = np.copy(lower_bound)
        self.value = -inf

        self.best_position = None
        self.best_value = -inf

        for i in range (len(self.position)):
            self.position[i] = random.uniform(self.lower_bound[i], self.upper_bound[i])
            self.velocity[i] = random.uniform(-delta[i], delta[i])

class ParticleSwarmOptimization:
    """
    Represents the Particle Swarm Optimization algorithm.
    Hyperparameters:
        inertia_weight: inertia weight.
        cognitive_parameter: cognitive parameter.
        social_parameter: social parameter.

    :param hyperparams: hyperparameters used by Particle Swarm Optimization.
    :type hyperparams: Params.
    :param lower_bound: lower bound of particle position.
    :type lower_bound: numpy array.
    :param upper_bound: upper bound of particle position.
    :type upper_bound: numpy array.
    """
    def __init__(self, hyperparams, lower_bound, upper_bound):
        
        self.num_particles = hyperparams.num_particles
        self.inertia_weight = hyperparams.inertia_weight
        self.cognitive_parameter = hyperparams.cognitive_parameter
        self.social_parameter = hyperparams.social_parameter

        self.best_global = None
        self.best_value = -inf
    
        self.particles = [Particle(lower_bound, upper_bound) for _ in range (self.num_particles)]
        self.current_particle_analysis = 0
        
        self.lower_bound = np.copy(lower_bound)
        self.upper_bound = np.copy(upper_bound)

    def get_best_position(self):
        """
        Obtains the best position so far found by the algorithm.

        :return: the best position.
        :rtype: numpy array.
        """

        return self.best_global

    def get_best_value(self):
        """
        Obtains the value of the best position so far found by the algorithm.

        :return: value of the best position.
        :rtype: float.
        """

        return self.best_value

    def get_position_to_evaluate(self):
        """
        Obtains a new position to evaluate.

        :return: position to evaluate.
        :rtype: numpy array.
        """
        
        return self.particles[self.current_particle_analysis % self.num_particles].position

    def advance_generation(self):
        """
        Advances the generation of particles.
        """

        w = self.inertia_weight/(1 + self.current_particle_analysis*0.001)
        cog = self.cognitive_parameter
        soc = self.social_parameter

        cognitive_member = self.lower_bound
        social_member = self.lower_bound

        rc = random.random()
        rg = random.random()

        for particle in  self.particles:
            
            for i in range (len(self.lower_bound)):
                cognitive_member[i] = particle.best_position[i] - particle.position[i]
                social_member[i] = self.best_global[i] - particle.position[i]

            particle.velocity = w*particle.velocity + cog*rc*cognitive_member + soc*rg*social_member
            particle.position = particle.position + particle.velocity

            for i in range (len(self.lower_bound)):
                particle.position[i] = min(max(particle.position[i], particle.lower_bound[i]), particle.upper_bound[i])
                particle.velocity[i] = min(max(particle.velocity[i], particle.lower_bound[i] - particle.upper_bound[i]), particle.upper_bound[i] - particle.lower_bound[i])

    def notify_evaluation(self, value):
        """
        Notifies the algorithm that a particle position evaluation was completed.

        :param value: quality of the particle position.
        :type value: float.
        """
    
        particle_num = self.current_particle_analysis % self.num_particles

        self.particles[particle_num].value = value
        
        if value > self.particles[particle_num].best_value:
            self.particles[particle_num].best_position = self.particles[particle_num].position
            self.particles[particle_num].best_value = value
        
            if value > self.best_value:
                self.best_global = self.particles[particle_num].position
                self.best_value = self.particles[particle_num].value

        self.current_particle_analysis += 1

        if self.current_particle_analysis % self.num_particles == 0:
            self.advance_generation()
