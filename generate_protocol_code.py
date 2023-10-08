import shutil
from pathlib import Path
from contextlib import suppress
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


def generated_dir() -> Path:
    return Path(__file__).parent.joinpath('src/eolib/protocol/generated').resolve()


def eo_protocol_dir() -> Path:
    return Path(__file__).parent.joinpath('eo-protocol/xml').resolve()


class GenerateProtocolCodeBuildHook(BuildHookInterface):
    def clean(self, versions: list) -> None:
        with suppress(FileNotFoundError):
            shutil.rmtree(generated_dir())

    def initialize(self, version: str, build_data: dict) -> None:
        self.clean([version])
