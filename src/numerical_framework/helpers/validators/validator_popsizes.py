import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPopsizes(AbstractValidator):
    """
    A class defining the validator for the parameter popsizes from the config.ini
    """

    def validate(self, config, creator):
        try:
            popsizes = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'popsizes'))
            if not len(popsizes) > 0:
                return 'popsizes in DIFFERENTIAL_EVOLUTION in config.ini must contain at least one element'
            for i in range(len(popsizes)):
                if not (isinstance(popsizes[i], int) and popsizes[i] > 0):
                    return 'popsizes in DIFFERENTIAL_EVOLUTION in config.ini must be positive integers'
            creator.popsizes = popsizes
        except ValueError:
            return 'popsizes in DIFFERENTIAL_EVOLUTION in config.ini must be a list of positive integers'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
