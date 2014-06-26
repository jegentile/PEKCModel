__author__ = 'jgentile'

import population_generators
import agent

class PopulationGenerator:
    def __init__(self,params,model):
        print "Generating Population of type",params['type']
        self.__agents = []

        self.__generator = False

        if(params['type'] == 'proportion'):
            self.__generator = population_generators.ProportionGenerator(params,model)
            self.__agents = self.__generator.get_agents()

        if(params['type'] == 'pareto'):
            self.__generator = population_generators.ParetoGenerator(params,model)
            self.__agents = self.__generator.get_agents()



    def get_agent_list(self):
        return self.__agents
