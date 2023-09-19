from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPathToFolderBackwardInduction(AbstractValidator):
    """
    A class defining the validator for the parameter local path to file folder backward induction from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.path_to_folder = config.get('MAIN', 'local_path_to_file_folder_backward_induction')
        except ValueError:
            return f'local_path_to_file_folder_backward_induction in MAIN must be a valid path but is {config.get("MAIN", "local_path_to_file_folder_backward_induction")}.'
        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
