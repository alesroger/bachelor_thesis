import json

from src.model.game.price_strategy_type import PriceStrategyType
from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorBasePriceForBothBuy(AbstractValidator):
    """
    A class defining the validator for the parameter base price for the case BOTH_BUY (in DE) from the config.ini
    """

    def validate(self, config, creator):
        if creator.price_strategy_type == PriceStrategyType.BOTH_BUY:
            try:
                base_price = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'base_price'))
                if not len(base_price) == creator.n_max:
                    return f"base_price in DIFFERENTIAL_EVOLUTION in config.ini must have length n_max ({creator.n_max}) but has length {len(base_price)}."
                for single_price in base_price:
                    if not (isinstance(single_price, (float, int))):
                        return f"elements of base_price in DIFFERENTIAL_EVOLUTION in config.ini must be floats or integers but contains element {single_price}."
                creator.base_price_for_both_buy = base_price
            except ValueError:
                return 'base_price in DIFFERENTIAL_EVOLUTION in config.ini must be a list of floats or integers.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
