import os
from pathlib import Path
from typing import List, Dict

import generators.utils
import generators.unit


class UnitEmbedded(generators.unit.Unit):
    def __init__(
        self,
        data: Dict,
    ):
        super().__init__(data)

        self.out_dir = self.get('extra_data').get('output_dir')
        self.template_dir = Path(os.path.dirname(__file__)).absolute().expanduser() / 'templates'
        self.src_dir = self.out_dir / 'src'
        self.header_dir = self.out_dir / 'src' / 'unit_system'

        super().add_template(generators.utils.Template(
            self.template_dir / 'unit.hpp.template',
            self.header_dir / f'{self.get("name")}.hpp',
        ))

        super().add_template(generators.utils.Template(
            self.template_dir / 'unit.cpp.template',
            self.src_dir / f'{self.get("name")}.cpp',
        ))
