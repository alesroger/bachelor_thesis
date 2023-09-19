from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorProductQualityUpgrade(AbstractValidator):
    """
    A class defining the validator for the parameter product quality upgrade from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.product_quality_upgrade = config.getfloat('GAME_INFORMATION',
                                                              'product_quality_upgrade')
            if creator.product_quality_base_product < 0:
                return 'product_quality_upgrade in GAME_INFORMATION must be float bigger or equal to zero.'
        except ValueError:
            return 'product_quality_upgrade in GAME_INFORMATION must be float.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
