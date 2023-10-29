import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class ProtocolBuildHook(BuildHookInterface):
    def clean(self, versions: list) -> None:
        self._run_python_script("./protocol.py clean")

    def initialize(self, version: str, build_data: dict) -> None:
        self._run_python_script("./protocol.py generate")

    def _run_python_script(self, python_args: str) -> None:
        command = f"python {python_args}"
        code: int = os.system(command)
        if code != 0:
            raise RuntimeError(f'Command "{command}" failed with exit code {code}.')
