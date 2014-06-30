__author__ = 'jgentile'


import numpy as np
from pekc_model import agent

class LorenzCurveGenerator:
    def __init__(self,params, model):

        print 'Lorenz Curve generation'

        self.__delta = float(params['delta'])
        self.__total_wealth = float(params['total_wealth'])

        self.__agents = []
        self.__model = model
        number_of_agents = params['number_of_agents']


        #r = np.random.pareto(self.__a, number_of_agents) + self.__m
        savings_rate = self.__model.get_parameter('savings_rate')

        poverty_line = 1/(self.__model.get_parameter('savings_rate')*self.__model.get_parameter('formal_sector_productivity'))

        for i in range(0,number_of_agents):
            N = float(number_of_agents)
            d = self.__delta
            wealth = self.__total_wealth*((1-float(i-1)/N)**d-(1-float(i)/N)**d)

            if wealth < poverty_line:
                self.__agents.append(agent.Agent(model,'poor',wealth,savings_rate))
            else:
                self.__agents.append(agent.Agent(model,'rich',wealth,savings_rate))



        #print self.__agents



    def get_agents(self):
        return self.__agents
