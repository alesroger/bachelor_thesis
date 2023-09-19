from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPrintUserTypesCombined(AbstractValidator):
    """
    A class defining the validator for the parameter print user types combined from the config.ini
    """

    def validate(self, config, creator):
        if creator.induction_with_all_user_types_from_game:
            try:
                creator.print_user_types_combined = config.getboolean('BACKWARD_INDUCTION',
                                                                      'print_user_types_combined')
            except ValueError:
                return f'print_user_types_combined in BACKWARD_INDUCTION in config.ini must be True or False.'

            if not (
                    creator.print_single_user_types or creator.print_user_types_combined):
                return 'if induction_with_all_user_types_from_game is True, either print_user_types_combined or print_single_user_types in BACKWARD_INDUCTION must be True, otherwise no results will be printed.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
