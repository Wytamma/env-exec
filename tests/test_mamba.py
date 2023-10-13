import pytest

from env_exec.enviroments.mamba import MambaEnv


@pytest.fixture
def env():
    return MambaEnv("test_env", dependencies=["numpy", "pandas=2.0.0"])

def test_conda_env_init(env):
    assert env.manager == "mamba"
