import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserValuationsBackwardInduction(AbstractValidator):
    """
    A class defining the validator for the parameter user valuations backward indcution from the config.ini
    """

    def validate(self, config, creator):
        if not creator.induction_with_all_user_types_from_game:
            try:
                valuations = json.loads(config.get('BACKWARD_INDUCTION', 'user_valuations'))
                for valuation in valuations:
                    if not (isinstance(valuation, (int, float)) and 0 <= valuation):
                        return f"user_valuations in BACKWARD_INDUCTION must be a list of non-negative integers and floats, but one element is {valuation}."
                creator.user_valuations = valuations
            except ValueError:
                return 'user_valuations in BACKWARD_INDUCTION must be a list of non-negative integers and floats.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
