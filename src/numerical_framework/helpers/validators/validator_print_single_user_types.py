from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPrintSingleUserTypes(AbstractValidator):
    """
    A class defining the validator for the parameter print single user types from the config.ini
    """

    def validate(self, config, creator):
        if creator.induction_with_all_user_types_from_game:
            try:
                creator.print_single_user_types = config.getboolean('BACKWARD_INDUCTION',
                                                                    'print_single_user_types')
            except ValueError:
                return f'print_single_user_types in BACKWARD_INDUCTION in config.ini must be True or False.'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
