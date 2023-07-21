import os
from pathlib import Path
from typing import List
import tarfile

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
            extra_data: dict = None,
            target_name: str = '',
            per_unit_templates: List[generators.utils.File] = None,
            script_dir: Path = Path(os.path.dirname(__file__)).absolute().expanduser(),
            unit_type: type(generators.unit.Unit) = generators.unit.Unit
    ):
        self.version = version
        self.target_name = target_name

        self.main_script_dir = main_script_dir
        self.output_dir = output_dir
        self.print_files = print_files

        self.target_dir = script_dir / self.target_name
        self.template_dir = script_dir / 'templates'
        self.type_location = main_script_dir / 'type data'
        self.per_unit_templates = per_unit_templates

        if extra_data is None:
            extra_data = {}

        extra_data['output_dir'] = output_dir
        self.extra_data = extra_data
        self.units: List[generators.unit.Unit] = []
        self.unit_type = unit_type
        self.hasCombinations = True
        self.fill_dict = {}

    def generate_fill_dict(self):
        self.fill_dict = generators.unit.fill_from_files(
            self.type_location,
            self.units,
            extra_data=self.extra_data,
        )

        self.fill_dict['target'] = self.target_name
        self.fill_dict['version'] = self.version

    def generate_sources(self):
        self.units = generators.unit.units_from_file(
            self.main_script_dir,
            self.print_files,
            per_unit_templates=self.per_unit_templates,
            extra_data=self.extra_data,
            unit_type=self.unit_type,
        )

        for unit in self.units:
            unit.generate()

        self.generate_fill_dict()

    def generate_system(self):
        generators.utils.Template(
            self.target_dir,
            self.output_dir,
        ).fill_with(self.fill_dict)

    def generate(self):
        self.generate_sources()
        self.generate_system()

    def archive(self):
        archive_name = self.main_script_dir / ('unit_system_' + self.target_name + '.tar.gz')
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(self.output_dir, arcname=self.target_name)
