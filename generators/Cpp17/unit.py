import os
import json
from pathlib import Path
from typing import List, Dict

import generators.utils
import generators.unit


# A class representing a unit fo the unit system.
#
# Attributes:
#     name: The name of the unit.
#     base_name: The base name of the unit. If the base name is not provided, this will be
#                   set to the value of the `name` attribute.
#     unit_id: The unit ID of the unit.
#     literals: A list of `UnitLiteral` objects that represent the literals for the unit.
#     export_macro: The export macro for the unit.
#     out_dir: The output directory for the unit.
#     include_subdir: The subdirectory for the header files (defaults to 'include').
#     src_subdir: The subdirectory for the source files (defaults to 'src').
class UnitCpp17(generators.unit.Unit):
    def __init__(
        self,
        data: Dict,
        out_dir: Path,
    ):
        super().__init__(data, out_dir)

        self.template_dir = Path(os.path.dirname(__file__)).absolute().expanduser() / 'templates'
        self.src_dir = self.out_dir / 'src'
        self.header_dir = self.out_dir / 'include' / 'unit_system'

        super().add_template(generators.utils.Template(
            self.template_dir / 'unit.hpp.template',
            self.header_dir / f'{self.get("name")}.hpp',
        ))

        super().add_template(generators.utils.Template(
            self.template_dir / 'unit.cpp.template',
            self.src_dir / f'{self.get("name")}.cpp',
        ))
