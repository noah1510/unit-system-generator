import os
from pathlib import Path
from typing import List

import generators.utils
import generators.unit


# A class that represents a target for the code generator
# This class is used to generalize the code generator so that more targets can be added easily
# while still keeping the code clean and readable
class Target:
    def __init__(
            self,
            version: str,
            main_script_dir: Path,
            output_dir: Path,
            print_files: bool = False,
            enable_export_macro: bool = True,
            target_name: str = '',
            script_dir: Path = Path(os.path.dirname(__file__)).absolute().expanduser(),
            unit_type: type(generators.unit.Unit) = generators.unit.Unit
    ):
        self.version = version
        self.target_name = target_name
        if enable_export_macro:
            self.export_macro = 'UNIT_SYSTEM_EXPORT_MACRO'
        else:
            self.export_macro = ''

        self.main_script_dir = main_script_dir
        self.output_dir = output_dir
        self.print_files = print_files

        self.target_dir = script_dir / self.target_name
        self.template_dir = script_dir / 'templates'
        self.type_location = main_script_dir / 'type data'

        self.units: List[generators.unit.Unit] = []
        self.unit_type = unit_type
        self.hasCombinations = True
        self.fill_dict = {}

    def generate_fill_dict(self):
        self.fill_dict = generators.unit.fill_from_files(
            self.type_location,
            self.export_macro,
            self.units
        )

        self.fill_dict['target'] = self.target_name
        self.fill_dict['version'] = self.version

    def generate_sources(self):
        self.units = generators.unit.units_from_file(
            self.main_script_dir,
            self.output_dir,
            self.export_macro,
            self.print_files,
            unit_type=self.unit_type
        )

        self.generate_fill_dict()

    def generate_system(self):
        generators.utils.Template(
            self.target_dir,
            self.output_dir,
        ).fill_with(self.fill_dict)

    def generate(self):
        self.generate_sources()
        self.generate_system()
