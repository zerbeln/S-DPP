import numpy as np
import math
from AADI_RoverDomain.parameters import Parameters as p
from Python_Code.suggestions import *

# GLOBAL REWARDS ------------------------------------------------------------------------------------------------------
def calc_global_alpha(rover_paths, poi_values, poi_positions):
    total_steps = p.num_steps + 1
    inf = 1000.00
    global_reward = 0.0

    poi_observer_distances = np.zeros((p.num_pois, total_steps))
    for poi_id in range(p.num_pois):
        for step_index in range(total_steps):
            observer_count = 0
            rover_distances = np.zeros(p.num_rovers)

            for agent_id in range(p.num_rovers):
                # Calculate distance between agent and POI
                x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, agent_id, 0]
                y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, agent_id, 1]
                distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                if distance < p.min_distance:
                    distance = p.min_distance

                rover_distances[agent_id] = distance

                # Check if agent observes poi and update observer count if true
                if distance < p.min_observation_dist:
                    observer_count += 1

            # Update global reward if POI is observed
            if observer_count >= p.coupling:
                summed_observer_distances = 0.0
                for observer in range(p.coupling):
                    # assert(min(rover_distances) < p.min_observation_dist)
                    summed_observer_distances += min(rover_distances)
                    od_index = np.argmin(rover_distances)
                    rover_distances[od_index] = inf
                poi_observer_distances[poi_id, step_index] = summed_observer_distances
            else:
                poi_observer_distances[poi_id, step_index] = inf

    for poi_id in range(p.num_pois):
        if (min(poi_observer_distances[poi_id])/p.coupling) < p.min_observation_dist:
            global_reward += poi_values[poi_id]/((1/p.coupling)*min(poi_observer_distances[poi_id]))

    return global_reward



# DIFFERENCE REWARDS --------------------------------------------------------------------------------------------------
# def calc_difference(rover_paths, poi_values, poi_positions, global_reward):
#     number_agents = p.num_rovers
#     number_pois = p.num_pois
#     min_obs_distance = p.min_observation_dist
#     total_steps = p.num_steps + 1
#     inf = 1000.00
#
#     difference_rewards = np.zeros(number_agents)
#
#     for agent_id in range(number_agents):
#         for step_index in range(total_steps):
#
#             counterfactual_global_reward = 0.0
#             temp_difference_reward = 0.0
#
#             for poi_id in range(number_pois):
#                 # Count how many agents observe poi, update closest distance if necessary
#                 observer_count = 0
#                 observer_distances = np.zeros(number_agents)
#                 summed_observer_distances = 0.0
#
#                 for other_agent_id in range(number_agents):
#
#                     if agent_id != other_agent_id:  # Ignore self (Null Action)
#                         # Calculate separation distance between poi and agent
#                         x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
#                         y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
#                         distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
#
#                         if distance < p.min_distance:
#                             distance = p.min_distance
#
#                         observer_distances[other_agent_id] = distance
#
#                         # Check if agent observes poi
#                         if distance < min_obs_distance:
#                             observer_count += 1
#                     else:
#                         observer_distances[other_agent_id] = inf  # Ignore self
#
#                 # Update reward if coupling is satisfied
#                 if observer_count >= p.coupling:
#                     for observer_id in range(p.coupling):
#                         summed_observer_distances += min(observer_distances)
#                         od_index = np.argmin(observer_distances)
#                         observer_distances[od_index] = inf
#                     counterfactual_global_reward += poi_values[poi_id] / ((1/p.coupling)*summed_observer_distances)
#
#             temp_difference_reward = global_reward - counterfactual_global_reward
#
#             if temp_difference_reward > difference_rewards[agent_id]:
#                 difference_rewards[agent_id] = temp_difference_reward
#
#     return difference_rewards

def calc_difference_alpha(rover_paths, poi_values, poi_positions, global_reward):
    min_obs_distance = p.min_observation_dist
    total_steps = p.num_steps + 1
    inf = 1000.00

    difference_rewards = np.zeros(p.num_rovers)

    for agent_id in range(p.num_rovers):  # For each rover
        poi_observer_distances = np.zeros((p.num_pois, total_steps))  # Tracks summed observer distances

        for poi_id in range(p.num_pois):  # For each POI
            for step_index in range(total_steps):  # For each step in trajectory
                observer_count = 0
                rover_distances = np.zeros(p.num_rovers)  # Track distances between rovers and POI

                # Count how many agents observe poi, update closest distances
                for other_agent_id in range(p.num_rovers):
                    if agent_id != other_agent_id:  # Remove current rover's trajectory
                        # Calculate separation distance between poi and agent
                        x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
                        y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
                        distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                        if distance < p.min_distance:
                            distance = p.min_distance

                        rover_distances[other_agent_id] = distance

                        # Check if agent observes poi
                        if distance < min_obs_distance:
                            observer_count += 1
                    else:
                        rover_distances[agent_id] = inf  # Ignore self

                # Determine if coupling is satisfied
                if observer_count >= p.coupling:
                    summed_observer_distances = 0.0
                    for observer in range(p.coupling):
                        # assert(min(rover_distances) < p.min_observation_dist)
                        summed_observer_distances += min(rover_distances)
                        od_index = np.argmin(rover_distances)
                        rover_distances[od_index] = inf
                    poi_observer_distances[poi_id, step_index] = summed_observer_distances
                else:
                    poi_observer_distances[poi_id, step_index] = inf

        counterfactual_global_reward = 0.0
        for poi_id in range(p.num_pois):
            if (min(poi_observer_distances[poi_id])/p.coupling) < p.min_observation_dist:
                counterfactual_global_reward += poi_values[poi_id] / ((1/p.coupling)*min(poi_observer_distances[poi_id]))
        difference_rewards[agent_id] = global_reward - counterfactual_global_reward

    return difference_rewards


# D++ REWARD ----------------------------------------------------------------------------------------------------------
# def calc_dpp(rover_paths, poi_values, poi_positions, global_reward):
#     number_agents = p.num_rovers
#     number_pois = p.num_pois
#     min_obs_distance = p.min_observation_dist
#     total_steps = p.num_steps + 1
#     inf = 1000.00
#
#     difference_rewards = calc_difference(rover_paths, poi_values, poi_positions, global_reward)
#     dpp_rewards = np.zeros(number_agents)
#
#     # Calculate Dpp Reward with (TotalAgents - 1) Counterfactuals
#     n_counters = p.coupling-1
#     for agent_id in range(number_agents):
#         for step_index in range(total_steps):
#             counterfactual_global_reward = 0.0
#
#             for poi_id in range(number_pois):
#
#                 # Count how many agents observe poi, update closest distance if necessary
#                 observer_count = 0
#                 summed_observer_distances = 0.0
#                 observer_distances = np.zeros(number_agents)
#
#                 for other_agent_id in range(number_agents):
#                     # Calculate separation distance between poi and agent
#                     x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
#                     y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
#                     distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
#
#                     if distance < p.min_distance:
#                         distance = p.min_distance
#
#                     observer_distances[other_agent_id] = distance
#
#                     if distance < min_obs_distance:
#                         observer_count += 1
#
#                 # Add in counterfactual partners
#                 for partner_id in range(n_counters):
#                     np.append(observer_distances, observer_distances[agent_id])
#                     if observer_distances[agent_id] < min_obs_distance:
#                         observer_count += 1
#
#                 # update closest distance only if poi is observed
#                 if observer_count >= p.coupling:
#                     for observer_id in range(p.coupling):
#                         summed_observer_distances += min(observer_distances)
#                         od_index = np.argmin(observer_distances)
#                         observer_distances[od_index] = inf
#                     counterfactual_global_reward += poi_values[poi_id] / ((1/p.coupling) * summed_observer_distances)
#
#             temp_dpp_reward = (counterfactual_global_reward - global_reward) / (1 + n_counters)
#
#             if temp_dpp_reward > dpp_rewards[agent_id]:
#                 dpp_rewards[agent_id] = temp_dpp_reward
#
#     for agent_id in range(number_agents):
#
#         if dpp_rewards[agent_id] > difference_rewards[agent_id]:
#             for step_index in range(total_steps):
#                 for n_counters in range(p.coupling-1):
#
#                     counterfactual_global_reward = 0.0
#
#                     for poi_id in range(number_pois):
#
#                         # Count how many agents observe poi, update closest distance if necessary
#                         observer_count = 0
#                         summed_observer_distances = 0.0
#                         observer_distances = np.zeros(number_agents)
#
#                         for other_agent_id in range(number_agents):
#                             # Calculate separation distance between poi and agent
#                             x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
#                             y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
#                             distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
#
#                             if distance < p.min_distance:
#                                 distance = p.min_distance
#
#                             observer_distances[other_agent_id] = distance
#
#                             if distance < min_obs_distance:
#                                 observer_count += 1
#
#                         # Add in counterfactual partners
#                         for partner_id in range(n_counters):
#                             np.append(observer_distances, observer_distances[agent_id])
#                             if observer_distances[agent_id] < min_obs_distance:
#                                 observer_count += 1
#
#                         # update closest distance only if poi is observed
#                         if observer_count >= p.coupling:
#                             for observer_id in range(p.coupling):
#                                 summed_observer_distances += min(observer_distances)
#                                 od_index = np.argmin(observer_distances)
#                                 observer_distances[od_index] = inf
#                             counterfactual_global_reward += poi_values[poi_id] / ((1/p.coupling) * summed_observer_distances)
#
#                     temp_dpp_reward = (counterfactual_global_reward - global_reward)/(1 + n_counters)
#
#                     if dpp_rewards[agent_id] < temp_dpp_reward:
#                         dpp_rewards[agent_id] = temp_dpp_reward
#         else:
#             dpp_rewards[agent_id] = difference_rewards[agent_id]  # Returns difference reward
#
#     return dpp_rewards

def calc_dpp_alpha(rover_paths, poi_values, poi_positions, global_reward):
    min_obs_distance = p.min_observation_dist
    total_steps = p.num_steps + 1
    inf = 1000.00

    difference_rewards = calc_difference_alpha(rover_paths, poi_values, poi_positions, global_reward)
    dpp_rewards = np.zeros(p.num_rovers)

    # Calculate Dpp Reward with (TotalAgents - 1) Counterfactuals
    n_counters = p.coupling - 1
    for agent_id in range(p.num_rovers):
        poi_observer_distances = np.zeros((p.num_pois, total_steps))

        for poi_id in range(p.num_pois):
            for step_index in range(total_steps):
                observer_count = 0
                rover_distances = np.zeros(p.num_rovers+n_counters)

                # Count how many agents observe poi, update closest distances
                for other_agent_id in range(p.num_rovers):
                    # Calculate separation distance between poi and agent
                    x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
                    y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
                    distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                    if distance < p.min_distance:
                        distance = p.min_distance

                    rover_distances[other_agent_id] = distance

                    if distance < min_obs_distance:
                        observer_count += 1

                # Add in counterfactual partners
                for partner_id in range(n_counters):
                    rover_distances[p.num_rovers+partner_id] = rover_distances[agent_id]

                    if rover_distances[agent_id] < min_obs_distance:
                        observer_count += 1

                # Update whether or not POI has been observed
                if observer_count >= p.coupling:
                    summed_observer_distances = 0.0
                    for observer in range(p.coupling):
                        # assert (min(rover_distances) < p.min_observation_dist)
                        summed_observer_distances += min(rover_distances)
                        od_index = np.argmin(rover_distances)
                        rover_distances[od_index] = inf
                    poi_observer_distances[poi_id, step_index] = summed_observer_distances
                else:
                    poi_observer_distances[poi_id, step_index] = inf

        counterfactual_global_reward = 0.0
        for poi_id in range(p.num_pois):
            if (min(poi_observer_distances[poi_id])/p.coupling) < p.min_observation_dist:
                counterfactual_global_reward += poi_values[poi_id]/((1/p.coupling)*min(poi_observer_distances[poi_id]))
        dpp_rewards[agent_id] = (counterfactual_global_reward - global_reward) / n_counters

    for agent_id in range(p.num_rovers):
        if dpp_rewards[agent_id] > difference_rewards[agent_id]:
            poi_observer_distances = np.zeros((p.num_pois, total_steps))

            for n_counters in range(p.coupling-1):
                for poi_id in range(p.num_pois):
                    for step_index in range(total_steps):
                        observer_count = 0
                        rover_distances = np.zeros(p.num_rovers + n_counters)

                        # Count how many agents observe poi, update closest distances
                        for other_agent_id in range(p.num_rovers):
                            # Calculate separation distance between poi and agent
                            x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
                            y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
                            distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                            if distance < p.min_distance:
                                distance = p.min_distance

                            rover_distances[other_agent_id] = distance

                            if distance < min_obs_distance:
                                observer_count += 1

                        # Add in counterfactual partners
                        for partner_id in range(n_counters):
                            rover_distances[p.num_rovers+partner_id] = rover_distances[agent_id]

                            if rover_distances[agent_id] < min_obs_distance:
                                observer_count += 1

                        # Determine if coupling has been satisfied
                        if observer_count >= p.coupling:
                            summed_observer_distances = 0.0
                            for observer in range(p.coupling):
                                # assert (min(rover_distances) < p.min_observation_dist)
                                summed_observer_distances += min(rover_distances)
                                od_index = np.argmin(rover_distances)
                                rover_distances[od_index] = inf
                            poi_observer_distances[poi_id, step_index] = summed_observer_distances
                        else:
                            poi_observer_distances[poi_id, step_index] = inf

                counterfactual_global_reward = 0.0
                for poi_id in range(p.num_pois):
                    if (min(poi_observer_distances[poi_id])/p.coupling) < p.min_observation_dist:
                        counterfactual_global_reward += poi_values[poi_id]/((1/p.coupling)*min(poi_observer_distances[poi_id]))
                if n_counters == 0:
                    n_counters = 1
                temp_dpp_reward = (counterfactual_global_reward - global_reward)/n_counters
                if dpp_rewards[agent_id] < temp_dpp_reward:
                    dpp_rewards[agent_id] = temp_dpp_reward
        else:
            dpp_rewards[agent_id] = difference_rewards[agent_id]  # Returns difference reward

    return dpp_rewards


# S-D++ REWARD --------------------------------------------------------------------------------------------------------
# def calc_sdpp(rover_paths, poi_values, poi_positions, global_reward):
#     number_agents = p.num_rovers
#     number_pois = p.num_pois
#     min_obs_distance = p.min_observation_dist
#     total_steps = p.num_steps + 1
#     inf = 1000.00
#
#     difference_rewards = calc_difference(rover_paths, poi_values, poi_positions, global_reward)
#     dpp_rewards = np.zeros(number_agents)
#
#     for agent_id in range(number_agents):
#         for step_index in range(total_steps):
#
#             counterfactual_global_reward = 0.0; added_observers = 0
#
#             for poi_id in range(number_pois):
#
#                 # Count how many agents observe poi, update closest distance if necessary
#                 observer_count = 0
#                 summed_observer_distances = 0.0
#                 observer_distances = np.zeros(number_agents)
#
#                 for other_agent_id in range(number_agents):
#                     # Calculate separation distance between poi and agent
#                     x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
#                     y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
#                     distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
#
#                     if distance < p.min_distance:
#                         distance = p.min_distance
#
#                     observer_distances[other_agent_id] = distance
#
#                     if distance < min_obs_distance:
#                         observer_count += 1
#
#                 # Add in counterfactual partners
#                 self_x = rover_paths[step_index, agent_id, 0]; self_y = rover_paths[step_index, agent_id, 1]
#                 suggested_partners, added_observers = high_value_only(observer_distances[agent_id], poi_id, poi_values)
#                 for partner_id in range(added_observers):
#                     np.append(observer_distances, suggested_partners[partner_id])
#                     if suggested_partners[partner_id] < p.min_observation_dist:
#                         observer_count += 1
#
#                 # update closest distance only if poi is observed
#                 if observer_count >= p.coupling:
#                     for observer_id in range(p.coupling):
#                         summed_observer_distances += min(observer_distances)
#                         od_index = np.argmin(observer_distances)
#                         observer_distances[od_index] = inf
#                     if summed_observer_distances == 0:
#                         summed_observer_distances = -1
#                     counterfactual_global_reward += poi_values[poi_id] / ((1/p.coupling) * summed_observer_distances)
#
#             temp_dpp_reward = (counterfactual_global_reward - global_reward)/(1 + added_observers)
#             if temp_dpp_reward > dpp_rewards[agent_id]:
#                 dpp_rewards[agent_id] = temp_dpp_reward
#
#         if dpp_rewards[agent_id] < difference_rewards[agent_id]:
#             dpp_rewards[agent_id] = difference_rewards[agent_id]  # Returns difference reward
#
#     return dpp_rewards

def calc_sdpp_alpha(rover_paths, poi_values, poi_positions, global_reward):
    min_obs_distance = p.min_observation_dist
    total_steps = p.num_steps + 1
    inf = 1000.00

    difference_rewards = calc_difference_alpha(rover_paths, poi_values, poi_positions, global_reward)
    dpp_rewards = np.zeros(p.num_rovers)

    n_counters = p.coupling - 1
    for agent_id in range(p.num_rovers):
        # poi_rewards = np.zeros(p.num_pois)
        coupled_distances = np.zeros((p.num_pois, total_steps))

        for step_index in range(total_steps):
            for poi_id in range(p.num_pois):
                observer_count = 0
                observer_distances = np.zeros(p.num_rovers + n_counters)

                # Count how many agents observe poi, update closest distances
                for other_agent_id in range(p.num_rovers):
                    # Calculate separation distance between poi and agent
                    x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
                    y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
                    distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                    if distance < p.min_distance:
                        distance = p.min_distance

                    observer_distances[other_agent_id] = distance

                    if distance < min_obs_distance:
                        observer_count += 1

                # Add in counterfactual partners
                added_observers = high_value_only(observer_distances[agent_id], poi_id, poi_values, n_counters)
                for partner_id in range(n_counters):
                    observer_distances[p.num_rovers + partner_id] = added_observers[partner_id]

                    if added_observers[partner_id] < min_obs_distance:
                        observer_count += 1

                # Update whether or not POI has been observed
                temp_poi_reward = 0.0
                if observer_count >= p.coupling:
                    # temp_poi_reward = poi_values[poi_id] / min(observer_distances)
                    summed_observer_distances = 0.0
                    for observer in range(p.coupling):
                        # assert (min(observer_distances) < p.min_observation_dist)
                        summed_observer_distances += min(observer_distances)
                        # od_index = np.argmin(observer_distances)
                        # observer_distances[od_index] = inf
                    coupled_distances[poi_id, step_index] = summed_observer_distances
                    # temp_poi_reward = poi_values[poi_id] / ((1 / p.coupling) * summed_observer_distances)
                else:
                    coupled_distances[poi_id, step_index] = inf

                # if temp_poi_reward > poi_rewards[poi_id]:
                #     poi_rewards[poi_id] = temp_poi_reward

        counterfactual_global_reward = 0.0
        for poi_id in range(p.num_pois):
            if min(coupled_distances[poi_id]) < (p.coupling * p.min_observation_dist):
                counterfactual_global_reward += poi_values[poi_id] / ((1 / p.coupling) * min(coupled_distances[poi_id]))
        dpp_rewards[agent_id] = (counterfactual_global_reward - global_reward) / n_counters

    for agent_id in range(p.num_rovers):
        if dpp_rewards[agent_id] > difference_rewards[agent_id]:
            # poi_rewards = np.zeros(p.num_pois)
            coupled_distances = np.zeros((p.num_pois, total_steps))

            for n_counters in range(p.coupling-1):
                for step_index in range(total_steps):
                    for poi_id in range(p.num_pois):
                        observer_count = 0
                        observer_distances = np.zeros(p.num_rovers + n_counters)

                        # Count how many agents observe poi, update closest distances
                        for other_agent_id in range(p.num_rovers):
                            # Calculate separation distance between poi and agent
                            x_distance = poi_positions[poi_id, 0] - rover_paths[step_index, other_agent_id, 0]
                            y_distance = poi_positions[poi_id, 1] - rover_paths[step_index, other_agent_id, 1]
                            distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

                            if distance < p.min_distance:
                                distance = p.min_distance

                            observer_distances[other_agent_id] = distance

                            if distance < min_obs_distance:
                                observer_count += 1

                        # Add in counterfactual partners
                        added_observers = high_value_only(observer_distances[agent_id], poi_id, poi_values, n_counters)
                        for partner_id in range(n_counters):
                            observer_distances[p.num_rovers + partner_id] = added_observers[partner_id]

                            if added_observers[partner_id] < min_obs_distance:
                                observer_count += 1

                        # Determine if coupling has been satisfied
                        temp_poi_reward = 0.0
                        if observer_count >= p.coupling:
                            # temp_poi_reward = poi_values[poi_id] / min(observer_distances)
                            summed_observer_distances = 0.0
                            for observer in range(p.coupling):
                                assert (min(observer_distances) < p.min_observation_dist)
                                summed_observer_distances += min(observer_distances)
                                # od_index = np.argmin(observer_distances)
                                # observer_distances[od_index] = inf
                            coupled_distances[poi_id, step_index] = summed_observer_distances
                            #temp_poi_reward = poi_values[poi_id] / ((1 / p.coupling) * summed_observer_distances)
                        else:
                            coupled_distances[poi_id, step_index] = inf

                        # if temp_poi_reward > poi_rewards[poi_id]:
                        #     poi_rewards[poi_id] = temp_poi_reward

                counterfactual_global_reward = 0.0
                for poi_id in range(p.num_pois):
                    if min(coupled_distances[poi_id]) < (p.coupling * p.min_observation_dist):
                        counterfactual_global_reward += poi_values[poi_id]/((1/p.coupling)*min(coupled_distances[poi_id]))
                if n_counters == 0: n_counters = 1
                temp_dpp_reward = (counterfactual_global_reward - global_reward)/n_counters
                if dpp_rewards[agent_id] < temp_dpp_reward:
                    dpp_rewards[agent_id] = temp_dpp_reward
        else:
            dpp_rewards[agent_id] = difference_rewards[agent_id]  # Returns difference reward

    return dpp_rewards
