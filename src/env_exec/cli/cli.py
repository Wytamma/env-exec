import argparse
import sys
from typing import Any

from env_exec.environments import CondaEnv, MambaEnv


class CLI:
    def __init__(self):
        self.manager = None
        self.env_name = None
        self.dependencies = []
        self.command = None
        self.args = None
        self.capture_output = True
        self.verbose = False

    def parse_args(self):
        parser = argparse.ArgumentParser(description="cli for executing commands in a virtual environment")
        parser.add_argument(
            "manager",
            help="The package manager to use.",
            choices=["conda", "mamba", "docker"],
        )
        parser.add_argument(
            "-n",
            "--name",
            help="The name of the environment.",
        )
        parser.add_argument(
            "-d",
            "--dependency",
            help="The dependencies to install.",
            action="append",
            default=[],
        )
        parser.add_argument(
            "-c",
            "--channel",
            help="Channel to use.",
            action="append",
            default=[],
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="If True, the output of the commands will be captured.",
            action="store_true",
        )
        parser.add_argument(
            "-i",
            "--isolate",
            help="If True, the command will be isolated from the system environment.",
            action="store_true",
        )
        parser.add_argument(
            "-m",
            "--install-missing",
            help="If True, missing dependencies will be installed.",
            action="store_true",
        )
        parser.add_argument(
            "command",
            help="The command to execute.",
            nargs=argparse.REMAINDER,
        )
        args = parser.parse_args()
        self.manager = args.manager
        self.env_name = args.name
        self.dependencies = args.dependency
        self.channels = args.channel
        self.command = args.command
        self.verbose = args.verbose
        self.isolate = args.isolate
        self.install_missing = args.install_missing

    def __call__(self):
        self.parse_args()
        if self.verbose:
            self.capture_output = False
        if self.manager == "conda":
            env = CondaEnv(
                self.env_name,
                dependencies=self.dependencies,
                channels=self.channels,
                capture_output=self.capture_output,
                install_missing=self.install_missing,
            )
        elif self.manager == "mamba":
            env = MambaEnv(
                self.env_name,
                dependencies=self.dependencies,
                channels=self.channels,
                capture_output=self.capture_output,
                install_missing=self.install_missing,
            )
        elif self.manager == "python":
            msg = "PythonEnv is not implemented yet."
            raise NotImplementedError(msg)
        elif self.manager == "docker":
            msg = "DockerEnv is not implemented yet."
            raise NotImplementedError(msg)
        else:
            msg = f"Unknown package manager: {self.manager}"
            raise ValueError(msg)
        with env:
            env.exec(" ".join(self.command), isolate=self.isolate)
