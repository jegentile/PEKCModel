__author__ = 'jgentile'
import json
import population_generator

import agent

class Model:
    def __init__(self,parameter_filename):
        """
        Instantiates a model class given the path and name of a parameter file. The paramters are provided in JSON
        format. Please refer to the README file for a complete list of parameters.
        """

        # Import the parameter data structure
        f = open(parameter_filename)
        if not f:
            print 'Error, could not open parameter file:', parameter_filename

        #
        self.__parameters = json.load(f)
        self.__pop_gen = population_generator.PopulationGenerator(self.__parameters['population_generator'],self)
        self.__agents = self.__pop_gen.get_agent_list()

        # Initialize model attributes
        self.__timestep = 0
        self.__government = 'Autocracy'
        self.__tax_rate = 0

    def update(self):
        """
        This method is called for every heartbeat of the simulation. The steps are
        1) Update the regime (decide between autocracy or democracy)
        2) Set the transfer for each agent (amount of benefits distributed by taxes)
        3) Update the current agents
        4) For every current agent, make a new agent and pass wealth from parent to progeny
        """

        # 1
        self.set_regime()

        # 2
        self.set_transfer()
        new_agents = []

        # 3
        for a in self.__agents:
            a.update()

        # 4
        savings_rate = self.__parameters['savings_rate']
        number_of_agents = len(self.__agents)
        for i in range(0,number_of_agents):
            new_agents.append(agent.Agent(
                self,
                self.__agents[i].get_classification(),
                self.__agents[i].pass_wealth(),
                savings_rate))
        self.__agents = new_agents




    def run(self):
        """
        Run the simulation starting at timestep zero up to the number of timesteps specified in the parameter
        """
        for i in range(0,self.__parameters['number_of_timesteps']):
            self.update()
            self.report(i)


    def get_parameter(self,name):
        """
        Returns the value of the parameter with name 'name'.
        """
        return self.__parameters[name]

    def get_tax_rate(self):
        return self.__tax_rate

    def get_transfer(self):
        return self.__transfer

    def set_transfer(self):
        """
        Calculates the agent-wise transfer by gathering taxes and calculating a per-agent share of the transfer
        """

        total_formal_production = 0
        # For every agent, get its formal production
        for i in self.__agents:
            total_formal_production += i.get_formal_production()

        # Calculate the transfer as the tax rate times total formal production divided by the number of agents
        self.__transfer = self.__tax_rate*total_formal_production/len(self.__agents)


    def set_regime(self):
        """
        Determine the regime (autocracy of democracy) for this timestep by
        1) Calculate the rich and poor wealth
        2) Calculate inequality by dividing the rich's wealth by the poor's wealth
        3) Calculate the revolution constraint
        3) Determine if inequality is greater than the revolution constraint. If it is, set the government and tax rate
        """

        # 1
        rich_wealth = 0
        poor_wealth = 0
        for i in self.__agents:
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
            else:
                rich_wealth += i.get_wealth()
        # 2
        inequality = rich_wealth/poor_wealth
        # 3
        revolution_constraint = (1-self.__parameters['proportion_of_economy_remaining_after_revolution'])/self.__parameters['proportion_of_economy_remaining_after_revolution']
        # 4
        if inequality > revolution_constraint:
            self.__government = 'Democracy'
            self.__tax_rate = (self.__parameters['formal_sector_productivity']-self.__parameters['informal_sector_productivity'])/self.__parameters['formal_sector_productivity']


    def report(self,time):
        """
        Reports the time-step information for the simulation given the enumerated timestep (i)
        The output is

        time_step) aggregate_rich_wealth aggregate_poor_wealth government_type
        """

        rich_wealth = 0
        poor_wealth = 0
        for i in self.__agents:
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
            else:
                rich_wealth += i.get_wealth()

        print time,') Rich:',rich_wealth,'Poor',poor_wealth,self.__government





