import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserEngagementFactorsBackwardInduction(AbstractValidator):
    """
    A class defining the validator for the parameter user engagement factors backward induction from the config.ini
    """

    def validate(self, config, creator):
        if not creator.induction_with_all_user_types_from_game:
            try:
                engagement_factors = json.loads(config.get('BACKWARD_INDUCTION', 'user_engagement_factors'))
                for engagement_factor in engagement_factors:
                    if not (isinstance(engagement_factor, (float, int)) and 0 <= engagement_factor <= 1):
                        return f"user_engagement_factors in BACKWARD_INDUCTION must be floats between 0 and 1, but one element is {engagement_factor}."
                creator.user_engagement_factors = engagement_factors
            except ValueError:
                return 'user_engagement_factors in BACKWARD_INDUCTION must be a list of floats'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
