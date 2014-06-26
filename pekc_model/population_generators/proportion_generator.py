__author__ = 'jgentile'

from pekc_model import agent

class ProportionGenerator:
    def __init__(self,params,model):


        self.__agents = []

        self.__number_of_agents = params['number_of_agents']
        self.__proportion_of_rich_agents = params['initial_proportion_of_rich_agents']

        self.__number_of_rich_agents = round(self.__number_of_agents*self.__proportion_of_rich_agents)

        number_of_agents = int(params['number_of_agents'])
        number_of_rich_agents = int(round(number_of_agents*params['initial_proportion_of_rich_agents']))

        rich_wealth = params['rich_wealth']
        poor_wealth = params['poor_wealth']
        savings_rate = model.get_parameter('savings_rate')


        for i in range(0,number_of_agents):
            if i < number_of_rich_agents:
                self.__agents.append(agent.Agent(model,'rich',rich_wealth,savings_rate))
            else:
                self.__agents.append(agent.Agent(model,'poor',poor_wealth,savings_rate))

        print self.__agents



    def get_agents(self):
        return self.__agents

