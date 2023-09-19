from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorPathToFolderDifferentialEvolution(AbstractValidator):
    """
    A class defining the validator for the parameter local path to file folder differential evolution from the config.ini
    """

    def validate(self, config, creator):
        try:
            creator.path_to_folder = config.get('MAIN', 'local_path_to_file_folder_differential_evolution')
        except ValueError:
            return f'local_path_to_file_folder_differential_evolution in MAIN must be a valid path.'
        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
