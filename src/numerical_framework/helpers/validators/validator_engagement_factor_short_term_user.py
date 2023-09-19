import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorEngagementFactorShortTermUser(AbstractValidator):
    """
    A class defining the validator for the parameter engagement factor short term user from the config.ini
    """

    def validate(self, config, creator):
        try:
            engagement_factors_short_term_user = json.loads(
                config.get('GAME_INFORMATION', 'engagement_factor_short_term_user'))
            if not len(engagement_factors_short_term_user) > 0:
                return "engagement_factors_short_term_user in GAME_INFORMATION must contain at least one element"
            for engagement_factor in engagement_factors_short_term_user:
                if not (isinstance(engagement_factor, (float, int)) and 0 <= engagement_factor <= 1):
                    return f"elements of engagement_factors_short_term_user in GAME_INFORMATION must be floats (or ints) between 0 and 1, but contains element {engagement_factor}."
            creator.engagement_factor_short_term_user = engagement_factors_short_term_user
        except ValueError:
            return f'engagement_factors_short_term_user in GAME_INFORMATION must be a list of floats (or integers) between 0 and 1.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
