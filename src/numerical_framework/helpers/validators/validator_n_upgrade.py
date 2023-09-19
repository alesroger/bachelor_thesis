from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorNUpgrade(AbstractValidator):
    """
    A class defining the validator for the parameter n_upgrade from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.n_upgrade = config.getint('GAME_INFORMATION', 'n_upgrade')
            if creator.n_upgrade <= 0 or creator.n_upgrade > creator.n_max:
                return f'n_upgrade in GAME_INFORMATION must be an integer greater than 0 and smaller or equal to n_max ({creator.n_max}) but is {creator.n_upgrade}.'
        except ValueError:
            return 'n_upgrade in GAME_INFORMATION must be an integer greater than 0.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
