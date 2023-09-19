from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserArrivalTimeDifferentialEvolution(AbstractValidator):
    """
    A class defining the validator for the parameter user arrival time differential evolution from the config.ini
    """

    def validate(self, config, creator):
        if not creator.evolution_with_all_user_types_from_game:
            try:
                creator.user_arrival_time = config.getint('DIFFERENTIAL_EVOLUTION', 'user_arrival_time')
                if not (1 <= creator.user_arrival_time <= creator.n_max):
                    return f"user_arrival_time in DIFFERENTIAL_EVOLUTION must be an integer between 1 and n_max of GAME_INFORMATION, but is {config.getint('DIFFERENTIAL_EVOLUTION', 'user_arrival_time')}."
            except ValueError:
                return 'user_arrival_time in DIFFERENTIAL_EVOLUTION must be an integer between 1 and n_max of GAME_INFORMATION'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
