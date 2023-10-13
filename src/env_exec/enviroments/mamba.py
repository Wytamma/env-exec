from env_exec.enviroments.conda import CondaEnv


class MambaEnv(CondaEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, manager="mamba")
