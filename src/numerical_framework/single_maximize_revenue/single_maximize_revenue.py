from datetime import datetime

from src.model.game.game import create_game
from src.model.publisher.productinformation import ProductInformation
from src.model.user.user_type import UserType
from src.numerical_framework.backward_induction.backward_induction import calculate_optimal_user_actions, \
    calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare
from src.numerical_framework.helpers.high_price import HighPrice
from src.numerical_framework.helpers.output_files_helper import write_single_maximize_revenue_result
from src.numerical_framework.helpers.tests_during_execution import test_reached_probabilities
from src.numerical_framework.result.result import SingleMaximizeRevenueResult


def single_maximize_revenue(single_maximize_revenue_creator):
    """
    Executes the whole single maximize revenue process, creates the result object and writes it to .csv files

    Parameters
    ----------
    single_maximize_revenue_creator : SingleMaximizeRevenueCreator
        object containing all details about single maximize revenue specifics
    """
    for valuation in single_maximize_revenue_creator.user_valuations:
        for arrival_time in single_maximize_revenue_creator.user_arrival_times:
            for engagement_factor in single_maximize_revenue_creator.user_engagement_factors:
                for quality_decay_factor in single_maximize_revenue_creator.user_quality_decay_factors:
                    user_type = UserType(arrival_time, engagement_factor, quality_decay_factor, valuation)

                    optimal_base_product_prices = []
                    optimal_upgrade_prices = []

                    # get exact prices user is willing to pay for base product and upgrade in each timestep
                    for timestep in range(arrival_time, single_maximize_revenue_creator.n_max + 1):
                        optimal_base_product_prices.append(
                            calculate_highest_possible_base_price(user_type, timestep, single_maximize_revenue_creator))
                        if timestep >= single_maximize_revenue_creator.n_upgrade:
                            optimal_upgrade_prices.append(
                                calculate_highest_possible_upgrade_price(user_type, timestep,
                                                                         single_maximize_revenue_creator))

                    price_base_product = []
                    price_upgrade = []
                    price_subscription = [HighPrice] * single_maximize_revenue_creator.n_max

                    # calculate publisher revenue and user welfare with price vector forcing the user to buy base product and upgrade in the first possible timestep
                    for i in range(1, arrival_time):
                        price_base_product.append(HighPrice)

                    for i in range(1, max(arrival_time, single_maximize_revenue_creator.n_upgrade)):
                        price_upgrade.append(HighPrice)

                    for i in range(arrival_time, single_maximize_revenue_creator.n_max + 1):
                        price_base_product.append(optimal_base_product_prices[0] - 0.000001)

                    for i in range(max(arrival_time, single_maximize_revenue_creator.n_upgrade),
                                   single_maximize_revenue_creator.n_max + 1):
                        price_upgrade.append(optimal_upgrade_prices[0] - 0.000001)

                    product_information = ProductInformation(price_base_product, price_upgrade, price_subscription, [
                        single_maximize_revenue_creator.product_quality_base_product,
                        single_maximize_revenue_creator.product_quality_upgrade])

                    game = create_game(product_information,
                                       user_type, single_maximize_revenue_creator.n_max,
                                       single_maximize_revenue_creator.n_upgrade,
                                       single_maximize_revenue_creator.price_strategy_type)

                    # do backward induction
                    calculate_optimal_user_actions(game)
                    calculate_probabilities_states_are_reached_and_publisher_revenue_and_user_welfare(game)
                    test_reached_probabilities(game)

                    timestep_count_actions = game.n_max
                    revenue_base_product_per_timestep = []
                    revenue_upgrade_per_timestep = []
                    revenue_subscription_per_timestep = []

                    for i in range(0, game.n_max):
                        revenue_base_product_per_timestep.append(0)
                        revenue_upgrade_per_timestep.append(0)
                        revenue_subscription_per_timestep.append(0)

                    while timestep_count_actions > 0:
                        for current_user_state in game.user_states[timestep_count_actions - 1]:
                            if current_user_state.probability_state_is_reached > 0:
                                if current_user_state.best_action.buy_action.base_product == 1:
                                    revenue_base_product_per_timestep[timestep_count_actions - 1] += \
                                        product_information.price_base_product[
                                            timestep_count_actions - 1] * current_user_state.probability_state_is_reached
                                if current_user_state.best_action.buy_action.upgrade == 1:
                                    revenue_upgrade_per_timestep[timestep_count_actions - 1] += \
                                        product_information.price_upgrade[
                                            timestep_count_actions - 1] * current_user_state.probability_state_is_reached
                        timestep_count_actions -= 1

                    # write result to .csv file
                    single_maximize_revenue_result = SingleMaximizeRevenueResult()
                    single_maximize_revenue_result.timestamp = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
                    single_maximize_revenue_result.user_valuation = valuation
                    single_maximize_revenue_result.user_arrival_time = arrival_time
                    single_maximize_revenue_result.user_engagement_factor = engagement_factor
                    single_maximize_revenue_result.user_quality_decay_factor = quality_decay_factor
                    single_maximize_revenue_result.path_to_main_file = single_maximize_revenue_creator.path_to_main_file
                    single_maximize_revenue_result.price_base_product = price_base_product
                    single_maximize_revenue_result.price_upgrade = price_upgrade
                    single_maximize_revenue_result.price_subscription = price_subscription
                    single_maximize_revenue_result.expected_publisher_revenue = game.expected_publisher_revenue
                    single_maximize_revenue_result.expected_user_welfare = game.expected_user_welfare
                    single_maximize_revenue_result.expected_total_welfare = game.expected_publisher_revenue + game.expected_user_welfare
                    single_maximize_revenue_result.n_max = single_maximize_revenue_creator.n_max
                    single_maximize_revenue_result.n_upgrade = single_maximize_revenue_creator.n_upgrade
                    single_maximize_revenue_result.product_quality_base_product = single_maximize_revenue_creator.product_quality_base_product
                    single_maximize_revenue_result.product_quality_upgrade = single_maximize_revenue_creator.product_quality_upgrade
                    single_maximize_revenue_result.files_results_are_written_to = single_maximize_revenue_creator.files_results_are_written_to
                    single_maximize_revenue_result.path_to_folder = single_maximize_revenue_creator.path_to_folder
                    single_maximize_revenue_result.revenue_base_product = revenue_base_product_per_timestep
                    single_maximize_revenue_result.revenue_upgrade = revenue_upgrade_per_timestep
                    single_maximize_revenue_result.revenue_subscription = revenue_subscription_per_timestep
                    write_single_maximize_revenue_result(single_maximize_revenue_result)


def calculate_highest_possible_base_price(user_type, timestep, single_maximize_revenue_creator):
    """
    Finds the highest possible base price for which the user buys the base product, maximizing publisher revenue, minimizing user welfare


    Parameters
    ----------
    user_type : UserType
        the users type
    timestep : int
        timestep for which calculation has to be made
    single_maximize_revenue_creator : SingleMaximizeRevenueCreator
        object containing all details about single maximize revenue specifics


    Returns
    -------
    highest_possible_base_price : float
        the highest price for which the user will buy the base product
    """
    if timestep < single_maximize_revenue_creator.n_upgrade:
        utility_before_upgrade = (user_type.quality_decay_factor ** (
                timestep - 1)) * single_maximize_revenue_creator.product_quality_base_product * (
                                         1 - user_type.quality_decay_factor ** (
                                         single_maximize_revenue_creator.n_upgrade - timestep) * user_type.engagement_factor ** (
                                                 single_maximize_revenue_creator.n_upgrade - timestep)) / (
                                         1 - user_type.engagement_factor * user_type.quality_decay_factor)
        probability_after_upgrade = user_type.engagement_factor * (
                1 - user_type.engagement_factor ** (
                single_maximize_revenue_creator.n_upgrade - timestep)) + user_type.engagement_factor ** (
                                            single_maximize_revenue_creator.n_upgrade - timestep)
        utility_after_upgrade = (user_type.quality_decay_factor ** (
                single_maximize_revenue_creator.n_upgrade - 1) * single_maximize_revenue_creator.product_quality_base_product) / (
                                        1 - user_type.engagement_factor * user_type.quality_decay_factor)
        sum_utility = utility_before_upgrade + probability_after_upgrade * utility_after_upgrade
        return max(sum_utility * user_type.valuation, 0)
    else:
        utility_after_upgrade = (user_type.quality_decay_factor ** (
                timestep - 1) * single_maximize_revenue_creator.product_quality_base_product) / (
                                        1 - user_type.engagement_factor * user_type.quality_decay_factor)
        return max(utility_after_upgrade * user_type.valuation, 0)


def calculate_highest_possible_upgrade_price(user_type, timestep, single_maximize_revenue_creator):
    """
    Finds the highest possible base price for which the user buys the upgrade, maximizing publisher revenue, minimizing user welfare


    Parameters
    ----------
    user_type : UserType
        the users type
    timestep : int
        timestep for which calculation has to be made
    single_maximize_revenue_creator : SingleMaximizeRevenueCreator
        object containing all details about single maximize revenue specifics


    Returns
    -------
    highest_possible_upgrade_price : float
        the highest price for which the user will buy the upgrade
    """

    utility_upgrade = (user_type.quality_decay_factor ** (
            timestep - single_maximize_revenue_creator.n_upgrade) * single_maximize_revenue_creator.product_quality_upgrade) / (
                              1 - user_type.engagement_factor * user_type.quality_decay_factor)
    return min(utility_upgrade * user_type.valuation, HighPrice)
