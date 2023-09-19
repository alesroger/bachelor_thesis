import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserArrivalTimesSingleMaxRevenue(AbstractValidator):
    """
    A class defining the validator for the parameter user arrival times single max revenue from the config.ini
    """

    def validate(self, config, creator):
        try:
            arrival_times = json.loads(config.get('SINGLE_MAX_REVENUE', 'user_arrival_times'))
            for arrival_time in arrival_times:
                if not (isinstance(arrival_time, int) and 1 <= arrival_time <= creator.n_max):
                    return f"user_arrival_times in SINGLE_MAX_REVENUE must be a list of integers between (and including) 1 and n_max ({creator.n_max}) of GAME_INFORMATION, but one element is {arrival_time}."
            creator.user_arrival_times = arrival_times
        except ValueError:
            return 'user_arrival_times in SINGLE_MAX_REVENUE must be a list of integers between (and including) 1 and n_max of SINGLE_MAX_REVENUE.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
