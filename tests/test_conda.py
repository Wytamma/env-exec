import json
import subprocess
from unittest.mock import patch

import pytest

from env_exec.enviroments.conda import CondaEnv
from env_exec.errors import ExecError


@pytest.fixture
def conda_env():
    return CondaEnv("test_env", dependencies=["numpy", "pandas=2.0.0"])


@pytest.fixture
def mock_subprocess_run():
    with patch("subprocess.run") as mock_run:
        yield mock_run


def test_conda_env_init(conda_env):
    assert conda_env.name == "test_env"
    assert conda_env.dependencies == ["numpy", "pandas=2.0.0"]
    assert not conda_env.force
    assert conda_env.check
    assert not conda_env.clean_up


def test_conda_env_exists(conda_env, mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = json.dumps(
        {"envs": ["/path/to/test_env"]}
    )
    assert conda_env.exists


def test_conda_env_create(conda_env, mock_subprocess_run):
    conda_env.create()
    mock_subprocess_run.assert_called_once()


def test_conda_env_delete(conda_env, mock_subprocess_run):
    conda_env.delete()
    mock_subprocess_run.assert_called_once()


def test_conda_env_check_missing(conda_env, mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = json.dumps(
        [{"name": "numpy", "version": "1"}, {"name": "pandas", "version": "1"}]
    )
    conda_env.get_missing_dependencies()


def test_conda_env_check_dependencies_missing(conda_env: CondaEnv, mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = json.dumps([{"name": "numpy", "version": "1"}, {"name": "pandas", "version": "1"}])
    assert conda_env.get_missing_dependencies() == ["pandas=2.0.0"]


def test_conda_env_exec(conda_env, mock_subprocess_run):
    conda_env.exec("ls")
    mock_subprocess_run.assert_called_once()


def test_conda_env_exec_error(conda_env, mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "ls")
    with pytest.raises(ExecError):
        conda_env.exec("ls")


@pytest.mark.parametrize(
    "force,exists,expected_calls",
    [(True, False, 3), (False, True, 2), (False, False, 2)],
)
def test_conda_env_enter(force, exists, expected_calls, conda_env, mock_subprocess_run):
    conda_env.force = force
    conda_env.install_missing = True
    mock_subprocess_run.return_value.stdout = json.dumps([{"name": "numpy", "version": "1"}, {"name": "pandas", "version": "1"}])
    # mock exists property
    with patch("env_exec.CondaEnv.exists") as mock_exists:
        mock_exists.return_value.stdout = json.dumps({"envs": ["/path/to/test_env"]})
        with conda_env:
            assert mock_subprocess_run.call_count == expected_calls


def test_conda_env_exit(conda_env, mock_subprocess_run):
    conda_env.clean_up = True
    conda_env.install_missing = True
    mock_subprocess_run.return_value.stdout = json.dumps([{"name": "numpy", "version": "1"}, {"name": "pandas", "version": "1"}])
    with patch("env_exec.CondaEnv.exists") as mock_exists:
        mock_exists.return_value.stdout = json.dumps({"envs": ["/path/to/test_env"]})
        with conda_env:
            pass
    assert mock_subprocess_run.call_count == 3
