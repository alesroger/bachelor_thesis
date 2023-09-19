import time
from datetime import datetime

import numpy as np
from scipy.optimize import differential_evolution

from src.model.game.game import create_game
from src.model.game.price_strategy_type import PriceStrategyType
from src.model.publisher.productinformation import ProductInformation
from src.model.user.user_type import UserType, get_probability_user_type, get_truncated_normal
from src.numerical_framework.backward_induction.backward_induction import calculate_optimal_user_actions, \
    calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare
from src.numerical_framework.helpers.high_price import HighPrice
from src.numerical_framework.helpers.output_files_helper import add_first_line_to_document, add_line_to_document, \
    create_or_get_file, PARTITION_LINE, fill_text_file_with_basic_information, write_differential_evolution_result
from src.numerical_framework.helpers.tests_during_execution import test_reached_probabilities, \
    test_if_value_equal_one
from src.numerical_framework.result.result import DifferentialEvolutionResult

EVALUATION_NUMBER = 0


class PriceBounds(object):
    """
    A class used to represent Price Bounds used to perform Differential Evolution

    ...

    Attributes
    ----------
    buy_min : int
        minimum bound for base product price
    buy_max : int
        maximum bound for base product price
    upgrade_min : int
        minimum bound for upgrade price
    upgrade_max : int
        maximum bound for upgrade price
    subscription_min : int
        minimum bound for subscription price
    subscription_max : int
        maximum bound for subscription price
    """

    def __init__(self, buy_min, buy_max, upgrade_min, upgrade_max, subscription_min, subscription_max):
        """
        Parameters
        ----------
        buy_min : int
            minimum bound for base product price
        buy_max : int
            maximum bound for base product price
        upgrade_min : int
            minimum bound for upgrade price
        upgrade_max : int
            maximum bound for upgrade price
        subscription_min : int
            minimum bound for subscription price
        subscription_max : int
            maximum bound for subscription price

        """
        self.buy_min = buy_min
        self.buy_max = buy_max
        self.upgrade_min = upgrade_min
        self.upgrade_max = upgrade_max
        self.subscription_min = subscription_min
        self.subscription_max = subscription_max


def differential_evolution_maximize_revenue(differential_evolution_creator):
    """
    Executes the whole differential evolution process, creates the result object and writes it to .csv files

    Parameters
    ----------
    differential_evolution_creator : DifferentialEvolutionCreator
        object containing all details about differential evolution specifics
    """

    number_of_iterations_over_same_type = 0

    # for single user type, the following variables are not important and length of lists is set to 1 to prevent too many iterations over for-loops
    if not differential_evolution_creator.evolution_with_all_user_types_from_game:
        differential_evolution_creator.number_of_user_valuations = [1]
        differential_evolution_creator.arrivals_in_first_timestep = [1]
        differential_evolution_creator.probability_of_second_quality_decay_element = [1]
        differential_evolution_creator.engagement_factor_short_term_user = [1]
        differential_evolution_creator.standard_deviation_valuation = [1]

    while number_of_iterations_over_same_type < differential_evolution_creator.number_of_iterations_per_evolution_type:
        for single_number_of_user_valuations in differential_evolution_creator.number_of_user_valuations:
            for single_arrivals_in_first_timestep in differential_evolution_creator.arrivals_in_first_timestep:
                for single_probability_of_second_quality_decay_element in differential_evolution_creator.probability_of_second_quality_decay_element:
                    for single_engagement_factor_short_term_user in differential_evolution_creator.engagement_factor_short_term_user:
                        for single_standard_deviation_valuation in differential_evolution_creator.standard_deviation_valuation:
                            for strategy in differential_evolution_creator.differential_evolution_strategies:
                                for popsize in differential_evolution_creator.popsizes:
                                    start_time = datetime.now()

                                    # create and fill overview .txt file with basic informations for differential evolution
                                    file_name = start_time.strftime(
                                        "%m.%d.%Y_%H.%M.%S") + "_" + differential_evolution_creator.price_strategy_type + ".txt"
                                    path_to_file_folder = differential_evolution_creator.path_to_folder + "/" + \
                                                          differential_evolution_creator.name_main_file_without_ending
                                    file_path = create_or_get_file(path_to_file_folder, file_name)
                                    fill_text_file_with_basic_information(differential_evolution_creator, file_path)

                                    # run differential evolution
                                    bounds = create_bounds(differential_evolution_creator)
                                    arguments = (
                                        differential_evolution_creator, file_path, single_number_of_user_valuations,
                                        single_arrivals_in_first_timestep,
                                        single_probability_of_second_quality_decay_element,
                                        single_engagement_factor_short_term_user, single_standard_deviation_valuation)
                                    # workers = -1 to use all available CPU cores
                                    # workers = -1 overrides updating to 'deferred' since parallelization is needed
                                    # updating = 'deferred' is compatible with parallelization
                                    result = differential_evolution(objective_maximize_revenue, bounds, args=arguments,
                                                                    workers=-1, updating='deferred', popsize=popsize,
                                                                    strategy=strategy)
                                    end_time = datetime.now()

                                    # access differential evolution result
                                    solution = result['x']
                                    number_of_evaluations = result['nfev']
                                    evaluation = objective_maximize_revenue(solution, differential_evolution_creator,
                                                                            file_path, single_number_of_user_valuations,
                                                                            single_arrivals_in_first_timestep,
                                                                            single_probability_of_second_quality_decay_element,
                                                                            single_engagement_factor_short_term_user,
                                                                            single_standard_deviation_valuation)
                                    price_base_product, price_upgrade, price_subscription, revenue_per_user, welfare_per_user, revenue_base_product_per_timestep, revenue_upgrade_per_timestep, revenue_subscription_per_timestep = get_solution_details(
                                        solution, differential_evolution_creator,
                                        file_path, single_number_of_user_valuations,
                                        single_arrivals_in_first_timestep,
                                        single_probability_of_second_quality_decay_element,
                                        single_engagement_factor_short_term_user,
                                        single_standard_deviation_valuation)

                                    # write differential evolution results to .txt file
                                    price_base_product_rounded = []
                                    price_upgrade_rounded = []
                                    price_subscription_rounded = []
                                    for i in range(len(price_base_product)):
                                        price_base_product_rounded.append(round(price_base_product[i], 4))
                                        price_upgrade_rounded.append(round(price_upgrade[i], 4))
                                        price_subscription_rounded.append(round(price_subscription[i], 4))
                                    add_first_line_to_document(file_path, PARTITION_LINE)
                                    additional_info_line = "Total evaluations: " + str(
                                        number_of_evaluations) + ", \t Status: " + str(
                                        result['message'])
                                    main_info_line = "Solution: " + str(solution) + ", \t Evaluation: " + str(
                                        evaluation)
                                    time_information_line = "Runtime: " + str(
                                        end_time - start_time) + ",\t Start time: " + start_time.strftime(
                                        "%m.%d.%Y_%H.%M.%S") + ",\t End Time: " + end_time.strftime(
                                        "%m.%d.%Y_%H.%M.%S")
                                    info_string_end_result = "Revenue: " + str(
                                        round(revenue_per_user, 4)) + "Welfare: " + str(
                                        round(welfare_per_user, 4)) + ",\t Base product price: " + str(
                                        price_base_product_rounded) + ",\t Upgrade price: " + str(
                                        price_upgrade_rounded) + ",\t Subscription price: " + str(
                                        round(price_subscription[0], 4))
                                    add_first_line_to_document(file_path, PARTITION_LINE)
                                    add_first_line_to_document(file_path, additional_info_line)
                                    add_first_line_to_document(file_path, PARTITION_LINE)
                                    add_first_line_to_document(file_path, info_string_end_result)
                                    add_first_line_to_document(file_path, PARTITION_LINE)
                                    add_first_line_to_document(file_path, main_info_line)
                                    add_first_line_to_document(file_path, "RESULT")
                                    add_first_line_to_document(file_path, PARTITION_LINE)
                                    add_first_line_to_document(file_path, time_information_line)

                                    # write differential evolution results to .csv file
                                    differential_evolution_result = DifferentialEvolutionResult()
                                    differential_evolution_result.path_to_main_file = differential_evolution_creator.path_to_main_file
                                    differential_evolution_result.number_of_user_valuations = single_number_of_user_valuations
                                    differential_evolution_result.price_strategy_type = differential_evolution_creator.price_strategy_type
                                    differential_evolution_result.price_base_product = price_base_product
                                    differential_evolution_result.price_upgrade = price_upgrade
                                    differential_evolution_result.price_subscription = price_subscription
                                    differential_evolution_result.n_max = differential_evolution_creator.n_max
                                    differential_evolution_result.n_upgrade = differential_evolution_creator.n_upgrade
                                    differential_evolution_result.engagement_factor_short_term_user = single_engagement_factor_short_term_user
                                    differential_evolution_result.engagement_factor_long_term_user = differential_evolution_creator.engagement_factor_long_term_user
                                    differential_evolution_result.probability_short_term_user = differential_evolution_creator.probability_short_term_user
                                    differential_evolution_result.quality_decay_factors = differential_evolution_creator.quality_decay_factors
                                    differential_evolution_result.probability_of_second_quality_decay_factor = single_probability_of_second_quality_decay_element
                                    differential_evolution_result.valuation_range = differential_evolution_creator.valuation_range
                                    differential_evolution_result.standard_deviation_valuation = single_standard_deviation_valuation
                                    differential_evolution_result.arrivals_in_first_timestep = single_arrivals_in_first_timestep
                                    differential_evolution_result.product_quality_base_product = differential_evolution_creator.product_quality_base_product
                                    differential_evolution_result.product_quality_upgrade = differential_evolution_creator.product_quality_upgrade
                                    differential_evolution_result.files_results_are_written_to = differential_evolution_creator.files_results_are_written_to
                                    differential_evolution_result.path_to_folder = differential_evolution_creator.path_to_folder
                                    differential_evolution_result.expected_publisher_revenue = revenue_per_user
                                    differential_evolution_result.expected_user_welfare = welfare_per_user
                                    differential_evolution_result.expected_total_welfare = revenue_per_user + welfare_per_user
                                    differential_evolution_result.revenue_base_product = revenue_base_product_per_timestep
                                    differential_evolution_result.revenue_upgrade = revenue_upgrade_per_timestep
                                    differential_evolution_result.revenue_subscription = revenue_subscription_per_timestep
                                    differential_evolution_result.evolution_with_all_user_types_from_game = differential_evolution_creator.evolution_with_all_user_types_from_game
                                    differential_evolution_result.start_time = start_time
                                    differential_evolution_result.runtime = end_time - start_time
                                    differential_evolution_result.number_of_evaluations = number_of_evaluations
                                    differential_evolution_result.is_prices_discounted = differential_evolution_creator.is_prices_discounted
                                    differential_evolution_result.is_subscription_price_variable = differential_evolution_creator.is_subscription_price_variable
                                    differential_evolution_result.price_bounds = differential_evolution_creator.price_bounds
                                    differential_evolution_result.popsize = popsize
                                    differential_evolution_result.differential_evolution_strategy = strategy
                                    differential_evolution_result.user_valuation = "-"
                                    differential_evolution_result.user_arrival_time = "-"
                                    differential_evolution_result.user_quality_decay_factor = "-"
                                    differential_evolution_result.user_engagement_factor = "-"
                                    differential_evolution_result.first_base_price_fixed = differential_evolution_creator.first_base_price_fixed
                                    differential_evolution_result.first_upgrade_price_fixed = differential_evolution_creator.first_upgrade_price_fixed

                                    if not differential_evolution_creator.evolution_with_all_user_types_from_game:
                                        differential_evolution_result.user_valuation = differential_evolution_creator.user_valuation
                                        differential_evolution_result.user_arrival_time = differential_evolution_creator.user_arrival_time
                                        differential_evolution_result.user_quality_decay_factor = differential_evolution_creator.user_quality_decay_factor
                                        differential_evolution_result.user_engagement_factor = differential_evolution_creator.user_engagement_factor

                                    write_differential_evolution_result(differential_evolution_result)

                                    # set global evaluation number to 0 for next evolution
                                    global EVALUATION_NUMBER
                                    EVALUATION_NUMBER = 0

        number_of_iterations_over_same_type += 1

        # wait 1 second such that very fast evolutions differ in their .txt file name
        time.sleep(1)


def objective_maximize_revenue(prices, *arguments):
    """
    Defines the objective function which is to be maximized through differential evolution

    Parameters
    ----------
    prices : list[float]
        list containing all prices (variables) for the specific evaluation of differential evolution
    *arguments
        all other necessary arguments for one single differential evolution evaluation such as the DifferentialEvolutionCreator
    """
    differential_evolution_creator, file_path, single_number_of_user_valuations, single_arrivals_in_first_timestep, single_probability_of_second_quality_decay_element, single_engagement_factor_short_term_user, single_standard_deviation_valuation = arguments

    global EVALUATION_NUMBER
    EVALUATION_NUMBER += 1

    # create price vectors from inserted bounds
    price_base_product, price_upgrade, price_subscription = get_price_vectors(prices, differential_evolution_creator)

    if differential_evolution_creator.evolution_with_all_user_types_from_game:
        # prepare user types
        interval_length = (differential_evolution_creator.valuation_range[1] -
                           differential_evolution_creator.valuation_range[
                               0]) / single_number_of_user_valuations
        valuations = np.arange(differential_evolution_creator.valuation_range[0],
                               differential_evolution_creator.valuation_range[1] + interval_length, interval_length)
        quality_decay_factors = differential_evolution_creator.quality_decay_factors
        long_term_engagement_factors = [single_engagement_factor_short_term_user,
                                        differential_evolution_creator.engagement_factor_long_term_user]

        total_revenue = []
        user_welfare = []

        # only used for execution testing
        total_valuation_weight = 0
        total_prob_user_type = 0

        # iterate over valuation types
        for v in range(len(valuations) - 1):
            lowerbound = valuations[v]
            upperbound = valuations[v + 1]
            valuation_mean = (differential_evolution_creator.valuation_range[0] +
                              differential_evolution_creator.valuation_range[1]) / 2
            if single_standard_deviation_valuation != 0:
                cdf_lowerboud = get_truncated_normal(mean=valuation_mean,
                                                     sd=single_standard_deviation_valuation,
                                                     low=differential_evolution_creator.valuation_range[0],
                                                     upp=differential_evolution_creator.valuation_range[1]).cdf(
                    lowerbound)
                cdf_upperbound = get_truncated_normal(mean=valuation_mean,
                                                      sd=single_standard_deviation_valuation,
                                                      low=differential_evolution_creator.valuation_range[0],
                                                      upp=differential_evolution_creator.valuation_range[1]).cdf(
                    upperbound)
                valuation_weight = cdf_upperbound - cdf_lowerboud
                total_valuation_weight += valuation_weight

                valuation = (lowerbound + upperbound) / 2
            # single_standard_deviation_valuation == 0
            else:
                valuation = valuation_mean
                valuation_weight = 1 / (len(valuations) - 1)
                total_valuation_weight += valuation_weight

            for quality_decay_factor in quality_decay_factors:
                for long_term_engagement_factor in long_term_engagement_factors:
                    user_type = UserType(None, long_term_engagement_factor, quality_decay_factor, valuation)
                    product_information = ProductInformation(price_base_product, price_upgrade, price_subscription,
                                                             [
                                                                 differential_evolution_creator.product_quality_base_product,
                                                                 differential_evolution_creator.product_quality_upgrade])

                    game = create_game(product_information, user_type, differential_evolution_creator.n_max,
                                       differential_evolution_creator.n_upgrade,
                                       differential_evolution_creator.price_strategy_type)
                    calculate_optimal_user_actions(game)

                    # optimal actions are independent of arrival time and can be reused
                    for arrival_time in range(1, differential_evolution_creator.n_max + 1):
                        game.user_type.arrival_time = arrival_time
                        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
                        test_reached_probabilities(game)

                        prob_user_type = get_probability_user_type(game.user_type,
                                                                   differential_evolution_creator,
                                                                   single_arrivals_in_first_timestep,
                                                                   single_probability_of_second_quality_decay_element,
                                                                   single_engagement_factor_short_term_user) * valuation_weight
                        total_revenue.append(game.expected_publisher_revenue * prob_user_type)
                        user_welfare.append(game.expected_user_welfare * prob_user_type)
                        total_prob_user_type += prob_user_type
                        # set values to 0 again
                        game.expected_publisher_revenue = 0
                        game.expected_user_welfare = 0
                        timestep = game.n_max
                        while timestep > 0:
                            for user_state in game.user_states[timestep - 1]:
                                user_state.probability_state_is_reached = 0
                            timestep -= 1
        revenue_per_user_type = sum(total_revenue)
        test_if_value_equal_one(total_valuation_weight, "total_valuation_weight")
        test_if_value_equal_one(total_prob_user_type, "total_prob_user_type")



    # evolution_with_all_user_types_from_game = False => evolution for single user type
    else:
        user_type = UserType(differential_evolution_creator.user_arrival_time,
                             differential_evolution_creator.user_engagement_factor,
                             differential_evolution_creator.user_quality_decay_factor,
                             differential_evolution_creator.user_valuation)
        product_information = ProductInformation(price_base_product, price_upgrade, price_subscription,
                                                 [differential_evolution_creator.product_quality_base_product,
                                                  differential_evolution_creator.product_quality_upgrade])

        game = create_game(product_information, user_type, differential_evolution_creator.n_max,
                           differential_evolution_creator.n_upgrade,
                           differential_evolution_creator.price_strategy_type)
        calculate_optimal_user_actions(game)
        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
        test_reached_probabilities(game)
        revenue_per_user_type = game.expected_publisher_revenue

    # write evaluation to .txt file if specified
    if EVALUATION_NUMBER % differential_evolution_creator.print_result_every_x_iterations == 0 or \
            EVALUATION_NUMBER <= differential_evolution_creator.print_result_for_the_first_x_iterations:
        price_base_product_rounded = []
        price_upgrade_rounded = []
        price_subscription_rounded = []
        for i in range(len(price_base_product)):
            price_base_product_rounded.append(round(price_base_product[i], 2))
            price_upgrade_rounded.append(round(price_upgrade[i], 2))
            price_subscription_rounded.append(round(price_subscription[i], 2))

        info_string = "ITERATION: " + str(EVALUATION_NUMBER) + "\t, Revenue: " + str(
            round(revenue_per_user_type, 4)) + ",\t Base product price: " + str(
            price_base_product_rounded) + ",\t Upgrade price: " + str(
            price_upgrade_rounded) + ",\t Subscription price: " + str(price_subscription_rounded)
        add_line_to_document(file_path, info_string)

    # return negated value since differential evolution is minimizing
    return -abs(revenue_per_user_type)


def get_solution_details(prices, *arguments):
    """
    Once a differential evolution solution has been found, this method calculates all necessary result details

    Parameters
    ----------
    prices : list[float]
        list containing all optimal prices (variables) found by differential evolution
    *arguments
        all other necessary arguments for one single differential evolution evaluation such as the DifferentialEvolutionCreator

    Returns
    -------
    price_base_product : list[float]
        optimal base product prices over time
    price_upgrade : list[float]
        optimal upgrade prices over time
    price_subscription : list[float]
        optimal subscription prices over time
    total_revenue : float
        expected total publisher revenue
    user_welfare : float
        expected total user welfare
    revenue_base_product_per_timestep : list[float]
        expected revenue through the base product in every timestep given all optimal prices
    revenue_upgrade_per_timestep : list[float]
        expected revenue through the upgrade in every timestep given all optimal prices
    revenue_subscription_per_timestep : list[float]
        expected revenue through subscription in every timestep given all optimal prices
    """
    differential_evolution_creator, file_path, single_number_of_user_valuations, single_arrivals_in_first_timestep, single_probability_of_second_quality_decay_element, single_engagement_factor_short_term_user, single_standard_deviation_valuation = arguments

    price_base_product, price_upgrade, price_subscription = get_price_vectors(prices, differential_evolution_creator)

    # do backward induction analogously to objective_maximize_revenue()
    if differential_evolution_creator.evolution_with_all_user_types_from_game:
        interval_length = (differential_evolution_creator.valuation_range[1] -
                           differential_evolution_creator.valuation_range[
                               0]) / single_number_of_user_valuations
        valuations = np.arange(differential_evolution_creator.valuation_range[0],
                               differential_evolution_creator.valuation_range[1] + interval_length, interval_length)
        quality_decay_factors = differential_evolution_creator.quality_decay_factors
        long_term_engagement_factors = [single_engagement_factor_short_term_user,
                                        differential_evolution_creator.engagement_factor_long_term_user]

        total_revenue = []
        user_welfare = []

        # only used for execution testing
        total_valuation_weight = 0
        total_prob_user_type = 0

        revenue_base_product_per_timestep = []
        revenue_upgrade_per_timestep = []
        revenue_subscription_per_timestep = []

        for i in range(0, differential_evolution_creator.n_max):
            revenue_base_product_per_timestep.append(0)
            revenue_upgrade_per_timestep.append(0)
            revenue_subscription_per_timestep.append(0)

        for v in range(len(valuations) - 1):
            lowerbound = valuations[v]
            upperbound = valuations[v + 1]
            valuation_mean = (differential_evolution_creator.valuation_range[0] +
                              differential_evolution_creator.valuation_range[1]) / 2

            if single_standard_deviation_valuation != 0:
                cdf_lowerboud = get_truncated_normal(mean=valuation_mean,
                                                     sd=single_standard_deviation_valuation,
                                                     low=differential_evolution_creator.valuation_range[0],
                                                     upp=differential_evolution_creator.valuation_range[1]).cdf(
                    lowerbound)
                cdf_upperbound = get_truncated_normal(mean=valuation_mean,
                                                      sd=single_standard_deviation_valuation,
                                                      low=differential_evolution_creator.valuation_range[0],
                                                      upp=differential_evolution_creator.valuation_range[1]).cdf(
                    upperbound)
                valuation_weight = cdf_upperbound - cdf_lowerboud
                total_valuation_weight += valuation_weight
                valuation = (lowerbound + upperbound) / 2
            # single_standard_deviation_valuation == 0
            else:
                valuation = valuation_mean
                valuation_weight = 1 / (len(valuations) - 1)
                total_valuation_weight += valuation_weight

            for i in range(len(quality_decay_factors)):
                for j in range(len(long_term_engagement_factors)):
                    user_type = UserType(None, long_term_engagement_factors[j], quality_decay_factors[i], valuation)
                    product_information = ProductInformation(price_base_product, price_upgrade, price_subscription,
                                                             [
                                                                 differential_evolution_creator.product_quality_base_product,
                                                                 differential_evolution_creator.product_quality_upgrade])

                    game = create_game(product_information, user_type, differential_evolution_creator.n_max,
                                       differential_evolution_creator.n_upgrade,
                                       differential_evolution_creator.price_strategy_type)
                    calculate_optimal_user_actions(game)

                    for arr_time in range(1, differential_evolution_creator.n_max + 1):
                        game.user_type.arrival_time = arr_time
                        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
                        test_reached_probabilities(game)

                        prob_user_type = get_probability_user_type(game.user_type,
                                                                   differential_evolution_creator,
                                                                   single_arrivals_in_first_timestep,
                                                                   single_probability_of_second_quality_decay_element,
                                                                   single_engagement_factor_short_term_user) * valuation_weight
                        total_prob_user_type += prob_user_type
                        total_revenue.append(game.expected_publisher_revenue * prob_user_type)
                        user_welfare.append(game.expected_user_welfare * prob_user_type)

                        # count actions of user type
                        timestep_count_revenue = game.n_max

                        while timestep_count_revenue > 0:
                            for current_user_state in game.user_states[timestep_count_revenue - 1]:
                                if current_user_state.probability_state_is_reached > 0:
                                    if current_user_state.best_action.subscribe_action == 1:
                                        revenue_subscription_per_timestep[timestep_count_revenue - 1] += \
                                            price_subscription[
                                                timestep_count_revenue - 1] * prob_user_type * current_user_state.probability_state_is_reached
                                        if timestep_count_revenue == game.n_max:
                                            revenue_subscription_per_timestep[
                                                timestep_count_revenue - 1] += current_user_state.expected_payment_in_future * prob_user_type * current_user_state.probability_state_is_reached
                                    if current_user_state.best_action.buy_action.base_product == 1:
                                        revenue_base_product_per_timestep[timestep_count_revenue - 1] += \
                                            price_base_product[
                                                timestep_count_revenue - 1] * prob_user_type * current_user_state.probability_state_is_reached
                                    if current_user_state.best_action.buy_action.upgrade == 1:
                                        revenue_upgrade_per_timestep[timestep_count_revenue - 1] += price_upgrade[
                                                                                                        timestep_count_revenue - 1] * prob_user_type * current_user_state.probability_state_is_reached
                            timestep_count_revenue -= 1

                        # clean game for next user type
                        game.expected_publisher_revenue = 0
                        game.expected_user_welfare = 0
                        timestep = game.n_max
                        while timestep > 0:
                            for user_state in game.user_states[timestep - 1]:
                                user_state.probability_state_is_reached = 0
                            timestep -= 1
        test_if_value_equal_one(total_valuation_weight, "total_valuation_weight")
        test_if_value_equal_one(total_prob_user_type, "total_prob_user_type")

    # evolution_with_all_user_types_from_game = False => evolution for single user type
    else:
        user_type = UserType(differential_evolution_creator.user_arrival_time,
                             differential_evolution_creator.user_engagement_factor,
                             differential_evolution_creator.user_quality_decay_factor,
                             differential_evolution_creator.user_valuation)
        product_information = ProductInformation(price_base_product, price_upgrade, price_subscription,
                                                 [differential_evolution_creator.product_quality_base_product,
                                                  differential_evolution_creator.product_quality_upgrade])

        game = create_game(product_information, user_type, differential_evolution_creator.n_max,
                           differential_evolution_creator.n_upgrade,
                           differential_evolution_creator.price_strategy_type)
        calculate_optimal_user_actions(game)
        calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
        test_reached_probabilities(game)

        total_revenue = [game.expected_publisher_revenue]
        user_welfare = [game.expected_user_welfare]

        # count actions of user type
        timestep_count_revenue = game.n_max
        revenue_base_product_per_timestep = []
        revenue_upgrade_per_timestep = []
        revenue_subscription_per_timestep = []

        for i in range(0, differential_evolution_creator.n_max):
            revenue_base_product_per_timestep.append(0)
            revenue_upgrade_per_timestep.append(0)
            revenue_subscription_per_timestep.append(0)

        while timestep_count_revenue > 0:
            for current_user_state in game.user_states[timestep_count_revenue - 1]:
                if current_user_state.probability_state_is_reached > 0:
                    if current_user_state.best_action.subscribe_action == 1:
                        revenue_subscription_per_timestep[timestep_count_revenue - 1] += price_subscription[
                                                                                             timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
                    if current_user_state.best_action.buy_action.base_product == 1:
                        revenue_base_product_per_timestep[timestep_count_revenue - 1] += price_base_product[
                                                                                             timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
                    if current_user_state.best_action.buy_action.upgrade == 1:
                        revenue_upgrade_per_timestep[timestep_count_revenue - 1] += price_upgrade[
                                                                                        timestep_count_revenue - 1] * current_user_state.probability_state_is_reached
            timestep_count_revenue -= 1

    return price_base_product, price_upgrade, price_subscription, sum(total_revenue), sum(
        user_welfare), revenue_base_product_per_timestep, revenue_upgrade_per_timestep, revenue_subscription_per_timestep


def create_bounds(differential_evolution_creator):
    """
    Creates the bounds for the differential evolution depending on the details of the creator

    I.e., the number of bounds is dependent on the price strategy type and other variables defined in the creator

    Parameters
    ----------
    differential_evolution_creator : DifferentialEvolutionCreator
        object containing all details about differential evolution specifics

    Returns
    -------
    bounds : list[list[int]]
        list of list of bounds (i.e., first element is lower bound, second is upper bound) for prices in DE
    """

    bounds = []

    # base price bounds
    if differential_evolution_creator.price_strategy_type == PriceStrategyType.BUY or \
            differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH:
        if differential_evolution_creator.play_different_ask_prices:
            if differential_evolution_creator.first_base_price_fixed is None or \
                    differential_evolution_creator.first_base_price_fixed == 0:
                bounds.append([differential_evolution_creator.price_bounds.buy_min,
                               differential_evolution_creator.price_bounds.buy_max])
            if differential_evolution_creator.is_prices_discounted:
                for i in range(1, differential_evolution_creator.n_max):
                    bounds.append([0, 1])

            else:
                for i in range(1, differential_evolution_creator.n_max):
                    bounds.append([differential_evolution_creator.price_bounds.buy_min,
                                   differential_evolution_creator.price_bounds.buy_max])

            # upgrade price bounds
            if differential_evolution_creator.first_upgrade_price_fixed is None or \
                    differential_evolution_creator.first_upgrade_price_fixed == 0:
                bounds.append([differential_evolution_creator.price_bounds.upgrade_min,
                               differential_evolution_creator.price_bounds.upgrade_max])
            if differential_evolution_creator.is_prices_discounted:
                for i in range(1, differential_evolution_creator.n_max - differential_evolution_creator.n_upgrade + 1):
                    bounds.append([0, 1])
            else:
                for i in range(1, differential_evolution_creator.n_max - differential_evolution_creator.n_upgrade + 1):
                    bounds.append([differential_evolution_creator.price_bounds.upgrade_min,
                                   differential_evolution_creator.price_bounds.upgrade_max])
        # play_different_ask_prices = False => initial model as in Dierks and Seuken (2020)
        else:
            bounds.append([differential_evolution_creator.price_bounds.buy_min,
                           differential_evolution_creator.price_bounds.buy_max])
            bounds.append([differential_evolution_creator.price_bounds.buy_min,
                           differential_evolution_creator.price_bounds.buy_max])
            bounds.append([differential_evolution_creator.price_bounds.upgrade_min,
                           differential_evolution_creator.price_bounds.upgrade_max])

    # subscription price bounds (single variable or is discounted in all cases)
    if differential_evolution_creator.price_strategy_type == PriceStrategyType.SUB or \
            differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH:
        if differential_evolution_creator.play_different_ask_prices:
            if differential_evolution_creator.is_subscription_price_variable:
                bounds.append([differential_evolution_creator.price_bounds.subscription_min,
                               differential_evolution_creator.price_bounds.subscription_max])
                for i in range(1, differential_evolution_creator.n_max):
                    bounds.append([0, 1])
            else:
                bounds.append([differential_evolution_creator.price_bounds.subscription_min,
                               differential_evolution_creator.price_bounds.subscription_max])
        # play_different_ask_prices = False => initial model as in Dierks and Seuken (2020)
        else:
            bounds.append([differential_evolution_creator.price_bounds.subscription_min,
                           differential_evolution_creator.price_bounds.subscription_max])

    if differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH_BUY:
        if differential_evolution_creator.play_different_ask_prices and differential_evolution_creator.is_subscription_price_variable:
            bounds.append([differential_evolution_creator.price_bounds.subscription_min,
                           differential_evolution_creator.price_bounds.subscription_max])
            for i in range(1, differential_evolution_creator.n_max):
                bounds.append([0, 1])
        else:
            bounds.append([differential_evolution_creator.price_bounds.subscription_min,
                           differential_evolution_creator.price_bounds.subscription_max])

    return bounds


def get_price_vectors(prices, differential_evolution_creator):
    """
    Creates the price vectors, depending on the price variables for DE and details in the creator

    Parameters
    ----------
    differential_evolution_creator : DifferentialEvolutionCreator
        object containing all details about differential evolution specifics

    Returns
    -------
    price_base_product : list[float]
        prices for the base product over time
    price_upgrade : list[float]
        prices for the upgrade over time
    price_subscription : list[float]
        prices for subscription over time

    """
    price_base_product = []
    price_upgrade = []
    price_subscription = []

    n_max = differential_evolution_creator.n_max
    n_upgrade = differential_evolution_creator.n_upgrade
    price_index = 0
    # base price
    if differential_evolution_creator.price_strategy_type == PriceStrategyType.BUY or \
            differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH:
        if differential_evolution_creator.play_different_ask_prices:
            if differential_evolution_creator.first_base_price_fixed is None \
                    or differential_evolution_creator.first_base_price_fixed == 0:
                price_base_product.append(prices[price_index])
                price_index += 1
            else:
                price_base_product.append(differential_evolution_creator.first_base_price_fixed)
            if differential_evolution_creator.is_prices_discounted:
                for i in range(1, n_max):
                    price_base_product.append(price_base_product[0] * prices[price_index])
                    price_index += 1
            else:
                for i in range(1, n_max):
                    price_base_product.append(prices[price_index])
                    price_index += 1

            # upgrade price
            for i in range(0, n_upgrade - 1):
                price_upgrade.append(HighPrice)
            if differential_evolution_creator.first_upgrade_price_fixed is None \
                    or differential_evolution_creator.first_upgrade_price_fixed == 0:
                price_upgrade.append(prices[price_index])
                price_index += 1
            else:
                price_upgrade.append(differential_evolution_creator.first_upgrade_price_fixed)
            if differential_evolution_creator.is_prices_discounted:
                for i in range(1, n_max - n_upgrade + 1):
                    price_upgrade.append(price_upgrade[n_upgrade - 1] * prices[price_index])
                    price_index += 1
            else:
                for i in range(1, n_max - n_upgrade + 1):
                    price_upgrade.append(prices[price_index])
                    price_index += 1
        # play_different_ask_prices = False => initial model as in Dierks and Seuken (2020)
        else:
            for i in range(0, n_upgrade - 1):
                price_base_product.append(prices[price_index])
            price_index += 1
            for i in range(n_upgrade, n_max + 1):
                price_base_product.append(prices[price_index])
            price_index += 1
            for i in range(0, n_upgrade - 1):
                price_upgrade.append(HighPrice)
            for i in range(n_upgrade, n_max + 1):
                price_upgrade.append(prices[price_index])
            price_index += 1
    else:
        price_base_product = [HighPrice] * n_max
        price_upgrade = [HighPrice] * n_max

    # subscription price (single variable or is discounted in all cases)
    if differential_evolution_creator.price_strategy_type == PriceStrategyType.SUB or \
            differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH:
        if differential_evolution_creator.play_different_ask_prices:
            price_subscription.append(prices[price_index])
            price_index += 1
            if differential_evolution_creator.is_subscription_price_variable:
                for i in range(1, n_max):
                    price_subscription.append(price_subscription[i - 1] * prices[price_index])
                    price_index += 1
            else:
                for i in range(1, n_max):
                    price_subscription.append(price_subscription[0])
        # play_different_ask_prices = False => initial model as in Dierks and Seuken (2020)
        else:
            for i in range(0, n_max):
                price_subscription.append(prices[price_index])
            price_index += 1
    else:
        price_subscription = [HighPrice] * n_max

    if differential_evolution_creator.price_strategy_type == PriceStrategyType.BOTH_BUY:
        price_base_product = differential_evolution_creator.base_price_for_both_buy
        price_upgrade = differential_evolution_creator.upgrade_price_for_both_buy
        price_subscription = []
        if differential_evolution_creator.play_different_ask_prices and differential_evolution_creator.is_subscription_price_variable:
            price_subscription.append(prices[price_index])
            price_index += 1
            for i in range(1, n_max):
                price_subscription.append(price_subscription[i - 1] * prices[price_index])
                price_index += 1
        else:
            for i in range(0, n_max):
                price_subscription.append(prices[price_index])
            price_index += 1

    return price_base_product, price_upgrade, price_subscription
