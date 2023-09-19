import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorValuationRange(AbstractValidator):
    """
    A class defining the validator for the parameter valuation range from the config.ini
    """

    def validate(self, config, creator):
        try:
            if len(json.loads(config.get('GAME_INFORMATION', 'valuation_range'))) != 2:
                return "valuation_range in GAME_INFORMATION must have length 2 defining lower and upper bound valuation."
            lower_bound_valuation = json.loads(config.get('GAME_INFORMATION', 'valuation_range'))[0]
            upper_bound_valuation = json.loads(config.get('GAME_INFORMATION', 'valuation_range'))[1]
            if lower_bound_valuation >= upper_bound_valuation:
                return "first element (lower bound) of valuation_range in GAME_INFORMATION must be smaller than second element (upper bound)."
            creator.valuation_range = [lower_bound_valuation, upper_bound_valuation]
        except ValueError:
            return "valuation_range bounds in GAME_INFORMATION in config.ini must be integers."
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
