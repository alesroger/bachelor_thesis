from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorIsPricesDiscounted(AbstractValidator):
    """
    A class defining the validator for the parameter is prices discounted from the config.ini
    """

    def validate(self, config, creator):
        if creator.play_different_ask_prices:
            try:
                creator.is_prices_discounted = config.getboolean('DIFFERENTIAL_EVOLUTION',
                                                                 'is_prices_discounted')
            except ValueError:
                return 'is_prices_discounted in DIFFERENTIAL_EVOLUTION in config.ini must be True or False'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
