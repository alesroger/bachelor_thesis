import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserArrivalTimesBackwardInduction(AbstractValidator):
    """
    A class defining the validator for the parameter user arrival times backward induction from the config.ini
    """

    def validate(self, config, creator):
        if not creator.induction_with_all_user_types_from_game:
            try:
                arrival_times = json.loads(config.get('BACKWARD_INDUCTION', 'user_arrival_times'))
                for arrival_time in arrival_times:
                    if not (isinstance(arrival_time, int) and 1 <= arrival_time <= creator.n_max):
                        return f"user_arrival_times in BACKWARD_INDUCTION must be a list of integers between (and including) 1 and n_max ({creator.n_max}) of GAME_INFORMATION."
                creator.user_arrival_times = arrival_times
            except ValueError:
                return 'user_arrival_times in BACKWARD_INDUCTION must be a list of integers between (and including) 1 and n_max of GAME_INFORMATION.'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
