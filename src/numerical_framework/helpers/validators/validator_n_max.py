from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorNMax(AbstractValidator):
    """
    A class defining the validator for the parameter n_max from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.n_max = config.getint('GAME_INFORMATION', 'n_max')
            if creator.n_max <= 0:
                return f"n_max in GAME_INFORMATION must be an integer greater than 0 but is {creator.n_max}"
        except ValueError:
            return 'n_max in GAME_INFORMATION must be an integer greater than 0.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
