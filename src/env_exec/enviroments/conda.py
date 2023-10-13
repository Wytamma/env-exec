import json
import subprocess
import uuid
from typing import List, Optional

from env_exec.enviroments.env import Env
from env_exec.errors import CreateEnvError, ExecError, MissingDependencyError


class CondaEnv(Env):
    """
    A Conda environment.
    """
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        dependencies: Optional[List[str]] = None,
        force: bool = False,
        check: bool = True,
        clean_up: bool = False,
        install_missing: bool = False,
        capture_output: bool = False,
        mamba: bool = False,
    ):
        """
        Initializes a Conda environment.

        Args:
            name (str, optional): The name of the environment. If not provided, a random name will be generated.
            dependencies (list[str], optional): A list of dependencies to install in the environment.
            force (bool, optional): If True, the environment will be recreated even if it already exists.
            check (bool, optional): If True, the environment will be checked for missing dependencies.
            clean_up (bool, optional): If True, the environment will be deleted when the context manager exits.
            install_missing (bool, optional): If True, missing dependencies will be installed.
            capture_output (bool, optional): If True, the output of the commands will be captured.
            mamba (bool, optional): If True, mamba will be used as the package manager.
        """
        if dependencies is None:
            dependencies = []
        if name is None:
            # create random id for env name
            name = "env_exec_" + str(uuid.uuid4()).replace("-", "")[:8]
            clean_up = True
        self.name = name
        self.dependencies = dependencies
        self.force = force
        self.check = check
        self.clean_up = clean_up
        self.capture_output = capture_output
        self.install_missing = install_missing
        self.manager = "mamba" if mamba else "conda"
        self.output = None

    def __enter__(self):
        """
        Enters the context manager.

        Returns:
            CondaEnv: The CondaEnv instance.

        Raises:
            MissingDependencyError: If check is True and there are missing dependencies and install_missing is False.
        """
        if self.force or not self.exists:
            self.output = self.create(capture_output=self.capture_output)
        if self.check:
            missing_dependencies = self.get_missing_dependencies()
            if not missing_dependencies:
                return self
            elif self.install_missing:
                self.install(missing_dependencies, capture_output=self.capture_output)
            else:
                raise MissingDependencyError(missing_dependencies)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context manager.

        Args:
            exc_type (type): The type of the exception raised.
            exc_value (Exception): The exception raised.
            traceback (traceback): The traceback of the exception raised.

        Side Effects:
            If clean_up is True, the environment will be deleted.
        """
        if self.clean_up:
            self.output = self.delete(capture_output=self.capture_output)

    @property
    def exists(self):
        """
        Checks if the environment exists.

        Returns:
            bool: True if the environment exists, False otherwise.
        """
        completed_process = subprocess.run(
            [self.manager, "env", "list", "--json"], capture_output=True, text=True, check=True
        )
        env_data = json.loads(completed_process.stdout)
        return self.name in [env.split("/")[-1] for env in env_data["envs"]]

    def create(self, *, capture_output: bool = False):
        """
        Creates the environment.

        Args:
            capture_output (bool, optional): If True, the output of the commands will be captured.

        Returns:
            CompletedProcess: The CompletedProcess object of the command.
        """
        try:
            return subprocess.run(
                [self.manager, "create", "--name", self.name, *self.dependencies, "--yes"],
                check=True,
                capture_output=capture_output,
                text=True,
            )
        except subprocess.CalledProcessError:
            msg = "\n\n---"
            msg += f"\n\nError Creating Environment: \nconda create --name {self.name} {' '.join(self.dependencies)}"
            msg += "\n(look at the top of the traceback above for more information)"
            raise CreateEnvError(msg) from None

    def install(self, package: List[str] | str, *, capture_output: bool = False):
        """
        Installs a package(s) in the environment.

        Args:
            package (str, list): The package to install.
            capture_output (bool, optional): If True, the output of the commands will be captured.

        Returns:
            CompletedProcess: The CompletedProcess object of the command.
        """
        if isinstance(package, str):
            package = [package]
        return subprocess.run(
            [self.manager, "install", "--name", self.name, *package, "--yes"],
            check=True,
            capture_output=capture_output,
            text=True,
        )

    def delete(self, *, capture_output: bool = False):
        """
        Deletes the environment.

        Args:
            capture_output (bool, optional): If True, the output of the commands will be captured.

        Returns:
            CompletedProcess: The CompletedProcess object of the command.
        """
        return subprocess.run(
            [self.manager, "env", "remove", "--name", self.name, "--yes"],
            check=True,
            capture_output=capture_output,
            text=True,
        )


    def get_missing_dependencies(self):
        """
        Gets the missing dependencies of a Conda environment.

        Args:
            self (CondaEnv): The Conda environment.

        Returns:
            List[str]: The missing dependencies.

        Raises:
            ExecError: If an error occurs while running the command.
            MissingDependencyError: If a dependency is missing.

        Examples:
            >>> env = CondaEnv("my_env", ["numpy=1.18.1", "pandas"])
            >>> env.get_missing_dependencies()
            ["numpy=1.18.1"]
        """
        completed_process = subprocess.run(
            [self.manager, "list", "--name", self.name, "--json"], capture_output=True, text=True, check=True
        )
        installed_packages = {package["name"]:package["version"] for package in json.loads(completed_process.stdout)}
        missing = []
        for dependency in self.dependencies:
            try:
                name, version = dependency.split("=")
            except ValueError:
                name = dependency
                version = None
            if name in installed_packages:
                if version and version != installed_packages[name]:
                    missing.append(dependency)
            else:
                missing.append(dependency)
        return missing

    def exec(self, command: str, *, capture_output: bool = False):
        """
        Executes a command in the environment.

        Args:
            command (str): The command to execute.
            capture_output (bool, optional): If True, the output of the commands will be captured.

        Returns:
            CompletedProcess: The CompletedProcess object of the command.

        Raises:
            ExecError: If the command fails.

        Examples:
            >>> with CondaEnv(name="my_env") as env:
            ...   env.exec("echo 'Hello World!'")
            CompletedProcess(args=['conda', 'run', '--name', 'my_env', 'bash', '-c', 'echo 'Hello World!'], returncode=0, stdout='Hello World!\\n', stderr='')
        """
        try:
            return subprocess.run(
                [self.manager, "run", "--name", self.name, "bash", "-c", command],
                check=True,
                capture_output=capture_output,
                text=True,
            )
        except subprocess.CalledProcessError:
            msg = "\n\n---"
            msg += f"\n\nError Running Command: \n{command}"
            msg += "\n(look at the top of the traceback above for more information)"
            raise ExecError(msg) from None
