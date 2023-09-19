from abc import ABC

from src.model.publisher.productinformation import ProductInformation
from src.numerical_framework.differential_evolution.differential_evolution import PriceBounds
from src.numerical_framework.helpers.validators.validator_arrival_time import ValidatorArrivalTime
from src.numerical_framework.helpers.validators.validator_base_price import ValidatorBasePrice
from src.numerical_framework.helpers.validators.validator_base_price_for_both_buy import ValidatorBasePriceForBothBuy
from src.numerical_framework.helpers.validators.validator_differential_evolution_with_all_user_types import \
    ValidatorDifferentialEvolutionWithAllUserTypes
from src.numerical_framework.helpers.validators.validator_engagement_factor_long_term_user import \
    ValidatorEngagementFactorLongTermUser
from src.numerical_framework.helpers.validators.validator_engagement_factor_short_term_user import \
    ValidatorEngagementFactorShortTermUser
from src.numerical_framework.helpers.validators.validator_files_backward_induction_results_are_written_to import \
    ValidatorFilesBackwardInductionResultsAreWrittenTo
from src.numerical_framework.helpers.validators.validator_files_differential_evolution_results_are_written_to import \
    ValidatorFilesDifferentialEvolutionResultsAreWrittenTo
from src.numerical_framework.helpers.validators.validator_files_single_max_revenue_results_are_written_to import \
    ValidatorFilesSingleMaxRevenueResultsAreWrittenTo
from src.numerical_framework.helpers.validators.validator_first_base_price_fixed import ValidatorFirstBasePriceFixed
from src.numerical_framework.helpers.validators.validator_first_upgrade_price_fixed import \
    ValidatorFirstUpgradePriceFixed
from src.numerical_framework.helpers.validators.validator_induction_with_all_user_types import \
    ValidatorInductionWithAllUserTypes
from src.numerical_framework.helpers.validators.validator_is_prices_discounted import ValidatorIsPricesDiscounted
from src.numerical_framework.helpers.validators.validator_is_subscription_price_variable import \
    ValidatorIsSubscriptionPriceVariable
from src.numerical_framework.helpers.validators.validator_n_max import ValidatorNMax
from src.numerical_framework.helpers.validators.validator_n_upgrade import ValidatorNUpgrade
from src.numerical_framework.helpers.validators.validator_number_of_iterations_per_evolution_type import \
    ValidatorNumberOfIterationsPerEvolutionType
from src.numerical_framework.helpers.validators.validator_number_of_user_valuations import \
    ValidatorNumberOfUserValuations
from src.numerical_framework.helpers.validators.validator_path_to_folder_backward_induction import \
    ValidatorPathToFolderBackwardInduction
from src.numerical_framework.helpers.validators.validator_path_to_folder_differential_evolution import \
    ValidatorPathToFolderDifferentialEvolution
from src.numerical_framework.helpers.validators.validator_path_to_folder_single_maximize_revenue import \
    ValidatorPathToFolderSingleMaxRevenue
from src.numerical_framework.helpers.validators.validator_play_different_ask_prices import \
    ValidatorPlayDifferentAskPrices
from src.numerical_framework.helpers.validators.validator_popsizes import ValidatorPopsizes
from src.numerical_framework.helpers.validators.validator_price_bounds import ValidatorPriceBounds
from src.numerical_framework.helpers.validators.validator_price_strategy import ValidatorPriceStrategy
from src.numerical_framework.helpers.validators.validator_print_result_every_x_iterations import \
    ValidatorPrintResultEveryXIterations
from src.numerical_framework.helpers.validators.validator_print_result_for_the_first_x_iterations import \
    ValidatorPrintResultForTheFirstXIterations
from src.numerical_framework.helpers.validators.validator_print_single_user_types import ValidatorPrintSingleUserTypes
from src.numerical_framework.helpers.validators.validator_print_user_types_combined import \
    ValidatorPrintUserTypesCombined
from src.numerical_framework.helpers.validators.validator_probability_of_second_quality_decay_factor import \
    ValidatorProbabilityOfSecondQualityDecayFactor
from src.numerical_framework.helpers.validators.validator_probability_short_term_user import \
    ValidatorProbabilityShortTermUser
from src.numerical_framework.helpers.validators.validator_product_quality_base_product import \
    ValidatorProductQualityBaseProduct
from src.numerical_framework.helpers.validators.validator_product_quality_upgrade import ValidatorProductQualityUpgrade
from src.numerical_framework.helpers.validators.validator_quality_decay_factors import ValidatorQualityDecayFactors
from src.numerical_framework.helpers.validators.validator_standard_deviation_valuation import \
    ValidatorStandardDeviationValuation
from src.numerical_framework.helpers.validators.validator_strategies import ValidatorStrategies
from src.numerical_framework.helpers.validators.validator_subscription_price import ValidatorSubscriptionPrice
from src.numerical_framework.helpers.validators.validator_upgrade_price import ValidatorUpgradePrice
from src.numerical_framework.helpers.validators.validator_upgrade_price_for_both_buy import \
    ValidatorUpgradePriceForBothBuy
from src.numerical_framework.helpers.validators.validator_user_arrival_time_backward_induction import \
    ValidatorUserArrivalTimesBackwardInduction
from src.numerical_framework.helpers.validators.validator_user_arrival_time_differential_evolution import \
    ValidatorUserArrivalTimeDifferentialEvolution
from src.numerical_framework.helpers.validators.validator_user_arrival_times_single_max_revenue import \
    ValidatorUserArrivalTimesSingleMaxRevenue
from src.numerical_framework.helpers.validators.validator_user_engagement_factor_differential_evolution import \
    ValidatorUserEngagementFactorDifferentialEvolution
from src.numerical_framework.helpers.validators.validator_user_engagement_factors_backward_induction import \
    ValidatorUserEngagementFactorsBackwardInduction
from src.numerical_framework.helpers.validators.validator_user_engagement_factors_single_max_revenue import \
    ValidatorUserEngagementFactorsSingleMaxRevenue
from src.numerical_framework.helpers.validators.validator_user_quality_decay_factor_differential_evolution import \
    ValidatorUserQualityDecayFactorDifferentialEvolution
from src.numerical_framework.helpers.validators.validator_user_quality_decay_factors_backward_induction import \
    ValidatorUserQualityDecayFactorsBackwardInduction
from src.numerical_framework.helpers.validators.validator_user_quality_decay_factors_single_max_revenue import \
    ValidatorUserQualityDecayFactorsSingleMaxRevenue
from src.numerical_framework.helpers.validators.validator_user_valuation_differential_evolution import \
    ValidatorUserValuationDifferentialEvolution
from src.numerical_framework.helpers.validators.validator_user_valuations_backward_induction import \
    ValidatorUserValuationsBackwardInduction
from src.numerical_framework.helpers.validators.validator_user_valuations_single_max_revenue import \
    ValidatorUserValuationsSingleMaxRevenue
from src.numerical_framework.helpers.validators.validator_valuation_range import ValidatorValuationRange


class AbstractGameCreator(ABC):
    """
    Abstract class used to collect all creator information from config.ini. For Details see the README.md
    """
    arrivals_in_first_timestep = None
    probability_of_second_quality_decay_element = None
    n_max = None
    n_upgrade = 7
    engagement_factor_short_term_user = None
    engagement_factor_long_term_user = None
    probability_short_term_user = None
    standard_deviation_valuation = None
    quality_decay_factors = None
    valuation_range = None
    product_quality_base_product = None
    product_quality_upgrade = None
    price_strategy_type = None
    files_results_are_written_to = None
    path_to_main_file = None
    path_to_folder = None
    number_of_user_valuations = None


class DifferentialEvolutionCreator(AbstractGameCreator):
    """
    Class used to collect all creator information for differential evolution from config.ini. For Details see the README.md
    """
    evolution_with_all_user_types_from_game = None
    play_different_ask_prices = True
    is_prices_discounted = True
    is_subscription_price_variable = False
    first_base_price_fixed = False
    first_upgrade_price_fixed = False
    price_bounds = PriceBounds(0, 300, 0, 300, 0, 300)
    print_result_every_x_iterations = None
    print_result_for_the_first_x_iterations = None
    popsizes = None
    differential_evolution_strategies = None
    name_main_file_without_ending = None
    number_of_iterations_per_evolution_type = None
    user_valuation = None
    user_arrival_time = None
    user_quality_decay_factor = None
    user_engagement_factor = None
    base_price_for_both_buy = None
    upgrade_price_for_both_buy = None


class BackwardInductionCreator(AbstractGameCreator):
    """
    Class used to collect all creator information for backward induction from config.ini. For Details see the README.md
    """
    base_price_for_backward_induction = None
    upgrade_price_for_backward_induction = None
    subscription_price_for_backward_induction = None
    induction_with_all_user_types_from_game = None
    print_user_types_combined = None
    print_single_user_types = None
    user_valuations = None
    user_arrival_times = None
    user_quality_decay_factors = None
    user_engagement_factors = None
    product_information = None


class SingleMaximizeRevenueCreator(AbstractGameCreator):
    """
    Class used to collect all creator information for single maximize revenue from config.ini. For Details see the README.md
    """
    user_arrival_times = None
    user_valuations = None
    user_engagement_factors = None
    user_quality_decay_factors = None


class SearchMaximizeRevenueCreator(AbstractGameCreator):
    """
    Class used to collect all creator information for search maximize revenue from config.ini. For Details see the README.md
    """
    path_to_folder = None


def get_and_validate_backward_induction_input_from_config_ini(config):
    """
    Validates all necessary input parameters needed for backward induction

    Parameters
    ----------
    config : RawConfigParser
        object containing all information from config.ini

    Returns
    -------
    backward_induction_creator : BackwardInductionCreator
        object containing all information converted from config.ini to creator element
    """
    validators = get_all_validators()
    error_message_combined = ""
    backward_induction_creator = BackwardInductionCreator()

    for validator in validators:
        if validator.backward_induction_needs_validation():
            error_message = validator.validate(config, backward_induction_creator)
            if error_message is not None:
                error_message_combined += "    - " + error_message + "\n"

    if not error_message_combined == "":
        raise Exception("The config.ini contains the following input errors: \n" + error_message_combined)

    backward_induction_creator.product_information = ProductInformation(
        backward_induction_creator.base_price_for_backward_induction,
        backward_induction_creator.upgrade_price_for_backward_induction,
        backward_induction_creator.subscription_price_for_backward_induction, [
            backward_induction_creator.product_quality_base_product,
            backward_induction_creator.product_quality_upgrade])
    return backward_induction_creator


def get_and_validate_differential_evolution_input_from_config_ini(config):
    """
    Validates all necessary input parameters needed for differential evolution

    Parameters
    ----------
    config : RawConfigParser
        object containing all information from config.ini

    Returns
    -------
    differential_evolution_creator : DifferentialEvolutionCreator
        object containing all information converted from config.ini to creator element
    """
    validators = get_all_validators()
    error_message_combined = ""
    differential_evolution_creator = DifferentialEvolutionCreator()

    for validator in validators:
        if validator.differential_evolution_needs_validation():
            error_message = validator.validate(config, differential_evolution_creator)
            if error_message is not None:
                error_message_combined += "    - " + error_message + "\n"

    if not error_message_combined == "":
        raise Exception("The config.ini contains the following input errors: \n" + error_message_combined)

    return differential_evolution_creator


def get_and_validate_single_max_revenue_input_from_config_ini(config):
    """
    Validates all necessary input parameters needed for single max revenue

    Parameters
    ----------
    config : RawConfigParser
        object containing all information from config.ini

    Returns
    -------
    single_max_revenue_creator : SingleMaximizeRevenueCreator
        object containing all information converted from config.ini to creator element
    """
    validators = get_all_validators()
    error_message_combined = ""
    single_max_revenue_creator = SingleMaximizeRevenueCreator()

    for validator in validators:
        if validator.single_maximize_revenue_needs_validation():
            error_message = validator.validate(config, single_max_revenue_creator)
            if error_message is not None:
                error_message_combined += "    - " + error_message + "\n"

    if not error_message_combined == "":
        raise Exception("The config.ini contains the following input errors: \n" + error_message_combined)

    return single_max_revenue_creator


def get_all_validators():
    """
    Collects all validators

    Returns
    -------
    list[AbstractValidator]
        list containing all validators needed to collect and validate the input from config.ini
    """
    return [
        ValidatorPathToFolderBackwardInduction(),
        ValidatorPathToFolderDifferentialEvolution(),
        ValidatorPathToFolderSingleMaxRevenue(),
        ValidatorPriceStrategy(),
        ValidatorArrivalTime(),
        ValidatorNMax(),
        ValidatorNUpgrade(),
        ValidatorQualityDecayFactors(),
        ValidatorProbabilityOfSecondQualityDecayFactor(),
        ValidatorEngagementFactorShortTermUser(),
        ValidatorEngagementFactorLongTermUser(),
        ValidatorProbabilityShortTermUser(),
        ValidatorValuationRange(),
        ValidatorStandardDeviationValuation(),
        ValidatorProductQualityBaseProduct(),
        ValidatorProductQualityUpgrade(),
        ValidatorNumberOfUserValuations(),
        ValidatorBasePrice(),
        ValidatorUpgradePrice(),
        ValidatorSubscriptionPrice(),
        ValidatorInductionWithAllUserTypes(),
        ValidatorPrintSingleUserTypes(),
        ValidatorPrintUserTypesCombined(),
        ValidatorUserValuationsBackwardInduction(),
        ValidatorUserArrivalTimesBackwardInduction(),
        ValidatorUserEngagementFactorsBackwardInduction(),
        ValidatorUserQualityDecayFactorsBackwardInduction(),
        ValidatorFilesBackwardInductionResultsAreWrittenTo(),
        ValidatorUserValuationsSingleMaxRevenue(),
        ValidatorUserArrivalTimesSingleMaxRevenue(),
        ValidatorUserEngagementFactorsSingleMaxRevenue(),
        ValidatorUserQualityDecayFactorsSingleMaxRevenue(),
        ValidatorFilesSingleMaxRevenueResultsAreWrittenTo(),
        ValidatorDifferentialEvolutionWithAllUserTypes(),
        ValidatorUserValuationDifferentialEvolution(),
        ValidatorUserArrivalTimeDifferentialEvolution(),
        ValidatorUserEngagementFactorDifferentialEvolution(),
        ValidatorUserQualityDecayFactorDifferentialEvolution(),
        ValidatorPlayDifferentAskPrices(),
        ValidatorIsPricesDiscounted(),
        ValidatorIsSubscriptionPriceVariable(),
        ValidatorFirstBasePriceFixed(),
        ValidatorFirstUpgradePriceFixed(),
        ValidatorPriceBounds(),
        ValidatorPrintResultEveryXIterations(),
        ValidatorPrintResultForTheFirstXIterations(),
        ValidatorPopsizes(),
        ValidatorStrategies(),
        ValidatorFilesDifferentialEvolutionResultsAreWrittenTo(),
        ValidatorNumberOfIterationsPerEvolutionType(),
        ValidatorBasePriceForBothBuy(),
        ValidatorUpgradePriceForBothBuy()]
