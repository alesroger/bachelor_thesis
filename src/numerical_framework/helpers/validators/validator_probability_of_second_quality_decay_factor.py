import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorProbabilityOfSecondQualityDecayFactor(AbstractValidator):
    """
    A class defining the validator for the parameter probability of second quality decay factor from the config.ini
    """

    def validate(self, config, creator):
        try:
            probability_of_second_quality_decay_element = json.loads(
                config.get('GAME_INFORMATION', 'probability_of_second_quality_decay_element'))
            if not len(probability_of_second_quality_decay_element) > 0:
                return "probability_of_second_quality_decay_element in GAME_INFORMATION must contain at least one element"
            for single_prob_quality_decay in probability_of_second_quality_decay_element:
                if not (isinstance(single_prob_quality_decay, (float, int)) and 1 >= single_prob_quality_decay >= 0):
                    return f"elements of probability_of_second_quality_decay_element in GAME_INFORMATION must be a float or int between 0 and 1, but contains element {single_prob_quality_decay}."
            creator.probability_of_second_quality_decay_element = probability_of_second_quality_decay_element
        except ValueError:
            return 'probability_of_second_quality_decay_element in GAME_INFORMATION must be a list of floats or integers between 0 and 1.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
