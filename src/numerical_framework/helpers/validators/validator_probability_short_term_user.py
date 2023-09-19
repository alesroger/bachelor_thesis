from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorProbabilityShortTermUser(AbstractValidator):
    """
    A class defining the validator for the parameter probability short term user from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.probability_short_term_user = config.getfloat('GAME_INFORMATION', 'probability_short_term_user')

            if not (0 <= creator.probability_short_term_user <= 1):
                return f"probability_short_term_user in GAME_INFORMATION in config.ini must be float (or integer) between 0 and 1, but is {creator.probability_short_term_user}."

        except ValueError:
            return f'probability_short_term_user in GAME_INFORMATION in config.ini must be float (or integer) between 0 and 1.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
