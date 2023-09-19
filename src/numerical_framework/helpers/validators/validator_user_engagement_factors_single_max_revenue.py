import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorUserEngagementFactorsSingleMaxRevenue(AbstractValidator):
    """
    A class defining the validator for the parameter user engagement factors single max revenue from the config.ini
    """

    def validate(self, config, creator):
        try:
            engagement_factors = json.loads(config.get('SINGLE_MAX_REVENUE', 'user_engagement_factors'))
            for engagement_factor in engagement_factors:
                if not 0 <= engagement_factor <= 1:
                    return f"user_engagement_factors in SINGLE_MAX_REVENUE must be floats (or integers) between 0 and 1, but contains element {engagement_factor}."
            creator.user_engagement_factors = engagement_factors
        except ValueError:
            return 'user_engagement_factors in SINGLE_MAX_REVENUE in config.ini must be a list of floats.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
