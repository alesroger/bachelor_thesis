import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorFilesBackwardInductionResultsAreWrittenTo(AbstractValidator):
    """
    A class defining the validator for the parameter files backward induction results are written to from the config.ini
    """

    def validate(self, config, creator):
        try:
            files = json.loads(config.get('BACKWARD_INDUCTION', 'files_backward_induction_results_are_written_to'))
            for file in files:
                if not file.endswith('.csv'):
                    return f"files_backward_induction_results_are_written_to in BACKWARD_INDUCTION in config.ini must be a list of strings ending with .csv, but one element is {file}."
                files_for_backward_induction = creator.files_results_are_written_to
                if files_for_backward_induction is None:
                    files_for_backward_induction = []
                files_for_backward_induction.append(file)
                creator.files_results_are_written_to = files_for_backward_induction
        except ValueError:
            return 'files_backward_induction_results_are_written_to in BACKWARD_INDUCTION must be a list of strings ending with .csv'

        return None

    def backward_induction_needs_validation(self):
        return True

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return False
