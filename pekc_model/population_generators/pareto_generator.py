__author__ = 'jgentile'


import numpy as np
from pekc_model import agent

class ParetoGenerator:
    def __init__(self,params, model):

        print 'Pareto generation'

        self.__a = float(params['dist_a'])
        self.__m = float(params['dist_m'])

        self.__agents = []
        self.__model = model
        number_of_agents = params['number_of_agents']


        r = np.random.pareto(self.__a, number_of_agents) + self.__m
        savings_rate = self.__model.get_parameter('savings_rate')

        poverty_line = 1/(self.__model.get_parameter('savings_rate')*self.__model.get_parameter('formal_sector_productivity'))

        ''

        for i in range(0,number_of_agents):
            wealth = r[i]
            if wealth < poverty_line:
                self.__agents.append(agent.Agent(model,'poor',wealth,savings_rate))
            else:
                self.__agents.append(agent.Agent(model,'rich',wealth,savings_rate))

        print self.__agents

    def get_agents(self):
        return self.__agents
