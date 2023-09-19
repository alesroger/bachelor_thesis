from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorNumberOfIterationsPerEvolutionType(AbstractValidator):
    """
    A class defining the validator for the parameter number of iterations per evolution type from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.number_of_iterations_per_evolution_type = config.getint(
                'DIFFERENTIAL_EVOLUTION',
                'number_of_iterations_per_evolution_type')
            if creator.number_of_iterations_per_evolution_type < 0:
                return f'number_of_iterations_per_evolution_type in DIFFERENTIAL_EVOLUTION in config.ini must be larger than 0, but is {creator.number_of_iterations_per_evolution_type}.'
        except ValueError:
            return 'first_upgrade_price_fixed in DIFFERENTIAL_EVOLUTION in config.ini must be non negative integer'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
