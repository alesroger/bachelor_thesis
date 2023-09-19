from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorInductionWithAllUserTypes(AbstractValidator):
    """
    A class defining the validator for the parameter induction with all user types from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.induction_with_all_user_types_from_game = config.getboolean('BACKWARD_INDUCTION',
                                                                                'induction_with_all_user_types_from_game')
        except ValueError:
            return f'induction_with_all_user_types_from_game in BACKWARD_INDUCTION in config.ini must be True or False.'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
