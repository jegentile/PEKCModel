__author__ = 'jgentile'

import random
from pekc_model import agent

class RandomMarriage:
    def __init__(self,params,model):
        self.__preference = params['preference']
        self.__model = model

    def make_next_generation(self):
        agents = self.__model.get_agents()
        random.shuffle(agents)

        rich_males = []
        poor_males = []
        rich_females = []
        poor_females = []

        for i in range(0,len(agents)):
            if i % 2 == 0:
                if agents[i].get_classification() == 'rich':
                    rich_males.append(agents[i])
                else:
                    poor_males.append(agents[i])

            else:
                if agents[i].get_classification() == 'rich':
                    rich_females.append(agents[i])
                else:
                    poor_females.append(agents[i])



        matings = []
        for i in rich_males:
            if len(rich_females):
                if random.random() < self.__preference:
                    matings.append([i,rich_females.pop()])
                else:
                    matings.append([i,poor_females.pop()])
            else:
                matings.append([i,poor_females.pop()])

        for i in poor_males:
            if len(rich_females):
                matings.append([i,rich_females.pop()])
            else:
                if len(poor_females):
                    matings.append([i,poor_females.pop()])

        new_agents = []
        savings_rate = self.__model.get_parameter('savings_rate')

        for i in matings:
            male_wealth = i[0].pass_wealth()
            female_wealth = i[1].pass_wealth()

            poverty_line = 1/(self.__model.get_parameter('savings_rate')*self.__model.get_parameter('formal_sector_productivity'))

            wealth = (male_wealth+female_wealth)/2
            classification = 'rich'
            if wealth < poverty_line:
                classification = 'poor'

            new_agents.append(agent.Agent(
                self.__model,
                classification,
                (male_wealth+female_wealth)/2,
                savings_rate))
            new_agents.append(agent.Agent(
                self.__model,
                classification,
                (male_wealth+female_wealth)/2,
                savings_rate))

        return new_agents



