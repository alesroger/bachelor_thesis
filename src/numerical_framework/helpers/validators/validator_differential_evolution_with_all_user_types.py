from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorDifferentialEvolutionWithAllUserTypes(AbstractValidator):
    """
    A class defining the validator for the parameter differential evolution with all user types from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.evolution_with_all_user_types_from_game = config.getboolean(
                'DIFFERENTIAL_EVOLUTION',
                'evolution_with_all_user_types_from_game')
        except ValueError:
            raise Exception(
                f'evolution_with_all_user_types_from_game in BACKWARD_INDUCTION in config.ini must be True or False but is {config.get("DIFFERENTIAL_EVOLUTION", "evolution_with_all_user_types_from_game")}')
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
