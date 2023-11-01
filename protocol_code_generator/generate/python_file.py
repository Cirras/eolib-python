import os
from pathlib import Path

from protocol_code_generator.generate.code_block import CodeBlock


class PythonFile:
    def __init__(self, relative_path, code_block, *, module_docstring=None):
        self._relative_path = relative_path
        self._code_block = code_block
        self._module_docstring = module_docstring

    def write(self, root_path):
        output_path = os.path.join(root_path, self._relative_path)

        header = CodeBlock()
        header.add_line("# Generated from the eo-protocol XML specification.")
        header.add_line("#")
        header.add_line("# This file should not be modified.")
        header.add_line("# Changes will be lost when code is regenerated.")
        header.add_line()

        if self._module_docstring is not None:
            header.add_code_block(self._module_docstring)
            header.add_line()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        package_path = os.path.dirname(self._relative_path)
        package_path = os.path.join("eolib/protocol/_generated", package_path)
        package_path = Path(package_path).as_posix()
        package_path = package_path.replace('/', '.')

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(header.to_string(package_path) + self._code_block.to_string(package_path))

    @property
    def relative_path(self):
        return self._relative_path
