import os
from pathlib import Path
from typing import List

import generators.target
import generators.utils


def get_target_files() -> List[generators.utils.File]:
    targets_dir = Path(os.path.dirname(__file__)).absolute().expanduser() / 'targets'
    targets = [generators.utils.File(targets_dir/f) for f in targets_dir.iterdir() if f.is_file()]
    return targets


def init_subparser(subparser):
    targets_json = [t.read_json() for t in get_target_files()]
    for target in targets_json:
        subparser.add_parser(target['name'], help=target['help'])


def get_target(
    version,
    main_script_dir,
    output_dir: Path,
    target_name: str,
    print_files=False,
) -> generators.target.Target:
    targets = get_target_files()

    for target in targets:
        if target.read_json()['name'] == target_name:
            return generators.target.Target(
                version,
                main_script_dir,
                output_dir,
                print_files,
                target_file=target,
            )

    raise ValueError(f'Unknown target: {target_name}')

