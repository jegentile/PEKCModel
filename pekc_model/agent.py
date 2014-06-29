__author__ = 'jgentile'

import math
class Agent:
    def __init__(self,model,classification,wealth,savings_rate):
        """
        Constructor for the model's agent given the model, classification (rich/poor), wealth, and savings rate
        """
        if wealth < 0.1:
            print "Error: Agent instantiated with welath < 1."
            exit()

            
        self.__classification = classification
        self.__model = model
        self.__wealth = wealth
        self.__savings_rate = savings_rate

    def __repr__(self):
        # Printer operator
        return '['+str(self.__classification)+','+str(self.__wealth)+']'

    def get_formal_production(self):
        # Returns the formal production as the productivity times the agent's wealth
        return self.__model.get_parameter("formal_sector_productivity")*self.__wealth

    def update(self):
        """
        Update an agent for the timestep by
        1) Setting the wealth constraint
        2) Calculate gross income as formal sectory productivity times __wealth
        3) Calculate the post-tax income as one minus the tax rate times gross income plus the transfer received by the gov't
        4) Calculate the savings as post-tax income time the savings rate
        5) Impose a saving's cponstraint
        """
        # 1
        if self.__wealth < 1:
            self.__wealth = 1
            # 2
        self.__gross_income = self.__model.get_parameter("formal_sector_productivity")*self.__wealth
        # 3
        self.__post_tax_income = (1-self.__model.get_tax_rate())*self.__gross_income+self.__model.get_transfer()
        # 4
        self.__savings = self.__savings_rate*self.__post_tax_income
        # 5
        if self.__savings <= 1:
            self.__savings = 0

            #print 'Agent',self.__classification,self.__gross_income,self.__post_tax_income

    def get_post_tax_income(self):
        return self.__post_tax_income

    def mate(self):
        """
        Placeholder function for agent reproduction
        """
        pass

    def get_classification(self):
        """
        Returns the classification of agents (rich or poor)
        """
        return self.__classification

    def get_savings(self):
        # Returns the agent's savings
        return self.__savings

    def get_wealth(self):
        # Return's agent wealth
        return self.__wealth

    def pass_wealth(self):
        # Returns wealth that is passed to progeny.

        pass_on_wealth = self.__model.get_parameter('offspring_human_capital_parameter')*math.pow(self.__savings,self.__model.get_parameter('offspring_human_capital_exponent'))


        if pass_on_wealth < 1:
            return 1
        else:
            return pass_on_wealth

    def __ge__(self, other):
        return self.get_wealth() >= other.get_wealth()

    def __le__(self, other):
        return self.get_wealth() <= other.get_wealth()

    def __eq__(self, other):
        return self.get_wealth() == other.get_wealth()
