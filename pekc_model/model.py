__author__ = 'jgentile'
import json
import population_generator

import agent
import sys

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

        if self.check_assumptions() == False:
            exit()

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
         #   print i.get_wealth()
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
            else:
                rich_wealth += i.get_wealth()
        # 2
        #print 'R:',rich_wealth,'P:',poor_wealth
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

        print time,') Rich:',rich_wealth,'Poor',poor_wealth,self.__government,'transfer',self.get_transfer()


    def check_assumptions(self):
        params = self.__parameters
        contradiction_is_present = False

        number_of_rich = 0;
        number_of_poor = 0;

        minimum_rich = sys.maxint
        maximum_poor = 0

        for i in self.__agents:
            if i.get_classification() == 'rich':
                number_of_rich +=1
                if i.get_wealth() < minimum_rich:
                    minimum_rich = i.get_wealth()
            if i.get_classification() == 'poor':
                number_of_poor +=1
                if i.get_wealth() > maximum_poor:
                    maximum_poor = i.get_wealth()

        if number_of_rich > number_of_poor:
            print 'Error: Rich outnumber the poor:'
            print '\tNumber_of_rich < Number_of_poor'
            print  '\t',number_of_rich, '<', number_of_poor,'is False'
            contradiction_is_present = True

        number_of_poor = float(number_of_poor)
        number_of_rich = float(number_of_rich)

        if number_of_poor/(number_of_rich+number_of_poor) < 0.5:
            print 'Error: Median agent is not poor:'
            print '\tnumber_of_poor/(number_of_rich+number_of_poor)'
            print  '\t',number_of_poor/(number_of_rich+number_of_poor), '> 0.5 is False'
            contradiction_is_present = True

        if maximum_poor > minimum_rich:
            print 'Error: Poorest rich agent is poorer than richest poor agent:'
            print '\t maximum_poor < minimum_rich'
            print  '\t',maximum_poor, '<' ,minimum_rich,'is False'
            contradiction_is_present = True

        if params['savings_rate'] > 1 or params['savings_rate']<0:
            print 'Error: savings_rate must be between zero and 1:'
            print '\t 0 <= savings_rate <=1'
            print  '\t','0 <=',params['savings_rate'],' <= 1 is False'
            contradiction_is_present = True

        if params['proportion_of_economy_remaining_after_revolution'] > 1 or params['proportion_of_economy_remaining_after_revolution']<0:
            print 'Error: savings_rate must be between zero and 1:'
            print '\t 0 <= proportion_of_economy_remaining_after_revolution <=1'
            print  '\t','0 <=',params['proportion_of_economy_remaining_after_revolution'],' <= 1 is False'
            contradiction_is_present = True

        if params['offspring_human_capital_parameter'] <= 1:
            print 'Error: offspring_human_capital_parameter must be greater than one'
            print '\toffspring_human_capital_parameter > 1'
            print  '\t',params['offspring_human_capital_parameter'],' > 1 is False'
            contradiction_is_present = True

        if params['offspring_human_capital_exponent'] >= 1:
            print 'Error: offspring_human_capital_exponent must be less than one:'
            print '\t offspring_human_capital_exponent < 1'
            print  '\t',params['offspring_human_capital_exponent'],' < 1 is False'
            contradiction_is_present = True

        if number_of_rich < 1:
            print 'Error: There must be at least one rich agent:'
            print '\tNumber_of_rich >= 1'
            print  '\t',number_of_rich, '>= 1 is False'
            contradiction_is_present = True

        # Formal sector > Informal Sector
        if params['formal_sector_productivity'] < params['informal_sector_productivity']:
            print 'Error: Parameters are in violation of the formal sector assumption:'
            print '\tformal_sector_productivity > informal_sector_productivity'
            print  '\t',params['formal_sector_productivity'], '<', params['informal_sector_productivity'],'is False'
            contradiction_is_present = True

        # Zero bequest assumption:
        if params['savings_rate']*params['formal_sector_productivity'] > 1:
            print 'Error: Parameters are in violation of the zero-bequest assumption:'
            print '\tsavings_rate * formal_sector_productivity < 1'
            print  '\t',params['savings_rate']*params['formal_sector_productivity'],'< 1 is False'
            contradiction_is_present = True

        # Steady-state assumption
        if (params['savings_rate']*params['informal_sector_productivity'])**(params['offspring_human_capital_exponent'])*params['offspring_human_capital_parameter'] < 1:
            print 'Error: Parameters are in violation of the stead-state assumption:'
            print '\toffspring_human_capital_parameter*(savings_rate*informal_sector_productivity)^offspring_human_capital_exponent > 1'
            print  '\t',(params['savings_rate']*params['informal_sector_productivity'])**(params['offspring_human_capital_exponent'])*params['offspring_human_capital_parameter'],'> 1 is False'
            contradiction_is_present = True


        # Initial conditions
        rich_wealth = 0
        for i in self.__agents:
            if i.get_classification() == 'rich':
                rich_wealth = i.get_wealth()
                if rich_wealth < 1/(params['savings_rate']*params['formal_sector_productivity']):
                    print 'Error: Parameters are in violation of the initial conditions assumption for agent',i,':'
                    print '\t sum(rich_wealth) > 1/(savings_rate*formal_sector_productivity)'
                    print  '\t',rich_wealth,'>', 1/(params['savings_rate']*params['formal_sector_productivity']),' is False'
                    contradiction_is_present = True


        if contradiction_is_present:
            return False
        else:
            return True




