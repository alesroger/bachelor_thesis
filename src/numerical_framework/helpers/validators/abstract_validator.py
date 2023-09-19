from abc import abstractmethod, ABC


class AbstractValidator(ABC):
    """
    An abstract class defining the structure of all validators for parameters read from the config.ini
    """

    @abstractmethod
    def validate(self, config, creator):
        """
        Validates the corresponding input value and if necessary returns an error message
        """
        pass

    @abstractmethod
    def backward_induction_needs_validation(self):
        """
        Method returning True if parameter is needed in backward induction, False otherwise
        """
        pass

    @abstractmethod
    def differential_evolution_needs_validation(self):
        """
        Method returning True if parameter is needed in differential evolution, False otherwise
        """
        pass

    @abstractmethod
    def single_maximize_revenue_needs_validation(self):
        """
       Method returning True if parameter is needed in single maximize revenue, False otherwise
       """
        pass
