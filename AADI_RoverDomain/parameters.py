import yaml


class Parameters:

    def __init__(self):
        # Run Parameters
        self.stat_runs = 10
        self.generations = 100  # Number of generations for CCEA in each stat run
        self.new_world_config = False  # False -> Reuse existing world config, True -> Use new world config
        self.reward_type = "DPP"  # Switch between reward functions "Global" "Difference" "DPP" "SDPP"

        # Visualizer
        self.running = False  # True keeps visualizer from closing until you 'X' out of window

        # Domain parameters
        self.num_rovers = 14  # Number of rovers on map (GETS MULTIPLIED BY NUMBER OF TYPES)
        self.coupling = 3  # Number of rovers required to view a POI for credit
        self.num_pois = 12  # Number of POIs on map
        self.num_steps = 20  # Number of steps rovers take each episode
        self.min_distance = 1.0  # Minimum distance which may appear in the denominator of credit eval functions
        self.x_dim = 30  # X-Dimension of the rover map
        self.y_dim = 30  # Y-Dimension of the rover map
        self.min_observation_dist = 2.0  # Minimum distance rovers must be to observe POIs
        self.angle_resolution = 90  # Resolution of sensors (determines number of sectors)
        self.sensor_model = "summed"  # Should either be "density" or "closest" or "summed"

        # Neural network parameters
        self.num_inputs = 8
        self.num_nodes = 9
        self.num_outputs = 2

        # CCEA parameters
        self.mutation_prob = 0.1  # Probability that a member of the offspring population will be mutated
        self.mutation_rate = 0.01  # Percentage of bits which get flipped in an individual
        self.epsilon = 0.1  # For e-greedy selection in CCEA
        self.parent_pop_size = 20
        self.offspring_pop_size = 20

        # User specific parameters
        """
        Suggestions: high_val, low_val, high_low, val_based, partner_prox, or none (none is standard D++)_
        """
        self.suggestion_type = "none"
        self.new_suggestion = "high_val"
        self.gen_switch_point = 499  # What generation should the suggestion type switch at?
        self.step_switch_point = 8  # What step should the suggestion type switch at?
        self.gen_suggestion_switch = False  # Switch suggestion types at a specified generation
        self.step_suggestion_switch = False  # Switch suggestion types at a specified rover step

    def load_yaml(self, filename):
        """
        loads a set of parameters into this object with setattr
        Does not require that all parameters are set, i.e. you can optionally set a specific set of parameters
        :param filename:
        :return:
        """
        with open(file=filename) as f:
            params = yaml.load(f)
        for key in params:
            setattr(self, key, params[key])

    def save_yaml(self, filename):
        """
        Saves ALL the parameters into a yaml file, not just the optionally set ones
        :param filename:
        :return:
        """
        with open(file=filename, mode='w') as f:
            yaml.dump(vars(self), f)


if __name__ == '__main__':
    with open("/tmp/param_tests.yaml", 'w') as f:
        f.write("""
            test_a: 10
            stat_runs: 100
            """)
    parameters = Parameters()
    print("Before load")
    print(parameters.stat_runs)
    parameters.load_yaml("/tmp/param_tests.yaml")
    print("After load")
    print(parameters.test_a)
    print(parameters.stat_runs)
    parameters.save_yaml("/tmp/param_tests_out.yaml")
