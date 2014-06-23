PEKCModel
=========

This is a Python implementation of the model described in 'The Political Economy of the Kuznets Curve'. Paramters are
in parameters.json. 

To execute, the command is: python main.py parameters.json

Parameters
-------------

The model is parameterized with an object described in a JSON file. This section outlines the required fields and their meaning.


- number_of_timesteps - the number of discrete timesteps in the simulation
- formal_sector_productivity - The formal market productivity for a given timestep (A)
- informal_sector_productivity - The informal market productivity for a given timestep (B)
- savings_rate - Agent savings rate as a proportion of capital (gamma)
- offspring_human_capital_parameter - Parameter for next-generation human capital (Z)
- offspring_human_capital_exponent - Exponent for next-generation human capital (beta)
- proportion_of_economy_remaining_after_revolution- The proportion of the economy that exists after a revolution
- population_generator - object that describes the population for the given simulation

