import shutil
import os
from argparse import ArgumentParser
from pathlib import Path
from contextlib import suppress
from protocol_code_generator.generate.code_generator import ProtocolCodeGenerator


def clean() -> None:
    generated = _generated_dir()
    if os.path.exists(generated):
        print(f"Removing: {generated}")
        shutil.rmtree(generated)


def generate() -> None:
    code_generator = ProtocolCodeGenerator(_eo_protocol_dir())
    code_generator.generate(_generated_dir())


def _generated_dir() -> Path:
    return Path(__file__).parent.joinpath('src/eolib/protocol/_generated').resolve()


def _eo_protocol_dir() -> Path:
    return Path(__file__).parent.joinpath('eo-protocol/xml').resolve()


if __name__ == "__main__":
    parser = ArgumentParser(description='Helper script for managing generated EO protocol code.')
    parser.add_argument("command", choices=["generate", "clean"])
    args = parser.parse_args()

    clean()

    if args.command != "clean":
        generate()
