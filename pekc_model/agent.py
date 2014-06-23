__author__ = 'jgentile'

import math
class Agent:
    def __init__(self,model,classification,wealth,savings_rate):
        self.__classification = classification
        self.__model = model
        self.__wealth = wealth
        self.__savings_rate = savings_rate

    def __repr__(self):
        return self.__classification

    def get_formal_production(self):
        return self.__model.get_parameter("formal_sector_productivity")*self.__wealth

    def update(self):
        if self.__wealth < 1:
            self.__wealth = 1

        self.__gross_income = self.__model.get_parameter("formal_sector_productivity")*self.__wealth
        self.__post_tax_income = (1-self.__model.get_tax_rate())*self.__gross_income+self.__model.get_transfer()

        self.__savings = self.__savings_rate*self.__post_tax_income

        #print 'Agent',self.__classification,self.__gross_income,self.__post_tax_income

    def mate(self):
        pass

    def get_classification(self):
        return self.__classification

    def get_savings(self):
        if self.__savings > 1:
            return self.__savings
        else:
            return 0

    def get_wealth(self):
        return self.__wealth

    def pass_wealth(self):
        return self.__model.get_parameter('offspring_human_capital_parameter')*math.pow(self.__savings,self.__model.get_parameter('offspring_human_capital_exponent'))

