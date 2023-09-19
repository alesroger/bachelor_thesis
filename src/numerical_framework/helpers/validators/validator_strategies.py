import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorStrategies(AbstractValidator):
    """
    A class defining the validator for the parameter strategies from the config.ini
    """

    def validate(self, config, creator):
        try:
            strategies = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'differential_evolution_strategies'))
            if not len(strategies) > 0:
                return 'differential_evolution_strategies in DIFFERENTIAL_EVOLUTION in config.ini must contain at least one element'
            for strategy in strategies:
                if not (strategy in ['best1bin', 'best1exp', 'rand1exp', 'randtobest1exp', 'currenttobest1exp',
                                     'best2exp',
                                     'rand2exp', 'randtobest1bin', 'currenttobest1bin', 'best2bin', 'rand2bin',
                                     'rand1bin']):
                    return 'every element in differential_evolution_strategies in DIFFERENTIAL_EVOLUTION in config.ini must be one of best1bin, best1exp, rand1exp, randtobest1exp, currenttobest1exp, best2exp, rand2exp, randtobest1bin, currenttobest1bin, best2bin, rand2bin, rand1bin'
            creator.differential_evolution_strategies = strategies
        except ValueError:
            return 'every element in differential_evolution_strategies in DIFFERENTIAL_EVOLUTION in config.ini must be one of best1bin, best1exp, rand1exp, randtobest1exp, currenttobest1exp, best2exp, rand2exp, randtobest1bin, currenttobest1bin, best2bin, rand2bin, rand1bin'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
