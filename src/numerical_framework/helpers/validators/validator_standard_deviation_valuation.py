import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorStandardDeviationValuation(AbstractValidator):
    """
    A class defining the validator for the parameter standard deviation valuation from the config.ini
    """

    def validate(self, config, creator):
        if creator.valuation_range is not None:
            try:
                standard_deviation_valuation = json.loads(
                    config.get('GAME_INFORMATION', 'standard_deviation_valuation'))
                if not len(standard_deviation_valuation) > 0:
                    return "standard_deviation_valuation in GAME_INFORMATION in config.ini must contain at least one element."
                for single_valuation_deviation in standard_deviation_valuation:
                    if not (isinstance(single_valuation_deviation, (float, int)) and single_valuation_deviation <= (
                            creator.valuation_range[1] - creator.valuation_range[0]) / 2):
                        return f"elements of standard_deviation_valuation in GAME_INFORMATION in config.ini must be smaller or equal to half of the range defined by the valuation range ({creator.valuation_range[1] - creator.valuation_range[0]}), but one element is {single_valuation_deviation}."
                creator.standard_deviation_valuation = standard_deviation_valuation
            except ValueError:
                return 'standard_deviation_valuation in GAME_INFORMATION in config.ini must be a list of floats or ints in valuation range.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
