PEKCModel
=========

This is a Python implementation of the model described in 'The Political Economy of the Kuznets Curve'. Parameters are
in parameters.json. 

To execute, the command is: python main.py parameters.json

Parameters
==========

The model is parameterized with an object described in a JSON file. This section outlines the required fields and their meaning.


- number_of_timesteps - the number of discrete timesteps in the simulation
- formal_sector_productivity - the formal market productivity for a given timestep (A)
- informal_sector_productivity - the informal market productivity for a given timestep (B)
- savings_rate - agent savings rate as a proportion of capital (gamma)
- offspring_human_capital_parameter - parameter for next-generation human capital (Z)
- offspring_human_capital_exponent - exponent for next-generation human capital (beta)
- proportion_of_economy_remaining_after_revolution- the proportion of the economy that exists after a revolution (mu)
- population_generator - object that describes the population for the given simulation
- progenty_generator - object describing how wealth is passed from one generation to the next


Population Generation
----------------

The population can be generated from one of any population generator

1) Proportional population generator (type = 'proportion') generates a two-class population given a total number and proportion
of rich agents
- type = 'proportion'
- number_of_agents - the total number of agents
- initial_proportion_of_rich_agents - proportion of rich agents (lambda)
- rich_wealth - initial wealth of the rich (h^r)
- poor_wealth - initial wealth of the poor (h^p)


Progeny Generation
------------------

These objects describe how wealth is passed from one generation to another

1) One-to-one progeny generator (type = 'one_to_one') is where one parent passes all its wealth to one progeny
- type = 'one_to_one'