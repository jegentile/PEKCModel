__author__ = 'jgentile'

import pekc_model.agent as agent

class OneToOne:
    def __init__(self,params,model):
        self.__model = model

    def make_next_generation(self):
        new_agents = []
        agents = self.__model.get_agents()

        savings_rate = self.__model.get_parameter('savings_rate')
        number_of_agents = len(agents)
        poverty_line = 1/(self.__model.get_parameter('savings_rate')*self.__model.get_parameter('formal_sector_productivity'))

        for i in range(0,number_of_agents):

            wealth = agents[i].pass_wealth()
            classification = 'rich'
            if wealth < poverty_line:
                classification = 'poor'

            new_agents.append(agent.Agent(
                self.__model,
                classification,
                wealth,
                savings_rate))

        return new_agents


