__author__ = 'jgentile'

import random
from pekc_model import agent

class AssortativeMating:
    def __init__(self,params,model):
        self.__preference = params['preference']
        self.__model = model

    def make_next_generation(self):
        agents = self.__model.get_agents()
        random.shuffle(agents)

        rich_agents = []
        poor_agents = []

        for i in agents:
            if i.get_classification() == 'rich':
                rich_agents.append(i)
            else:
                poor_agents.append(i)

        matings = []

        while len(rich_agents) or len(poor_agents):
            if len(poor_agents):
                ratio = len(rich_agents)/len(poor_agents)
            else:
                ratio = 1.1

            if random.random() < ratio: # pick poor agent
                a = rich_agents.pop()
                if random.random() < self.__preference:
                    if len(rich_agents):
                        mate = rich_agents.pop()
                    else:
                        mate = poor_agents.pop()
                else:
                    # If the agent has no preference, randomly draw a mate as rich or poor
                    
                    if len(poor_agents):
                        draw = len(rich_agents)/len(poor_agents)
                    else:
                        draw = 1.1

                    if random.random() < draw:
                        mate = rich_agents.pop()
                    else:
                        mate = poor_agents.pop()

            else:
                a = poor_agents.pop()
                if random.random() < self.__preference:
                    if len(poor_agents):
                        mate = poor_agents.pop()
                    else:
                        mate = rich_agents.pop()
                else:
                    # If the agent has no preference, randomly draw a mate as rich or poor
                    if len(poor_agents):
                        draw = len(rich_agents)/len(poor_agents)
                    else:
                        draw = 1.1

                    if random.random() < draw:
                        mate = rich_agents.pop()
                    else:
                        mate = poor_agents.pop()



            matings.append([a,mate])


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



