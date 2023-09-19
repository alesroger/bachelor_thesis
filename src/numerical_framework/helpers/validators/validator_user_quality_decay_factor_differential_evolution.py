from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserQualityDecayFactorDifferentialEvolution(AbstractValidator):
    """
    A class defining the validator for the parameter user quality decay factor differential evolution from the config.ini
    """

    def validate(self, config, creator):
        if not creator.evolution_with_all_user_types_from_game:
            try:
                creator.user_quality_decay_factor = config.getfloat('DIFFERENTIAL_EVOLUTION',
                                                                    'user_quality_decay_factor')
                if not (0 < creator.user_quality_decay_factor < 1):
                    return f"user_quality_decay_factor in DIFFERENTIAL_EVOLUTION must be float between 0 and 1 but is {creator.user_quality_decay_factor}."
            except ValueError:
                return f"user_quality_decay_factor in DIFFERENTIAL_EVOLUTION must be float between 0 and 1."
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
