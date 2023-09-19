from datetime import datetime

import numpy as np

from src.model.game.game import create_game
from src.model.user.user_action import create_all_possible_user_actions, UserAction
from src.model.user.user_functions import get_immediate_utility, get_immediate_payment, \
    get_normalized_immediate_reward, \
    get_expected_utility_and_payment_in_future, get_transition_probability, \
    get_preferred_action_if_deliver_equal_utility
from src.model.user.user_type import UserType, get_probability_user_type, get_truncated_normal
from src.numerical_framework.helpers.output_files_helper import write_backward_induction_result
from src.numerical_framework.helpers.tests_during_execution import test_reached_probabilities, \
    test_if_value_equal_one
from src.numerical_framework.result.result import BackwardInductionResult


def backward_induction_over_user_types(backward_induction_creator):
    """
    Executes the whole backward induction process, creates the result object and writes it to .csv files

    Parameters
    ----------
    backward_induction_creator : BackwardInductionCreator
        object containing all details about backward induction specifics
    """
    if backward_induction_creator.induction_with_all_user_types_from_game:
        for single_number_of_user_valuations in backward_induction_creator.number_of_user_valuations:
            for single_arrivals_in_first_timestep in backward_induction_creator.arrivals_in_first_timestep:
                for single_probability_of_second_quality_decay_element in backward_induction_creator.probability_of_second_quality_decay_element:
                    for single_engagement_factor_short_term_user in backward_induction_creator.engagement_factor_short_term_user:
                        for single_standard_deviation_valuation in backward_induction_creator.standard_deviation_valuation:
                            interval_length = (backward_induction_creator.valuation_range[1] -
                                               backward_induction_creator.valuation_range[
                                                   0]) / single_number_of_user_valuations
                            valuations = np.arange(backward_induction_creator.valuation_range[0],
                                                   backward_induction_creator.valuation_range[1] + interval_length,
                                                   interval_length)
                            quality_decay_factors = backward_induction_creator.quality_decay_factors
                            long_term_engagement_factors = [
                                single_engagement_factor_short_term_user,
                                backward_induction_creator.engagement_factor_long_term_user]
                            total_revenue = []
                            user_welfare = []
                            revenue_base_product_per_timestep = []
                            revenue_upgrade_per_timestep = []
                            revenue_subscription_per_timestep = []
                            revenue_base_product_per_timestep_single_user_type = []
                            revenue_upgrade_per_timestep_single_user_type = []
                            revenue_subscription_per_timestep_single_user_type = []
                            total_valuation_weight = 0
                            total_prob_user_type = 0

                            # prepare result object
                            backward_induction_result = BackwardInductionResult()
                            backward_induction_result.path_to_main_file = backward_induction_creator.path_to_main_file
                            backward_induction_result.number_of_user_valuations = single_number_of_user_valuations
                            backward_induction_result.price_strategy_type = backward_induction_creator.price_strategy_type
                            backward_induction_result.price_base_product = backward_induction_creator.product_information.price_base_product
                            backward_induction_result.price_upgrade = backward_induction_creator.product_information.price_upgrade
                            backward_induction_result.price_subscription = backward_induction_creator.product_information.price_subscription
                            backward_induction_result.n_max = backward_induction_creator.n_max
                            backward_induction_result.n_upgrade = backward_induction_creator.n_upgrade
                            backward_induction_result.engagement_factor_short_term_user = single_engagement_factor_short_term_user
                            backward_induction_result.engagement_factor_long_term_user = backward_induction_creator.engagement_factor_long_term_user
                            backward_induction_result.probability_short_term_user = backward_induction_creator.probability_short_term_user
                            backward_induction_result.quality_decay_factors = backward_induction_creator.quality_decay_factors
                            backward_induction_result.probability_of_second_quality_decay_factor = single_probability_of_second_quality_decay_element
                            backward_induction_result.valuation_range = backward_induction_creator.valuation_range
                            backward_induction_result.standard_deviation_valuation = single_standard_deviation_valuation
                            backward_induction_result.arrivals_in_first_timestep = single_arrivals_in_first_timestep
                            backward_induction_result.product_quality_base_product = backward_induction_creator.product_quality_base_product
                            backward_induction_result.product_quality_upgrade = backward_induction_creator.product_quality_upgrade
                            backward_induction_result.files_results_are_written_to = backward_induction_creator.files_results_are_written_to
                            backward_induction_result.path_to_folder = backward_induction_creator.path_to_folder

                            for i in range(0, backward_induction_creator.n_max):
                                revenue_base_product_per_timestep.append(0)
                                revenue_upgrade_per_timestep.append(0)
                                revenue_subscription_per_timestep.append(0)
                                revenue_base_product_per_timestep_single_user_type.append(0)
                                revenue_upgrade_per_timestep_single_user_type.append(0)
                                revenue_subscription_per_timestep_single_user_type.append(0)

                            for v in range(len(valuations) - 1):
                                lowerbound = valuations[v]
                                upperbound = valuations[v + 1]
                                valuation_mean = (backward_induction_creator.valuation_range[0] +
                                                  backward_induction_creator.valuation_range[1]) / 2

                                if single_standard_deviation_valuation != 0:
                                    cdf_lowerboud = get_truncated_normal(mean=valuation_mean,
                                                                         sd=single_standard_deviation_valuation,
                                                                         low=backward_induction_creator.valuation_range[
                                                                             0],
                                                                         upp=backward_induction_creator.valuation_range[
                                                                             1]).cdf(
                                        lowerbound)
                                    cdf_upperbound = get_truncated_normal(mean=valuation_mean,
                                                                          sd=single_standard_deviation_valuation,
                                                                          low=
                                                                          backward_induction_creator.valuation_range[0],
                                                                          upp=
                                                                          backward_induction_creator.valuation_range[
                                                                              1]).cdf(
                                        upperbound)
                                    valuation_weight = cdf_upperbound - cdf_lowerboud
                                    total_valuation_weight += valuation_weight

                                    valuation = (lowerbound + upperbound) / 2
                                    valuation = valuation
                                # single_standard_deviation_valuation == 0
                                else:
                                    valuation = valuation_mean
                                    valuation_weight = 1 / (len(valuations) - 1)
                                    total_valuation_weight += valuation_weight

                                for quality_decay_factor in quality_decay_factors:
                                    for engagement_factor in long_term_engagement_factors:
                                        user_type = UserType(None, engagement_factor, quality_decay_factor, valuation)
                                        product_information = backward_induction_creator.product_information

                                        game = create_game(product_information, user_type,
                                                           backward_induction_creator.n_max,
                                                           backward_induction_creator.n_upgrade,
                                                           backward_induction_creator.price_strategy_type)
                                        calculate_optimal_user_actions(game)

                                        for arr_time in range(1, backward_induction_creator.n_max + 1):
                                            game.user_type.arrival_time = arr_time
                                            calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(
                                                game)
                                            test_reached_probabilities(game)
                                            prob_user_type = get_probability_user_type(game.user_type,
                                                                                       backward_induction_creator,
                                                                                       single_arrivals_in_first_timestep,
                                                                                       single_probability_of_second_quality_decay_element,
                                                                                       single_engagement_factor_short_term_user) * valuation_weight
                                            total_revenue += [game.expected_publisher_revenue * prob_user_type]
                                            user_welfare += [game.expected_user_welfare * prob_user_type]
                                            total_prob_user_type += prob_user_type

                                            # set revenue for single user type to 0
                                            for i in range(0, game.n_max):
                                                revenue_base_product_per_timestep_single_user_type[i] = 0
                                                revenue_upgrade_per_timestep_single_user_type[i] = 0
                                                revenue_subscription_per_timestep_single_user_type[i] = 0

                                            # count revenue for different timesteps and products
                                            timestep_count_revenue = game.n_max
                                            while timestep_count_revenue > 0:
                                                for current_user_state in game.user_states[timestep_count_revenue - 1]:
                                                    if current_user_state.probability_state_is_reached > 0:
                                                        revenue_base_product_current_timestep = 0
                                                        revenue_upgrade_current_timestep = 0
                                                        revenue_subscription_current_timestep = 0
                                                        if current_user_state.best_action.subscribe_action == 1:
                                                            revenue_subscription_current_timestep += \
                                                                backward_induction_creator.product_information.price_subscription[
                                                                    timestep_count_revenue - 1] * current_user_state.probability_state_is_reached

                                                            if timestep_count_revenue == game.n_max:
                                                                revenue_subscription_current_timestep += current_user_state.expected_payment_in_future * current_user_state.probability_state_is_reached

                                                        if current_user_state.best_action.buy_action.base_product == 1:
                                                            revenue_base_product_current_timestep += \
                                                                backward_induction_creator.product_information.price_base_product[
                                                                    timestep_count_revenue - 1] * current_user_state.probability_state_is_reached

                                                        if current_user_state.best_action.buy_action.upgrade == 1:
                                                            revenue_upgrade_current_timestep += \
                                                                backward_induction_creator.product_information.price_upgrade[
                                                                    timestep_count_revenue - 1] * current_user_state.probability_state_is_reached

                                                        revenue_base_product_per_timestep[
                                                            timestep_count_revenue - 1] += revenue_base_product_current_timestep * prob_user_type
                                                        revenue_base_product_per_timestep_single_user_type[
                                                            timestep_count_revenue - 1] += revenue_base_product_current_timestep
                                                        revenue_upgrade_per_timestep[
                                                            timestep_count_revenue - 1] += revenue_upgrade_current_timestep * prob_user_type
                                                        revenue_upgrade_per_timestep_single_user_type[
                                                            timestep_count_revenue - 1] += revenue_upgrade_current_timestep
                                                        revenue_subscription_per_timestep[
                                                            timestep_count_revenue - 1] += revenue_subscription_current_timestep * prob_user_type
                                                        revenue_subscription_per_timestep_single_user_type[
                                                            timestep_count_revenue - 1] += revenue_subscription_current_timestep
                                                timestep_count_revenue -= 1

                                            if backward_induction_creator.print_single_user_types:
                                                backward_induction_result.timestamp = datetime.now().strftime(
                                                    "%m.%d.%Y_%H.%M.%S")
                                                backward_induction_result.probability_user_type = prob_user_type
                                                backward_induction_result.arrival_time = arr_time
                                                backward_induction_result.valuation = valuation
                                                backward_induction_result.engagement_factor = engagement_factor
                                                backward_induction_result.quality_decay_factor = quality_decay_factor
                                                backward_induction_result.expected_publisher_revenue = game.expected_publisher_revenue
                                                backward_induction_result.expected_user_welfare = game.expected_user_welfare
                                                backward_induction_result.expected_total_welfare = game.expected_user_welfare + game.expected_publisher_revenue
                                                backward_induction_result.revenue_base_product = revenue_base_product_per_timestep_single_user_type
                                                backward_induction_result.revenue_upgrade = revenue_upgrade_per_timestep_single_user_type
                                                backward_induction_result.revenue_subscription = revenue_subscription_per_timestep_single_user_type
                                                # write backward induction results to .csv file
                                                write_backward_induction_result(backward_induction_result)

                                            # set values to 0 again
                                            game.expected_publisher_revenue = 0
                                            game.expected_user_welfare = 0
                                            timestep = game.n_max

                                            while timestep > 0:
                                                for user_state in game.user_states[timestep - 1]:
                                                    user_state.probability_state_is_reached = 0
                                                timestep -= 1

                            if backward_induction_creator.print_user_types_combined:
                                backward_induction_result.timestamp = datetime.now().strftime(
                                    "%m.%d.%Y_%H.%M.%S")
                                backward_induction_result.probability_user_type = round(total_prob_user_type, 5)
                                backward_induction_result.arrival_time = [1, backward_induction_creator.n_max]
                                backward_induction_result.valuation = backward_induction_creator.valuation_range
                                backward_induction_result.engagement_factor = [single_engagement_factor_short_term_user,
                                                                               backward_induction_creator.engagement_factor_long_term_user]
                                backward_induction_result.quality_decay_factor = backward_induction_creator.quality_decay_factors
                                backward_induction_result.expected_publisher_revenue = sum(total_revenue)
                                backward_induction_result.expected_user_welfare = sum(user_welfare)
                                backward_induction_result.expected_total_welfare = sum(total_revenue) + sum(
                                    user_welfare)
                                backward_induction_result.revenue_base_product = revenue_base_product_per_timestep
                                backward_induction_result.revenue_upgrade = revenue_upgrade_per_timestep
                                backward_induction_result.revenue_subscription = revenue_subscription_per_timestep

                                # write backward induction results to .csv file
                                write_backward_induction_result(backward_induction_result)

                            test_if_value_equal_one(total_valuation_weight, "total_valuation_weight")
                            test_if_value_equal_one(total_prob_user_type, "total_prob_user_type")

    # induction_with_all_user_types_from_game = False => backward induction for single user types
    else:
        # prepare result object
        backward_induction_result = BackwardInductionResult()
        backward_induction_result.path_to_main_file = backward_induction_creator.path_to_main_file
        backward_induction_result.number_of_user_valuations = "-"
        backward_induction_result.price_strategy_type = backward_induction_creator.price_strategy_type
        backward_induction_result.price_base_product = backward_induction_creator.product_information.price_base_product
        backward_induction_result.price_upgrade = backward_induction_creator.product_information.price_upgrade
        backward_induction_result.price_subscription = backward_induction_creator.product_information.price_subscription
        backward_induction_result.n_max = backward_induction_creator.n_max
        backward_induction_result.n_upgrade = backward_induction_creator.n_upgrade
        backward_induction_result.engagement_factor_short_term_user = "-"
        backward_induction_result.engagement_factor_long_term_user = "-"
        backward_induction_result.probability_short_term_user = "-"
        backward_induction_result.quality_decay_factors = "-"
        backward_induction_result.probability_of_second_quality_decay_factor = "-"
        backward_induction_result.valuation_range = "-"
        backward_induction_result.standard_deviation_valuation = "-"
        backward_induction_result.arrivals_in_first_timestep = "-"
        backward_induction_result.probability_user_type = "-"
        backward_induction_result.product_quality_base_product = backward_induction_creator.product_quality_base_product
        backward_induction_result.product_quality_upgrade = backward_induction_creator.product_quality_upgrade
        backward_induction_result.files_results_are_written_to = backward_induction_creator.files_results_are_written_to
        backward_induction_result.path_to_folder = backward_induction_creator.path_to_folder

        for valuation in backward_induction_creator.user_valuations:
            for arrival_time in backward_induction_creator.user_arrival_times:
                for engagement_factor in backward_induction_creator.user_engagement_factors:
                    for quality_decay_factor in backward_induction_creator.user_quality_decay_factors:
                        user_type = UserType(arrival_time, engagement_factor, quality_decay_factor, valuation)
                        game = create_game(backward_induction_creator.product_information,
                                           user_type, backward_induction_creator.n_max,
                                           backward_induction_creator.n_upgrade,
                                           backward_induction_creator.price_strategy_type)

                        # do backward induction
                        calculate_optimal_user_actions(game)
                        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
                        test_reached_probabilities(game)

                        # count actions of user type
                        timestep_count_revenue = game.n_max
                        revenue_base_product_per_timestep = []
                        revenue_upgrade_per_timestep = []
                        revenue_subscription_per_timestep = []

                        for i in range(0, game.n_max):
                            revenue_base_product_per_timestep.append(0)
                            revenue_upgrade_per_timestep.append(0)
                            revenue_subscription_per_timestep.append(0)

                        while timestep_count_revenue > 0:
                            for current_user_state in game.user_states[timestep_count_revenue - 1]:
                                if current_user_state.probability_state_is_reached > 0:
                                    if current_user_state.best_action.subscribe_action == 1:
                                        revenue_subscription_per_timestep[timestep_count_revenue - 1] += \
                                            backward_induction_creator.product_information.price_subscription[
                                                timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
                                        if timestep_count_revenue == game.n_max:
                                            revenue_subscription_per_timestep[
                                                timestep_count_revenue - 1] += current_user_state.expected_payment_in_future * current_user_state.probability_state_is_reached
                                    if current_user_state.best_action.buy_action.base_product == 1:
                                        revenue_base_product_per_timestep[timestep_count_revenue - 1] += \
                                            backward_induction_creator.product_information.price_base_product[
                                                timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
                                    if current_user_state.best_action.buy_action.upgrade == 1:
                                        revenue_upgrade_per_timestep[timestep_count_revenue - 1] += \
                                            backward_induction_creator.product_information.price_upgrade[
                                                timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
                            timestep_count_revenue -= 1

                        backward_induction_result.timestamp = datetime.now().strftime(
                            "%m.%d.%Y_%H.%M.%S")
                        backward_induction_result.arrival_time = arrival_time
                        backward_induction_result.valuation = valuation
                        backward_induction_result.engagement_factor = engagement_factor
                        backward_induction_result.quality_decay_factor = quality_decay_factor
                        backward_induction_result.expected_publisher_revenue = game.expected_publisher_revenue
                        backward_induction_result.expected_user_welfare = game.expected_user_welfare
                        backward_induction_result.expected_total_welfare = game.expected_user_welfare + game.expected_publisher_revenue
                        backward_induction_result.revenue_base_product = revenue_base_product_per_timestep
                        backward_induction_result.revenue_upgrade = revenue_upgrade_per_timestep
                        backward_induction_result.revenue_subscription = revenue_subscription_per_timestep

                        # write backward induction results to .csv file
                        write_backward_induction_result(backward_induction_result)


def calculate_optimal_user_actions(game):
    """
    Finds the optimal action for every user state in every timestep (i.e., backward induction is performed)

    Parameters
    ----------
    game : Game
        object holding all important information for the publisher and user acting optimally against each other
    """
    # get all possible user actions
    all_possible_user_actions = create_all_possible_user_actions(game.price_strategy_type)

    # do actual backward induction by iteration back from n_max to 1
    timestep = game.n_max

    while timestep > 0:
        for current_user_state in game.user_states[timestep - 1]:
            best_action = UserAction(0, [0, 0])
            best_normalized_immediate_reward = 0
            best_immediate_payment = 0
            best_immediate_utility = 0
            best_expected_payment_in_future = 0
            best_expected_utility_in_future_best = 0
            best_expected_utility = 0

            for user_action in all_possible_user_actions:
                # it is not allowed to buy the upgrade without owning or buying the base product
                if current_user_state.ownership.base_product == 0 and user_action.buy_action.base_product == 0 and user_action.buy_action.upgrade == 1:
                    continue
                # it is never optimal to subscribe if base product and upgrade are already owned
                if current_user_state.ownership.base_product == 1 and current_user_state.ownership.upgrade == 1 and user_action.subscribe_action == 1:
                    continue
                # if upgrade is not released yet it cannot be optimal to buy it
                if user_action.buy_action.upgrade == 1 and timestep < game.n_upgrade:
                    continue
                # if base product or upgrade already owned, it is never optimal to buy the corresponding product
                if user_action.buy_action.upgrade == 1 and current_user_state.ownership.upgrade == 1:
                    continue
                if user_action.buy_action.base_product == 1 and current_user_state.ownership.base_product == 1:
                    continue
                immediate_utility = get_immediate_utility(timestep, game.n_upgrade,
                                                          user_action, game.user_type,
                                                          current_user_state,
                                                          game.product_information)
                expected_utility_in_future, expected_future_payment = get_expected_utility_and_payment_in_future(
                    timestep, current_user_state, user_action, game)

                total_expected_utility_for_action = immediate_utility + expected_utility_in_future

                if total_expected_utility_for_action >= best_expected_utility:
                    if total_expected_utility_for_action == best_expected_utility and total_expected_utility_for_action > 0:
                        if get_preferred_action_if_deliver_equal_utility(user_action, best_action) != user_action:
                            continue

                    best_action = user_action
                    best_immediate_utility = immediate_utility
                    best_immediate_payment = get_immediate_payment(timestep, user_action, game.product_information)
                    best_normalized_immediate_reward = get_normalized_immediate_reward(timestep,
                                                                                       game.n_upgrade, user_action,
                                                                                       game.user_type,
                                                                                       current_user_state,
                                                                                       game.product_information)
                    best_expected_payment_in_future = expected_future_payment
                    best_expected_utility_in_future_best = expected_utility_in_future
                    best_expected_utility = total_expected_utility_for_action

            current_user_state.best_action = best_action
            current_user_state.immediate_payment = best_immediate_payment
            current_user_state.normalized_immediate_reward = best_normalized_immediate_reward
            current_user_state.immediate_utility = best_immediate_utility
            current_user_state.expected_payment_in_future = best_expected_payment_in_future
            current_user_state.expected_utility_in_future = best_expected_utility_in_future_best
            current_user_state.expected_utility = best_expected_utility

        timestep -= 1


def calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game):
    """
    Calculates and adds the probabilities a state is reached to the game object

    Parameters
    ----------
    game : Game
        object holding all important information for the publisher and user acting optimally against each other
    """
    # set probability of start state to 1
    get_start_state(game).probability_state_is_reached = 1

    timestep = game.user_type.arrival_time
    while timestep <= game.n_max:
        for user_state in game.user_states[timestep - 1]:
            for last_user_state in game.user_states[timestep - 2]:
                if last_user_state.probability_state_is_reached > 0:
                    user_state.probability_state_is_reached += get_transition_probability(timestep, game.n_upgrade,
                                                                                          user_state, last_user_state,
                                                                                          last_user_state.best_action,
                                                                                          game.user_type,
                                                                                          game.product_information.product_quality.upgrade) * \
                                                               last_user_state.probability_state_is_reached

            game.expected_publisher_revenue += user_state.probability_state_is_reached * user_state.immediate_payment
            game.expected_user_welfare += user_state.probability_state_is_reached * user_state.immediate_utility
            if timestep == game.n_max:
                game.expected_user_welfare += user_state.probability_state_is_reached * user_state.expected_utility_in_future
                game.expected_publisher_revenue += user_state.probability_state_is_reached * user_state.expected_payment_in_future

        timestep += 1


def get_start_state(game):
    """
    Finds the starting state for the user type playing the game

    Parameters
    ----------
    game : Game
        object holding all important information for the publisher and user acting optimally against each other

    Returns
    -------
    UserState
        user state where user type is starting
    """
    for user_state in game.user_states[game.user_type.arrival_time - 1]:
        if user_state.demand == 1 and user_state.ownership.base_product == 0 and user_state.ownership.upgrade == 0:
            return user_state
