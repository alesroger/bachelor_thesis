import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorNumberOfUserValuations(AbstractValidator):
    """
    A class defining the validator for the parameter number of user valuations from the config.ini
    """

    def validate(self, config, creator):
        try:
            number_of_user_valuations = json.loads(config.get('GAME_INFORMATION', 'number_of_user_valuations'))
            if not len(number_of_user_valuations) > 0:
                return "number_of_user_valuations in GAME_INFORMATION in config.ini must contain at least one element"
            for single_number_of_user_valuations in number_of_user_valuations:
                if not (isinstance(single_number_of_user_valuations, int) and single_number_of_user_valuations > 0):
                    return f"elements of number_of_user_valuations in GAME_INFORMATION in config.ini must be integers bigger than 0, but contains element {single_number_of_user_valuations}."
            creator.number_of_user_valuations = number_of_user_valuations
        except ValueError:
            return 'number_of_user_valuations in GAME_INFORMATION must be a list of floats or integers bigger than 0.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
