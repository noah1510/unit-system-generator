import os
from pathlib import Path

import generators.target
import generators.utils


def init_subparser(subparser):
    meson_parser = subparser.add_parser("meson", help="generate the code for the meson build system")
    arduino_parser = subparser.add_parser("arduino", help="generate the code for the arduino library manager")


def get_target(
    version,
    main_script_dir,
    output_dir: Path,
    target_name: str,
    print_files=False,
) -> generators.target.Target:
    script_dir = Path(os.path.dirname(__file__)).absolute().expanduser()

    match target_name:
        case 'meson':
            extra_data_meson = {}
            template_dir_cpp17 = script_dir / 'Cpp17' / 'templates'
            unit_templates_meson = [
                {
                    'infile': generators.utils.File(template_dir_cpp17 / 'unit.cpp.template'),
                    'out_dir': output_dir / 'src',
                    'file_format': '{unit[name]}.cpp',
                }, {
                    'infile': generators.utils.File(template_dir_cpp17 / 'unit.hpp.template'),
                    'out_dir': output_dir / 'include' / 'unit_system',
                    'file_format': '{unit[name]}.hpp',
                }
            ]
            return generators.target.Target(
                version,
                main_script_dir,
                output_dir,
                print_files,
                extra_data=extra_data_meson,
                target_name='meson',
                script_dir=script_dir / 'Cpp17',
                per_unit_templates=unit_templates_meson,
            )

        case 'arduino':
            template_dir_embedded = script_dir / 'embedded' / 'templates'
            unit_templates_arduino = [
                {
                    'infile': generators.utils.File(template_dir_embedded / 'unit.cpp.template'),
                    'out_dir': output_dir / 'src',
                    'file_format': '{unit[name]}.cpp',
                }, {
                    'infile': generators.utils.File(template_dir_embedded / 'unit.hpp.template'),
                    'out_dir': output_dir / 'src' / 'unit_system',
                    'file_format': '{unit[name]}.hpp',
                }
            ]
            extra_data_arduino = {
                'use_alternate_names': True,
            }
            return generators.target.Target(
                version,
                main_script_dir,
                output_dir,
                print_files,
                extra_data=extra_data_arduino,
                target_name='arduino',
                script_dir=script_dir / 'embedded',
                per_unit_templates=unit_templates_arduino,
            )
        case _:
            raise ValueError(f'Unknown target: {target_name}')
