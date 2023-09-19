from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserValuationDifferentialEvolution(AbstractValidator):
    """
    A class defining the validator for the parameter user valuation differential evolution from the config.ini
    """

    def validate(self, config, creator):
        if not creator.evolution_with_all_user_types_from_game:
            try:
                creator.user_valuation = config.getfloat('DIFFERENTIAL_EVOLUTION',
                                                         'user_valuation')
                if not (0 <= creator.user_valuation):
                    return f"user_valuation in DIFFERENTIAL_EVOLUTION must be a non-negative float but is {config.getfloat('DIFFERENTIAL_EVOLUTION', 'user_valuation')}"
            except ValueError:
                return 'user_valuation in DIFFERENTIAL_EVOLUTION must be a non-negative float.'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
