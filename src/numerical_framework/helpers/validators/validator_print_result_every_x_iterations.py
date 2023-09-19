from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPrintResultEveryXIterations(AbstractValidator):
    """
    A class defining the validator for the parameter print result every x iterations from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.print_result_every_x_iterations = config.getint('DIFFERENTIAL_EVOLUTION',
                                                                    'print_result_every_x_iterations')
            if creator.print_result_every_x_iterations < 0:
                return f'print_result_every_x_iterations in DIFFERENTIAL_EVOLUTION in config.ini must be 0 (no price fixed) or greater but is {creator.print_result_every_x_iterations}.'
        except ValueError:
            return 'first_upgrade_price_fixed in DIFFERENTIAL_EVOLUTION in config.ini must be non negative integer'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
