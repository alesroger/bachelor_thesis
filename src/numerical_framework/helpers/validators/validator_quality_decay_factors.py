import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorQualityDecayFactors(AbstractValidator):
    """
    A class defining the validator for the parameter quality decay factors from the config.ini
    """

    def validate(self, config, creator):
        try:

            if len(json.loads(config.get('GAME_INFORMATION', 'quality_decay_factors'))) != 3:
                return "quality_decay_factors in GAME_INFORMATION in config.ini must have length 3, otherwise user probability calculations are wrong."

            first_quality_decay_factor = json.loads(config.get('GAME_INFORMATION', 'quality_decay_factors'))[0]
            second_quality_decay_factor = json.loads(config.get('GAME_INFORMATION', 'quality_decay_factors'))[1]
            third_quality_decay_factor = json.loads(config.get('GAME_INFORMATION', 'quality_decay_factors'))[2]
            if not (isinstance(first_quality_decay_factor, float) and 0 < first_quality_decay_factor < 1
                    and isinstance(second_quality_decay_factor, float) and 0 < second_quality_decay_factor < 1
                    and isinstance(third_quality_decay_factor, float) and 0 < third_quality_decay_factor < 1):
                return "quality_decay_factors in GAME_INFORMATION in config.ini must be floats between 0 and 1."
            creator.quality_decay_factors = [first_quality_decay_factor, second_quality_decay_factor,
                                             third_quality_decay_factor]
        except ValueError:
            return "quality_decay_factors in GAME_INFORMATION in config.ini must be floats between 0 and 1."
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
