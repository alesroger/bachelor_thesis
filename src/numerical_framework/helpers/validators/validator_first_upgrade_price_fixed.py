from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorFirstUpgradePriceFixed(AbstractValidator):
    """
    A class defining the validator for the parameter first upgrade price fixed from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.first_upgrade_price_fixed = config.getfloat('DIFFERENTIAL_EVOLUTION',
                                                                'first_upgrade_price_fixed')
            if creator.first_upgrade_price_fixed < 0:
                return 'first_upgrade_price_fixed in DIFFERENTIAL_EVOLUTION in config.ini must be 0 (no price fixed) or greater'
        except ValueError:
            return 'first_upgrade_price_fixed in DIFFERENTIAL_EVOLUTION in config.ini must be float'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
