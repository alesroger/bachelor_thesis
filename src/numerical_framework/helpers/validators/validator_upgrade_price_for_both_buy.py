import json

from src.model.game.price_strategy_type import PriceStrategyType
from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUpgradePriceForBothBuy(AbstractValidator):
    """
    A class defining the validator for the parameter upgrade price for BOTH_BUY from the config.ini
    """

    def validate(self, config, creator):
        if creator.price_strategy_type == PriceStrategyType.BOTH_BUY:
            try:
                upgrade_price = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'upgrade_price'))
                if not len(upgrade_price) == creator.n_max:
                    return f"upgrade_price in DIFFERENTIAL_EVOLUTION must have length n_max({creator.n_max}) but has length {len(upgrade_price)}."
                for single_price in upgrade_price:
                    if not (isinstance(single_price, (float, int))):
                        return f"elements of upgrade_price in DIFFERENTIAL_EVOLUTION must be floats or integers but contains element {single_price}."
                creator.upgrade_price_for_both_buy = upgrade_price
            except ValueError:
                return 'upgrade_price in DIFFERENTIAL_EVOLUTION must be a list of floats or integers.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
