"""
This file contains all constant test parameters which may be altered from this single
location for convenience.
"""

class Parameters:

    # Run Parameters
    stat_runs = 1
    generations = 10  # Number of generations for CCEA in each stat run

    # Domain parameters
    reward_type = 2  # 0 for global, 1 for difference, 2 for d++, 3 for s-d++
    num_rovers = 12  # Number of rovers on map
    num_pois = 10  # Number of POIs on map
    num_steps = 30  # Number of steps rovers take each episode
    min_distance = 1.0  # Minimum distance which may appear in the denominator of credit eval functions
    world_size = 30
    coupling = 3  # Number of rovers required to view a POI for credit
    activation_dist = 4.0  # Minimum distance rovers must be to observe POIs
    n_sectors = 4  # Number of sectors sensor observations are divided into

    # Neural network parameters
    num_inputs = 8
    num_nodes = 9
    num_outputs = 2

    # CCEA parameters
    mutation_rate = 0.1
    epsilon = 0.1
    pop_size = 10