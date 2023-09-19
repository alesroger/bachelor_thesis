import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorArrivalTime(AbstractValidator):
    """
    A class defining the validator for the parameter arrival time from the config.ini
    """

    def validate(self, config, creator):
        try:
            arrivals_in_first_timesteps = json.loads(config.get('GAME_INFORMATION', 'arrivals_in_first_timestep'))
            if not len(arrivals_in_first_timesteps) > 0:
                return "arrivals_in_first_timestep in GAME_INFORMATION must contain at least one element"
            for arrival in arrivals_in_first_timesteps:
                if not (isinstance(arrival, (float, int)) and arrival >= 0):
                    return f"elements of arrivals_in_first_timestep in GAME_INFORMATION must be floats or integers bigger equal to 0, but contains element {arrival}."
            creator.arrivals_in_first_timestep = arrivals_in_first_timesteps
        except ValueError:
            return 'arrivals_in_first_timestep in GAME_INFORMATION must be a list of floats or integers bigger equal to 0.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
