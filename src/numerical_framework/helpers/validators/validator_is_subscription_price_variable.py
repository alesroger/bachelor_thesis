from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorIsSubscriptionPriceVariable(AbstractValidator):
    """
    A class defining the validator for the parameter is subscription price variable from the config.ini
    """

    def validate(self, config, creator):
        if creator.play_different_ask_prices:
            try:
                creator.is_subscription_price_variable = config.getboolean('DIFFERENTIAL_EVOLUTION',
                                                                           'is_subscription_price_variable')
            except ValueError:
                return 'is_subscription_price_variable in DIFFERENTIAL_EVOLUTION in config.ini must be True or False'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
