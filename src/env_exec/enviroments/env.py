from abc import ABCMeta, abstractmethod


class Env(metaclass=ABCMeta):
    """
    Abstract base class for environment objects.
    """
    @abstractmethod
    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
            Env: The environment object.
        """
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context related to this object.

        Args:
            exc_type (Exception): The exception type.
            exc_value (Exception): The exception value.
            traceback (Traceback): The traceback object.
        """
        pass

    @abstractmethod
    def create(self):
        """
        Create the environment.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete the environment.
        """
        pass

    @abstractmethod
    def exec(self, command: str):
        """
        Execute a command in the environment.
        
        Args:
            command (str): The command to execute.
        """
        pass



