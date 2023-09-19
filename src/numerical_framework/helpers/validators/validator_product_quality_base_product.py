from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorProductQualityBaseProduct(AbstractValidator):
    """
    A class defining the validator for the parameter product quality base product from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.product_quality_base_product = config.getfloat('GAME_INFORMATION',
                                                                   'product_quality_base_product')
            if creator.product_quality_base_product <= 0:
                return 'product_quality_base_product in GAME_INFORMATION must be float bigger than zero.'
        except ValueError:
            return 'product_quality_base_product in GAME_INFORMATION must be float.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return True
