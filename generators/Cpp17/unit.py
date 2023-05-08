import os
import json
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
        name: str,  # the name of the unit
        base_name: str,  # the base name of the unit
        unit_id: int,  # the unit ID of the unit
        literals: List[generators.unit.UnitLiteral],  # a list of UnitLiteral objects that represent the literals
        export_macro: str,  # the export macro for the unit
        base_dir: os.path,  # the base directory that is used out_dir is empty
        create_subdir=True,  # whether to create a subdirectory for the unit
        include_subdir='include',  # the subdirectory for the header files (defaults to 'include')
        src_subdir='src',  # the subdirectory for the source files (defaults to 'src')
        force_flat_headers=False,  # whether to force the header files to be in the same directory as the source files
        use_alternate_names=False,  # whether to use alternate names for literals on problematic platforms
    ):
        super().__init__(
            name=name,
            base_name=base_name,
            unit_id=unit_id,
            literals=literals,
            export_macro=export_macro,
            base_dir=base_dir,
            create_subdir=create_subdir,
            include_subdir=include_subdir,
            src_subdir=src_subdir,
            force_flat_headers=force_flat_headers,
            use_alternate_names=use_alternate_names
        )

    # returns the path to the header file for the unit system
    def get_header_path(self) -> str:
        # If an output directory was specified, use it, otherwise use the default output directory
        path = self.base_dir
        if self.create_subdir and not self.force_flat_headers:
            path = os.path.join(path, self.include_subdir)

        if not self.force_flat_headers:
            path = os.path.join(path, 'unit_system')

        # Append the name of the unit system and the .hpp file extension
        # to the output directory to get the path to the header file
        path = os.path.join(path, self.name + '.hpp')
        
        # create any missing directories in the path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    # returns the path to the source file for the unit system
    def get_source_path(self) -> str:
        # If an output directory was specified, use it, otherwise use the default output directory
        path = self.base_dir
        if self.create_subdir and not self.force_flat_headers:
            path = os.path.join(path, self.src_subdir)
        
        # Append the name of the unit system and the .cpp file extension
        # to the output directory to get the path to the source file
        path = os.path.join(path, self.name + '.cpp')

        # create any missing directories in the path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    # generates the source files for a given unit system
    def generate(self, print_files: bool=False):
        # the directory containing the template files
        template_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'templates')

        # the values to fill into the templates
        fill_dict = {
            'unit_name': self.name,  # the name of the unit system
            'unit_base_name': self.base_name,  # the base name of the unit system
            'unit_id': self.unit_id,  # the unit ID of the unit system
            'literals': self.literals,  # a list of UnitLiteral objects that represent
            # the literals for the unit system
            'create_literals': len(self.literals) > 0,  # create literals if there is at least one
            'export_macro': self.export_macro,  # the export macro for the unit system
            'force_flat_headers': self.force_flat_headers,  # whether to force the header files to be in the same
            'use_alternate_names': self.use_alternate_names,  # whether to use alternate names for literals
        }

        # generate the header
        generators.utils.fill_template(
            os.path.join(template_dir, 'unit.hpp.template'),  # the path to the header template file
            fill_dict,  # the values to fill into the template
            self.get_header_path()  # the path to the output header file
        )

        # generate the source
        generators.utils.fill_template(
            os.path.join(template_dir, 'unit.cpp.template'),  # the path to the source template file
            fill_dict,  # the values to fill into the template
            self.get_source_path()  # the path to the output source file
        )

        if print_files:
            print(self.get_header_path())
            print(self.get_source_path())
