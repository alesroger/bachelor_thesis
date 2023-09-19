from abc import ABC


class AbstractResult(ABC):
    """
    Abstract class used to collect all result information
    """
    path_to_main_file = None
    number_of_user_valuations = None
    price_strategy_type = None
    expected_publisher_revenue = None
    expected_user_welfare = None
    expected_total_welfare = None
    price_base_product = None
    price_upgrade = None
    price_subscription = None
    revenue_base_product = None
    revenue_upgrade = None
    revenue_subscription = None
    n_max = None
    n_upgrade = None
    engagement_factor_short_term_user = None
    engagement_factor_long_term_user = None
    probability_short_term_user = None
    quality_decay_factors = None
    probability_of_second_quality_decay_factor = None
    valuation_range = None
    standard_deviation_valuation = None
    arrivals_in_first_timestep = None
    product_quality_base_product = None
    product_quality_upgrade = None
    files_results_are_written_to = None
    path_to_folder = None


class DifferentialEvolutionResult(AbstractResult):
    """
    Class used to collect all differential evolution result information
    """
    evolution_with_all_user_types_from_game = None
    start_time = None
    runtime = None
    number_of_evaluations = None
    is_prices_discounted = None
    is_subscription_price_variable = None
    price_bounds = None
    popsize = None
    differential_evolution_strategy = None
    user_valuation = None
    user_arrival_time = None
    user_quality_decay_factor = None
    user_engagement_factor = None
    base_price_for_differential_evolution = None
    upgrade_price_for_differential_evolution = None


class BackwardInductionResult(AbstractResult):
    """
    Class used to collect all backward induction result information
    """
    timestamp = None
    arrival_time = None
    valuation = None
    engagement_factor = None
    quality_decay_factor = None
    probability_user_type = None


class SingleMaximizeRevenueResult(AbstractResult):
    """
    Class used to collect all single maximize revenue result information
    """
    timestamp = None
    user_valuation = None
    user_arrival_time = None
    user_quality_decay_factor = None
    user_engagement_factor = None


class SearchMaximizeRevenueResult(AbstractResult):
    """
    Class used to collect all search maximize revenue result information
    """
    timestamp = None
    user_valuation = None
    user_arrival_time = None
    user_quality_decay_factor = None
    user_engagement_factor = None
