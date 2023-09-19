import json

from src.numerical_framework.helpers.validators.abstract_validator import AbstractValidator


class ValidatorFilesSingleMaxRevenueResultsAreWrittenTo(AbstractValidator):
    """
    A class defining the validator for the parameter files single max revenue results are written to from the config.ini
    """

    def validate(self, config, creator):
        try:
            files = json.loads(config.get('SINGLE_MAX_REVENUE', 'files_single_max_revenue_results_are_written_to'))
            for file in files:
                if not file.endswith('.csv'):
                    return f"files_single_max_revenue_results_are_written_to in SINGLE_MAX_REVENUE must be a list of strings ending with.csv, but one element is {file}."
            creator.files_results_are_written_to = files
        except ValueError:
            return 'files_single_max_revenue_results_are_written_to in SINGLE_MAX_REVENUE in config.ini must be a string ending with .csv.'

        return None

    def backward_induction_needs_validation(self):
        return False

    def differential_evolution_needs_validation(self):
        return False

    def single_maximize_revenue_needs_validation(self):
        return True
