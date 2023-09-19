import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorSubscriptionPrice(AbstractValidator):
    """
    A class defining the validator for the parameter subscription price from the config.ini
    """

    def validate(self, config, creator):
        try:
            subscription_price = json.loads(config.get('BACKWARD_INDUCTION', 'subscription_price'))
            if not len(subscription_price) == creator.n_max:
                return f"subscription_price in BACKWARD_INDUCTION must have length n_max ({creator.n_max}) but has length {len(subscription_price)}."
            for single_price in subscription_price:
                if not (isinstance(single_price, (float, int))):
                    return "elements of subscription_price in BACKWARD_INDUCTION must be floats or integers."
            creator.subscription_price_for_backward_induction = subscription_price
        except ValueError:
            return 'subscription_price in BACKWARD_INDUCTION must be a list of floats or integers.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
