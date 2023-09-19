from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorEngagementFactorLongTermUser(AbstractValidator):
    """
    A class defining the validator for the parameter engagement factor long term user from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.engagement_factor_long_term_user = config.getfloat('GAME_INFORMATION',
                                                                       'engagement_factor_long_term_user')
            if not (0 <= creator.engagement_factor_long_term_user <= 1):
                return f'engagement_factor_long_term_user in GAME_INFORMATION in config.ini must be float (or integer) between 0 and 1, but is {creator.engagement_factor_long_term_user}.'
        except ValueError:
            return 'engagement_factor_long_term_user in GAME_INFORMATION in config.ini must be float (or integer) between 0 and 1.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
