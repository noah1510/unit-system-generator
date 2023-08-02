import os
import subprocess
from pathlib import Path
from typing import List, Dict
import tarfile

import generator_code.utils
import generator_code.unit


# A class that represents a target for the code generator
# This class is used to generalize the code generator so that more targets can be added easily
# while still keeping the code clean and readable
class Target:
    def __init__(
            self,
            version: str,
            main_script_dir: Path,
            output_dir: str,
            print_files: bool = False,
            clean_output_dir: bool = False,
            target_file: generator_code.utils.File = None,
            unit_type: type(generator_code.unit.Unit) = generator_code.unit.Unit
    ):
        # read the target config file and the passed arguments
        target_json = target_file.read_json()
        self.version = version
        self.target_name = target_json['name']
        self.target_group = target_json['group']
        self.print_files = print_files
        self.clean_output_dir = clean_output_dir
        if 'extra_data' in target_json:
            self.extra_data = target_json['extra_data']
        else:
            self.extra_data = {}
        self.units: List[generator_code.unit.Unit] = []
        self.unit_type = unit_type
        self.hasCombinations = True
        self.fill_dict = {}
        self.clang_format_options = target_json.get('clang-format', {})

        # setup all needed paths
        self.main_script_dir = main_script_dir
        if output_dir is None or output_dir == '':
            self.output_dir = main_script_dir / ('output_' + self.target_name)
        else:
            self.output_dir = main_script_dir / output_dir
        self.extra_data['output_dir'] = self.output_dir
        self.script_dir = self.main_script_dir / "target_data"
        self.common_dir = self.script_dir / 'common'
        self.group_dir = self.script_dir / self.target_group
        self.target_dir = self.group_dir / self.target_name
        self.generic_dir = self.group_dir / 'generic'
        self.template_dir = self.group_dir / 'per_unit'
        self.type_location = main_script_dir / 'type data'

        # get the per-unit templates
        self.per_unit_templates: List[Dict] = []
        if 'per_unit_templates' in target_json:
            for template in target_json['per_unit_templates']:
                unit_template: Dict = {
                    'infile': generator_code.utils.File(self.template_dir / template['filename']),
                    'out_dir': self.output_dir / template['output_location'],
                    'file_format': template['output_pattern'],
                }
                self.per_unit_templates += [unit_template]

    def generate_fill_dict(self):
        self.fill_dict = generator_code.unit.fill_from_files(
            self.type_location,
            self.units,
            extra_data=self.extra_data,
        )

        self.fill_dict['target'] = self.target_name
        self.fill_dict['version'] = self.version

    def generate_sources(self):
        self.units = generator_code.unit.units_from_file(
            self.main_script_dir,
            self.print_files,
            per_unit_templates=self.per_unit_templates,
            extra_data=self.extra_data,
            unit_type=self.unit_type,
        )

        for unit in self.units:
            unit.generate(self.print_files)

        self.generate_fill_dict()

    def generate_system(self):
        generator_code.utils.Template(
            self.common_dir,
            self.output_dir,
        ).fill_with(self.fill_dict)

        generator_code.utils.Template(
            self.generic_dir,
            self.output_dir,
        ).fill_with(self.fill_dict)

        generator_code.utils.Template(
            self.target_dir,
            self.output_dir,
        ).fill_with(self.fill_dict)

    def generate(self):
        self.clean()
        self.generate_sources()
        self.generate_system()

    def clean(self):
        if self.clean_output_dir:
            generator_code.utils.File(self.output_dir).clean()

    def archive(self):
        archive_name = self.main_script_dir / ('unit_system_' + self.target_name + '.tar.gz')
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(self.output_dir, arcname=self.target_name)

    def format(self):
        if 'file_patters' not in self.clang_format_options:
            return

        for pattern in self.clang_format_options['file_patters']:
            for file in self.output_dir.glob(pattern):
                subprocess.run(['clang-format', '-i', file], cwd=self.output_dir)

    @staticmethod
    def get_target_files() -> List[generator_code.utils.File]:
        targets_dir = Path(os.path.dirname(__file__)).absolute().expanduser() / 'targets'
        targets = [generator_code.utils.File(targets_dir / f) for f in targets_dir.iterdir() if f.is_file()]
        return targets

    @staticmethod
    def init_subparser(subparser):
        targets_json = [t.read_json() for t in Target.get_target_files()]
        subparser.add_parser('all', help='Generate all targets')
        for target in targets_json:
            subparser.add_parser(target['name'], help=target['help'])

    @staticmethod
    def get_targets(
            version,
            main_script_dir,
            output_dir: str,
            target_name: str,
            print_files=False,
            clean_output_dir=False,
    ) -> List['Target']:
        targets_json = Target.get_target_files()
        target_list = []

        for target in targets_json:
            if target.read_json()['name'] == target_name or target_name == 'all':
                target_list.append(Target(
                    version=version,
                    main_script_dir=main_script_dir,
                    output_dir=output_dir,
                    print_files=print_files,
                    clean_output_dir=clean_output_dir,
                    target_file=target,
                ))

        if len(target_list) == 0:
            raise ValueError(f'Unknown target: {target_name}')

        return target_list
