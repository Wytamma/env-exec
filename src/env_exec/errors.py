"""
Custom errors for env_exec
"""

# EnvExecError
class EnvExecError(Exception):
    """Base class for exceptions in this module."""
    pass

# ExecError
class ExecError(EnvExecError):
    """Exception raised for errors in the execution of a command.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Initializes an ExecError object.

        Args:
            message (str): Explanation of the error.

        Returns:
            ExecError: An ExecError object.

        Examples:
            >>> raise ExecError('Error in command execution.')
            ExecError: Error in command execution.
        """
        self.message = message
        super().__init__(self.message)

# MissingDependencyError
class MissingDependencyError(EnvExecError):
    """Exception raised for errors in the execution of a command.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Initializes a MissingDependencyError object.

        Args:
            message (str): Explanation of the error.

        Returns:
            MissingDependencyError: A MissingDependencyError object.

        Examples:
            >>> raise MissingDependencyError('Missing dependency.')
            MissingDependencyError: Missing dependency.
        """
        self.message = message
        super().__init__(self.message)

# CreateEnvError
class CreateEnvError(EnvExecError):
    """Exception raised for errors in the execution of a command.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Initializes a CreateEnvError object.

        Args:
            message (str): Explanation of the error.

        Returns:
            CreateEnvError: A CreateEnvError object.

        Examples:
            >>> raise CreateEnvError('Error creating environment.')
            CreateEnvError: Error creating environment.
        """
        self.message = message
        super().__init__(self.message)

# InstallPackageError
class InstallPackageError(EnvExecError):
    """Exception raised for errors in the execution of a command.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Initializes an InstallPackageError object.

        Args:
            message (str): Explanation of the error.

        Returns:
            InstallPackageError: An InstallPackageError object.

        Examples:
            >>> raise InstallPackageError('Error installing package.')
            InstallPackageError: Error installing package.
        """
        self.message = message
        super().__init__(self.message)

# ManagerNotAvailable
class ManagerNotAvailable(EnvExecError):
    """Exception raised for errors in the execution of a command.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        """
        Initializes a ManagerNotAvailable object.

        Args:
            message (str): Explanation of the error.

        Returns:
            ManagerNotAvailable: A ManagerNotAvailable object.

        Examples:
            >>> raise ManagerNotAvailable('Manager not available.')
            ManagerNotAvailable: Manager not available.
        """
        self.message = message
        super().__init__(self.message)