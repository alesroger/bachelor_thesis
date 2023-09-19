from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPathToFolderSingleMaxRevenue(AbstractValidator):
    """
    A class defining the validator for the parameter local path to file folder single max revenue from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.path_to_folder = config.get('MAIN', 'local_path_to_file_folder_single_max_revenue')
        except ValueError:
            return f'local_path_to_file_folder_single_max_revenue in MAIN must be a valid path.'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
