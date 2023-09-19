import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorFilesDifferentialEvolutionResultsAreWrittenTo(AbstractValidator):
    """
    A class defining the validator for the parameter files differential evolution results are written to from the config.ini
    """

    def validate(self, config, creator):
        try:
            files = json.loads(config.get('DIFFERENTIAL_EVOLUTION', 'files_diff_evolution_results_are_written_to'))
            for file in files:
                if not file.endswith('.csv'):
                    return f"main_result_file_differential_evolution in DIFFERENTIAL_EVOLUTION in config.ini must end with .csv but contains element {file}"
            creator.files_results_are_written_to = files
        except ValueError:
            return 'files_diff_evolution_results_are_written_to in DIFFERENTIAL_EVOLUTION in config.ini must be a string ending with .csv'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return True

    def single_maximize_revenue_needs_validation(self):
        return False
