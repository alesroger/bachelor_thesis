from datetime import datetime

import numpy as np

from src.model.game.game import create_game
from src.model.game.price_strategy_type import PriceStrategyType
from src.model.publisher.productinformation import ProductInformation
from src.model.user.user_type import get_truncated_normal, UserType, get_probability_user_type
from src.numerical_framework.backward_induction.backward_induction import calculate_optimal_user_actions, \
    calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare
from src.numerical_framework.helpers.high_price import HighPrice
from src.numerical_framework.helpers.output_files_helper import write_search_maximize_revenue_result
from src.numerical_framework.helpers.tests_during_execution import test_reached_probabilities, \
    test_if_value_equal_one
from src.numerical_framework.result.result import SearchMaximizeRevenueResult
from src.numerical_framework.single_maximize_revenue.single_maximize_revenue import \
    calculate_highest_possible_base_price, calculate_highest_possible_upgrade_price


def search_maximize_revenue(search_maximize_revenue_creator):
    """
    Executes the whole search maximize revenue process, creates the result object and writes it to .csv files

    Note that this approach is hardcoded and cannot be changed trough the details in the config.ini

    Parameters
    ----------
    search_maximize_revenue_creator : SearchMaximizeRevenueCreator
        object containing all details search maximize specifics
    """

    # force optimization type BUY because the following calculations just hold if no subscription option is offered
    price_strategy_type = PriceStrategyType.BUY
    n_max = 2
    n_upgrade = 2
    search_maximize_revenue_creator.n_max = n_max
    search_maximize_revenue_creator.n_upgrade = n_upgrade
    search_maximize_revenue_creator.product_quality_base_product = 1
    search_maximize_revenue_creator.product_quality_upgrade = 0.5
    arrivals_in_first_timestep = 5
    probability_of_second_quality_decay_element = 0.8

    number_of_user_valuations = 2
    quality_decay_factors = [0.85, 0.9, 0.95]
    engagement_factor_short_term_user = 0.5
    engagement_factor_long_term_user = 0.9
    probability_short_term_user = 0.8
    valuation_range = [0, 50]
    standard_deviation_valuation = 10

    search_maximize_revenue_creator.quality_decay_factors = quality_decay_factors
    search_maximize_revenue_creator.engagement_factor_long_term_user = engagement_factor_long_term_user
    search_maximize_revenue_creator.probability_short_term_user = probability_short_term_user

    interval_length = (valuation_range[1] - valuation_range[0]) / number_of_user_valuations
    valuations = np.arange(valuation_range[0], valuation_range[1] + interval_length, interval_length)
    engagement_factors = [engagement_factor_short_term_user, engagement_factor_long_term_user]

    revenue_base_product_per_timestep = []
    revenue_upgrade_per_timestep = []
    revenue_subscription_per_timestep = []
    revenue_base_product_per_timestep_single_user_type = []
    revenue_upgrade_per_timestep_single_user_type = []
    revenue_subscription_per_timestep_single_user_type = []
    total_valuation_weight = 0
    total_prob_user_type = 0

    potentially_optimal_base_price = []
    potentially_optimal_upgrade_price = []

    for i in range(0, n_max):
        potentially_optimal_base_price.append([])
    for i in range(0, n_max):
        potentially_optimal_upgrade_price.append([])

    for i in range(0, n_max):
        revenue_base_product_per_timestep.append(0)
        revenue_upgrade_per_timestep.append(0)
        revenue_subscription_per_timestep.append(0)
        revenue_base_product_per_timestep_single_user_type.append(0)
        revenue_upgrade_per_timestep_single_user_type.append(0)
        revenue_subscription_per_timestep_single_user_type.append(0)

    for v in range(len(valuations) - 1):
        lowerbound = valuations[v]
        upperbound = valuations[v + 1]
        valuation_mean = (valuation_range[0] + valuation_range[1]) / 2

        cdf_lowerboud = get_truncated_normal(mean=valuation_mean,
                                             sd=standard_deviation_valuation,
                                             low=valuation_range[0],
                                             upp=valuation_range[1]).cdf(lowerbound)
        cdf_upperbound = get_truncated_normal(mean=valuation_mean,
                                              sd=standard_deviation_valuation,
                                              low=valuation_range[0],
                                              upp=valuation_range[1]).cdf(upperbound)
        valuation_weight = cdf_upperbound - cdf_lowerboud
        total_valuation_weight += valuation_weight

        valuation = (lowerbound + upperbound) / 2
        valuation = valuation

        for quality_decay_factor in quality_decay_factors:
            for engagement_factor in engagement_factors:
                user_type = UserType(None, engagement_factor, quality_decay_factor, valuation)
                optimal_base_product_prices = []
                optimal_upgrade_prices = []

                # get exact prices user is willing to pay for base product and upgrade in each timestep
                for timestep in range(1, n_max + 1):

                    optimal_base_price = calculate_highest_possible_base_price(user_type, timestep,
                                                                               search_maximize_revenue_creator)
                    optimal_base_product_prices.append(optimal_base_price)

                    for i in range(timestep, n_max + 1):
                        potentially_optimal_base_price[i - 1].append(optimal_base_price - 0.000001)

                    if timestep >= n_upgrade:
                        optimal_uprade_price = calculate_highest_possible_upgrade_price(user_type, timestep,
                                                                                        search_maximize_revenue_creator)
                        optimal_upgrade_prices.append(optimal_uprade_price)

                        for i in range(timestep, n_max + 1):
                            potentially_optimal_upgrade_price[i - 1].append(optimal_uprade_price - 0.000001)

    best_revenue = 0
    best_welfare = 0
    best_base_price = []
    best_upgrade_price = []
    total_revenue = []
    user_welfare = []

    for base_price_1 in potentially_optimal_base_price[0]:
        for base_price_2 in potentially_optimal_base_price[1]:
            for upgrade_price_2 in potentially_optimal_upgrade_price[1]:
                base_price = [base_price_1, base_price_2]
                upgrade_price = [HighPrice, upgrade_price_2]
                subscription_price = [HighPrice, HighPrice]
                product_information = ProductInformation(base_price, upgrade_price, subscription_price,
                                                         [search_maximize_revenue_creator.product_quality_base_product,
                                                          search_maximize_revenue_creator.product_quality_upgrade])

                for engagement_factor in engagement_factors:
                    for quality_decay_factor in quality_decay_factors:
                        for valuation in [12.5, 37.5]:
                            user_type = UserType(None, engagement_factor, quality_decay_factor,
                                                 valuation)

                            game = create_game(product_information, user_type, n_max, n_upgrade, price_strategy_type)
                            calculate_optimal_user_actions(game)

                            for arr_time in range(1, n_max + 1):
                                game.user_type.arrival_time = arr_time
                                calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
                                test_reached_probabilities(game)
                                valuation_weight = 0.5

                                prob_user_type = get_probability_user_type(game.user_type,
                                                                           search_maximize_revenue_creator,
                                                                           arrivals_in_first_timestep,
                                                                           probability_of_second_quality_decay_element,
                                                                           engagement_factor_short_term_user) * valuation_weight

                                total_revenue += [game.expected_publisher_revenue * prob_user_type]
                                user_welfare += [game.expected_user_welfare * prob_user_type]
                                total_prob_user_type += prob_user_type

                                # set values to 0 again
                                game.expected_publisher_revenue = 0
                                game.expected_user_welfare = 0
                                timestep = game.n_max

                                while timestep > 0:
                                    for user_state in game.user_states[timestep - 1]:
                                        user_state.probability_state_is_reached = 0
                                    timestep -= 1
                test_if_value_equal_one(total_prob_user_type, "total_prob_user_type")
                total_prob_user_type = 0

                if sum(total_revenue) > best_revenue:
                    new_best_revenue = sum(total_revenue)
                    best_revenue = new_best_revenue
                    best_welfare = sum(user_welfare)
                    best_base_price = base_price
                    best_upgrade_price = upgrade_price
                total_revenue = []
                user_welfare = []

    # write single max revenue results to .csv file
    search_maximize_revenue_result = SearchMaximizeRevenueResult()
    search_maximize_revenue_result.timestamp = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
    search_maximize_revenue_result.user_valuation = str([12.5, 37.5])
    search_maximize_revenue_result.user_engagement_factor = engagement_factors
    search_maximize_revenue_result.user_quality_decay_factor = quality_decay_factors
    search_maximize_revenue_result.user_arrival_time = str([1, 2])
    search_maximize_revenue_result.expected_publisher_revenue = best_revenue
    search_maximize_revenue_result.expected_user_welfare = best_welfare
    search_maximize_revenue_result.expected_total_welfare = best_welfare + best_revenue
    search_maximize_revenue_result.price_base_product = best_base_price
    search_maximize_revenue_result.price_upgrade = best_upgrade_price
    search_maximize_revenue_result.n_max = n_max
    search_maximize_revenue_result.n_upgrade = n_upgrade
    search_maximize_revenue_result.product_quality_base_product = search_maximize_revenue_creator.product_quality_base_product
    search_maximize_revenue_result.product_quality_upgrade = search_maximize_revenue_creator.product_quality_upgrade
    search_maximize_revenue_result.path_to_main_file = search_maximize_revenue_creator.path_to_main_file
    write_search_maximize_revenue_result(search_maximize_revenue_result)
