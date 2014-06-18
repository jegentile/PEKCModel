__author__ = 'jgentile'
import json

import agent

class Model:
    def __init__(self,parameter_filename):
        self.__timestep = 0

        f = open(parameter_filename)
        if not f:
            print 'Error, could not open parameter file:', parameter_filename

        self.__parameters = json.load(f)
        print self.__parameters['number_of_agents']

        self.initialize_model()

        self.__government = 'Autocracy'
        self.__tax_rate = 0


    def initialize_model(self):
        self.__agents = []
        number_of_agents = int(self.__parameters['number_of_agents'])
        number_of_rich_agents = int(round(number_of_agents*self.__parameters['initial_proportion_of_rich_agents']))
        
        rich_wealth = self.__parameters['rich_wealth']
        poor_wealth = self.__parameters['poor_wealth']
        savings_rate = self.__parameters['savings_rate']


        for i in range(0,number_of_agents):
            if i < number_of_rich_agents:
                self.__agents.append(agent.Agent(self,'rich',rich_wealth,savings_rate))
            else:
                self.__agents.append(agent.Agent(self,'poor',poor_wealth,savings_rate))

        print self.__agents

    def update(self):

        self.set_regime()

        self.set_transfer()
        new_agents = []

        for a in self.__agents:
            a.update()

        savings_rate = self.__parameters['savings_rate']

        for i in range(0,self.__parameters['number_of_agents']):
            new_agents.append(agent.Agent(
                self,
                self.__agents[i].get_classification(),
                self.__agents[i].pass_wealth(),
                savings_rate))
        self.__agents = new_agents




    def run(self):
        for i in range(0,self.__parameters['number_of_timesteps']):
            self.update()
            self.report(i)


    def get_parameter(self,name):
        return self.__parameters[name]

    def get_tax_rate(self):
        return self.__tax_rate

    def get_transfer(self):
        return self.__transfer

    def set_transfer(self):

        total_formal_production = 0
        for i in self.__agents:
            total_formal_production += i.get_formal_production()

        self.__transfer = self.__tax_rate*total_formal_production/len(self.__agents)


    def set_regime(self):

        rich_wealth = 0
        poor_wealth = 0
        for i in self.__agents:
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
            else:
                rich_wealth += i.get_wealth()

        inequality = rich_wealth/poor_wealth
        revolution_constraint = (1-self.__parameters['proportion_of_economy_remaining_after_revolution'])/self.__parameters['proportion_of_economy_remaining_after_revolution']

        if inequality > revolution_constraint:
            self.__government = 'Democracy'
            self.__tax_rate = (self.__parameters['formal_sector_productivity']-self.__parameters['informal_sector_productivity'])/self.__parameters['formal_sector_productivity']


    def report(self,time):
        rich_wealth = 0
        poor_wealth = 0
        for i in self.__agents:
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
            else:
                rich_wealth += i.get_wealth()

        print time,') Rich:',rich_wealth,'Poor',poor_wealth,self.__government





