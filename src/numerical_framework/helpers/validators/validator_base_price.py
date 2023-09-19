import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorBasePrice(AbstractValidator):
    """
    A class defining the validator for the parameter base price from the config.ini
    """

    def validate(self, config, creator):
        try:
            base_price = json.loads(config.get('BACKWARD_INDUCTION', 'base_price'))
            if not len(base_price) == creator.n_max:
                return f"base_price in BACKWARD_INDUCTION must have length n_max ({creator.n_max}) but has length {len(base_price)}."
            for single_price in base_price:
                if not (isinstance(single_price, (float, int))):
                    return "elements of base_price in BACKWARD_INDUCTION must be floats or integers."
            creator.base_price_for_backward_induction = base_price
        except ValueError:
            return 'base_price in BACKWARD_INDUCTION must be a list of floats or integers.'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
