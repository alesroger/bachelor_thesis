from src.model.game.price_strategy_type import PriceStrategyType
from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPriceStrategy(AbstractValidator):
    """
    A class defining the validator for the parameter price strategy from the config.ini
    """

    def validate(self, config, creator):
        try:
            price_strategy_name = config.get('GAME_INFORMATION', 'price_strategy_type')
            if price_strategy_name == PriceStrategyType.BUY or price_strategy_name == PriceStrategyType.BOTH or price_strategy_name == PriceStrategyType.SUB or price_strategy_name == PriceStrategyType.BOTH_BUY:
                creator.price_strategy_type = price_strategy_name
            else:
                return f'price_strategy_type in section GAME_INFORMATION must be BUY, SUB, BOTH or BOTH_BUY but is {price_strategy_name}.'
        except ValueError:
            return 'price_strategy_type in section GAME_INFORMATION must be BUY, SUB, BOTH or BOTH_BUY'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
