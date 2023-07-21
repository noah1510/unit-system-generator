import os
from pathlib import Path
from typing import Dict

import generators.Cpp17.unit
import generators.embedded.unit
import generators.target


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
            return generators.target.Target(
                version,
                main_script_dir,
                output_dir,
                print_files,
                extra_data=extra_data_meson,
                target_name='meson',
                script_dir=script_dir / 'Cpp17',
                unit_type=generators.Cpp17.unit.UnitCpp17
            )

        case 'arduino':
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
                unit_type=generators.embedded.unit.UnitEmbedded
            )
        case _:
            raise ValueError(f'Unknown target: {target_name}')
