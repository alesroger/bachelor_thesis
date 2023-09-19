import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserValuationsSingleMaxRevenue(AbstractValidator):
    """
    A class defining the validator for the parameter user valuations single max revenue from the config.ini
    """

    def validate(self, config, creator):
        try:
            valuations = json.loads(config.get('SINGLE_MAX_REVENUE', 'user_valuations'))
            for valuation in valuations:
                if not (isinstance(valuation, (int, float)) and 0 <= valuation):
                    return f"user_valuations in SINGLE_MAX_REVENUE must be a list of non-negative integers or floats, but one element is {valuation}."
            creator.user_valuations = valuations
        except ValueError:
            return 'user_valuations in SINGLE_MAX_REVENUE must be a list of integers in valuation_range of GAME_INFORMATION'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
