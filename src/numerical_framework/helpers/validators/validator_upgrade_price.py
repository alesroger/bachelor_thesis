import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUpgradePrice(AbstractValidator):
    """
    A class defining the validator for the parameter upgrade price from the config.ini
    """

    def validate(self, config, creator):
        try:
            upgrade_price = json.loads(config.get('BACKWARD_INDUCTION', 'upgrade_price'))
            if not len(upgrade_price) == creator.n_max:
                return f"upgrade_price in BACKWARD_INDUCTION must have length n_max ({creator.n_max}) but has length {len(upgrade_price)}."
            for single_price in upgrade_price:
                if not (isinstance(single_price, (float, int))):
                    return "elements of upgrade_price in BACKWARD_INDUCTION  must be floats or integers."
            creator.upgrade_price_for_backward_induction = upgrade_price
        except ValueError:
            return 'upgrade_price in BACKWARD_INDUCTION must be a list of floats or integers.'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
