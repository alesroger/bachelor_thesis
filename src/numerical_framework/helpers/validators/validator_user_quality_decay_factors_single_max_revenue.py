import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserQualityDecayFactorsSingleMaxRevenue(AbstractValidator):
    """
    A class defining the validator for the parameter user quality decay factors single max revenue from the config.ini
    """

    def validate(self, config, creator):
        try:
            quality_decay_factors = json.loads(config.get('SINGLE_MAX_REVENUE', 'user_quality_decay_factors'))
            for quality_decay_factor in quality_decay_factors:
                if not (isinstance(quality_decay_factor, float) and 0 < quality_decay_factor < 1):
                    return f"user_quality_decay_factors in BACKWARD_INDUCTION in config.ini must be floats between 0 and 1, but one element is {quality_decay_factor}."
            creator.user_quality_decay_factors = quality_decay_factors
        except ValueError:
            return 'user_quality_decay_factors in SINGLE_MAX_REVENUE in config.ini must be a list of floats.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
