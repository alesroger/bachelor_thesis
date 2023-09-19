from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPlayDifferentAskPrices(AbstractValidator):
    """
    A class defining the validator for the parameter play different ask prices from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.play_different_ask_prices = config.getboolean('DIFFERENTIAL_EVOLUTION',
                                                                  'play_different_ask_prices')
        except ValueError:
            return 'play_different_ask_prices in DIFFERENTIAL_EVOLUTION in config.ini must be True or False.'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
