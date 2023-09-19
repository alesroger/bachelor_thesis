import json

from src.numerical_framework.differential_evolution.differential_evolution import PriceBounds
from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPriceBounds(AbstractValidator):
    """
    A class defining the validator for the parameter price bounds from the config.ini
    """

    def validate(self, config, creator):
        try:
            lower_bound_base_product = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_base_product'))[0]
            upper_bound_base_product = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_base_product'))[1]
            if not (isinstance(lower_bound_base_product, int) and isinstance(upper_bound_base_product,
                                                                             int) and 0 <= lower_bound_base_product <= upper_bound_base_product):
                return "price_bounds_base_product in DIFFERENTIAL_EVOLUTION in config.ini must be integers. lower bound must be greater or equals 0 and not greater than upper bound."

            lower_bound_upgrade = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_upgrade'))[0]
            upper_bound_upgrade = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_upgrade'))[1]
            if not (isinstance(lower_bound_upgrade, int) and isinstance(upper_bound_upgrade,
                                                                        int) and 0 <= lower_bound_upgrade <= upper_bound_upgrade):
                return "price_bounds_upgrade in DIFFERENTIAL_EVOLUTION in config.ini must be integers. lower bound must be greater or equals 0 and not greater than upper bound."

            lower_bound_subscription = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_subscription'))[0]
            upper_bound_subscription = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'price_bounds_subscription'))[1]
            if not (isinstance(lower_bound_subscription, int) and isinstance(upper_bound_subscription,
                                                                             int) and 0 <= lower_bound_subscription <= upper_bound_subscription):
                return "price_bounds_subscription in DIFFERENTIAL_EVOLUTION in config.ini must be integers. lower bound must be greater or equals 0 and not greater than upper bound."

            creator.price_bounds = PriceBounds(lower_bound_base_product,
                                               upper_bound_base_product,
                                               lower_bound_upgrade, upper_bound_upgrade,
                                               lower_bound_subscription,
                                               upper_bound_subscription)
        except ValueError:
            return "price_bounds_base_product, price_bounds_upgrade, price_bounds_subscription in DIFFERENTIAL_EVOLUTION must be 3 lists of length 2 with lower and upper bound for base_product, upgrade and subscription"
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
