__author__ = 'jgentile'
import json
import population_generator
import progeny_generator
import bisect

import sys

class Model:
    def __init__(self,parameters,preface,outputfile):
        """
        Instantiates a model class given the path and name of a parameter file. The paramters are provided in JSON
        format. Please refer to the README file for a complete list of parameters.
        """


        # Import the parameter data structure
        print type(parameters)

        if type(parameters) is str:
            print 'string'
            f = open(parameters)
            if not f:
                print 'Error, could not open parameter file:', parameters
            self.__parameters = json.load(f)

        if type(parameters) is dict:
            self.__parameters = parameters

        self.__preface = preface
        self.__output_file = outputfile

        #

        self.__pop_gen = population_generator.PopulationGenerator(self.__parameters['population_generator'],self)
        self.__agents = self.__pop_gen.get_agent_list()
        self.__progeny_generator = progeny_generator.ProgenyGenerator(self.__parameters['progeny_generator'],self)

        # Initialize model attributes
        self.__timestep = 0
        self.__government = 'Autocracy'
        self.__tax_rate = 0
        self.__transfer = 0

        self.__stop = False

        if self.check_assumptions() == False:
            exit()

    def update(self):
        """
        This method is called for every heartbeat of the simulation. The steps are
        1) Update the current agents
        2) Update the regime (decide between autocracy or democracy)
        3) Set the transfer for each agent (amount of benefits distributed by taxes)
        4) For every current agent, make a new agent and pass wealth from parent to progeny
        """


        # 1
        for a in self.__agents:
            a.update()

        # 2
        self.set_regime()

        # 3
        self.set_transfer()

        # 4
        self.__agents = self.__progeny_generator.make_next_generation()



    def run(self):
        """
        Run the simulation starting at timestep zero up to the number of timesteps specified in the parameter
        """
        for i in range(0,self.__parameters['number_of_timesteps']):
            self.__timestep = i
            self.update()
            self.report(i)
            if self.__stop:
                return


    def get_parameter(self,name):
        """
        Returns the value of the parameter with name 'name'.
        """
        return self.__parameters[name]

    def get_tax_rate(self):
        return self.__tax_rate

    def get_agents(self):
        return self.__agents

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
        num_poor = 0

        for i in self.__agents:
         #   print i.get_wealth()



            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
                num_poor += 1
            else:
                rich_wealth += i.get_wealth()

        #if num_poor == 0:
        #    print 'No more poor'
        #    self.__stop = True
        #    return

        sorted_agents_post_tax_income = []
        sorted_agents_wealth = []
        total_income = 0
        poor_agents = []


        for i in self.__agents:
            bisect.insort(sorted_agents_post_tax_income,i.get_post_tax_income())
            bisect.insort(sorted_agents_wealth,i.get_wealth())
            total_income += i.get_post_tax_income()
            if i.get_classification() == 'poor':
                bisect.insort(poor_agents,i.get_post_tax_income())


        if len(sorted_agents_post_tax_income) % 2 == 0:
            #median_income = (sorted_agents_post_tax_income[int(0.5*len(sorted_agents_post_tax_income)/2)]+sorted_agents_post_tax_income[int(0.25*len(sorted_agents_post_tax_income)/2)+1])/2
            median_income = (sorted_agents_post_tax_income[int(len(sorted_agents_post_tax_income)/2)]+sorted_agents_post_tax_income[int(len(sorted_agents_post_tax_income)/2)+1])/2
        else:
            median_income = sorted_agents_post_tax_income[int(len(sorted_agents_post_tax_income)/2)]

        self.__Gini = 0
        index = 1
        number_of_agents = len(self.__agents)

        for i in sorted_agents_post_tax_income:
            self.__Gini += (2*index-number_of_agents-1)*i
            index+=1



        self.__Gini = self.__Gini/(number_of_agents*total_income)

        #self.__inequality = rich_wealth/poor_wealth


        # 2
        #print 'R:',rich_wealth,'P:',poor_wealth
        #inequality = rich_wealth/poor_wealth
        # 3
        if self.__government != 'Democracy':
            richest_poor_agents_income = poor_agents[len(poor_agents)-1]
            mu = self.__parameters['proportion_of_economy_remaining_after_revolution']
            A = self.__parameters['formal_sector_productivity']
            H_t = rich_wealth+poor_wealth
            N_p = len(poor_agents)

            richest_poor_agents_potential = mu*A*H_t/N_p



            if richest_poor_agents_potential > richest_poor_agents_income:
                self.__government = 'Democracy'


        #print "meadian income:",median_income,"average_income",total_income / len(sorted_agents_post_tax_income)

        if self.__government == 'Democracy':
            if median_income > total_income / len(sorted_agents_post_tax_income):
                self.__tax_rate = 0
            else:
                self.__tax_rate = (self.__parameters['formal_sector_productivity']-self.__parameters['informal_sector_productivity'])/self.__parameters['formal_sector_productivity']

        Z = self.__parameters['offspring_human_capital_parameter']
        beta = self.__parameters['offspring_human_capital_exponent']
        gamma = self.__parameters['savings_rate']
        A = self.__parameters['formal_sector_productivity']


        h_ss =(  Z*(gamma*A)**(beta) )**(1/(1-beta))

        """
        if sorted_agents_wealth[len(sorted_agents_wealth)-1] > h_ss:
            print "Error: richest agent's wealth is greater than steady_state"
            print sorted_agents_wealth[len(sorted_agents_wealth)-1],">",h_ss,'is False'
            #exit()
"""


    def report(self,time):
        """
        Reports the time-step information for the simulation given the enumerated timestep (i)
        The output is

        time_step) aggregate_rich_wealth aggregate_poor_wealth government_type
        """


        rich_wealth = 0
        poor_wealth = 0
        num_poor = 0
        num_rich = 0
        for i in self.__agents:
            if i.get_classification() == 'poor':
                poor_wealth += i.get_wealth()
                num_poor += 1
            else:
                rich_wealth += i.get_wealth()
                num_rich += 1

        #print time,') Rich:',rich_wealth,'Poor',poor_wealth,self.__government,'transfer',self.get_transfer()

        self.__output_file.write(self.__preface+','+str(time)+','+str(poor_wealth)+','+str(num_poor)+','+str(rich_wealth)+','+str(num_rich)+','+str(self.__Gini)+','+str(self.__government)+','+str(self.__transfer)+','+str(self.__tax_rate)+'\n')
        #print self.__preface,',',time,',',poor_wealth,',',num_poor,',',rich_wealth,',',num_rich,',',self.__inequality,',',self.__Gini,',',self.__government

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

        if number_of_poor == 0:
            print "No more poor"
            exit()

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





