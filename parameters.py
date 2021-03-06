parameters = {}

# Run Parameters
parameters["stat_runs"] = 1
parameters["generations"] = 2000  # Number of generations for CCEA in each stat run
parameters["new_world_config"] = 0  # 0 = False -> Reuse existing world config, 1 = True -> Use new world config
parameters["n_suggestions"] = 2  # Number of suggestions a rover should learn

# Visualizer
parameters["vis_running"] = False  # True keeps visualizer from closing until you 'X' out of window

# Domain parameters
parameters["n_rovers"] = 3  # Number of rovers on map
parameters["coupling"] = 3  # Number of rovers required to view a POI for credit
parameters["n_poi"] = 2  # Number of POIs on map
parameters["n_steps"] = 30  # Number of steps rovers take each episode
parameters["min_distance"] = 1.0  # Minimum distance which may appear in the denominator of credit eval functions
parameters["x_dim"] = 40.0  # X-Dimension of the rover map
parameters["y_dim"] = 40.0  # Y-Dimension of the rover map
parameters["obs_rad"] = 4.0  # Minimum distance rovers must be to observe POIs

# Rover Parameters
parameters["sensor_model"] = "summed"  # Should either be "density" or "closest" or "summed"
parameters["ctrl_type"] = "GRU"  # NN or GRU
parameters["angle_res"] = 90  # Resolution of sensors (determines number of sectors)

# Neural network parameters
parameters["n_inputs"] = 8
parameters["n_hnodes"] = 12
parameters["n_outputs"] = 2
parameters["mem_block_size"] = 12

# CCEA parameters
parameters["pop_size"] = 60
parameters["mut_prob"] = 0.1  # Probability that a mutation will occur
parameters["mut_rate"] = 0.1  # How much a weight is allowed to change
parameters["epsilon"] = 0.1  # For e-greedy selection in CCEA
parameters["n_elites"] = 3
