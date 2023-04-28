import os
import argparse
import json
from typing import List, Dict

import generators.utils


# A class representing a unit literal.
#
# This class extends the built-in `Dict` class, so it can be treated like a dictionary in addition to
# having its own attributes.
#
# Attributes:
#     name: The name of the unit literal.
#     multiplier: The multiplier to be applied when converting between this unit literal and the base unit.
#     offset: The offset to be applied when converting between this unit literal and the base unit.
class UnitLiteral(Dict):
    def __init__(self, _data: dict):
        super().__init__(_data)
        # Set the name attribute to the value of the 'name' key in the input dictionary
        self.name = _data['name']
        # If the input dictionary contains a 'multiplier' key, set the multiplier attribute
        # to the corresponding value, otherwise set it to 1.0
        if 'multiplier' in _data:
            self.multiplier = _data['multiplier']
        else:
            self.multiplier = 1.0

        # If the input dictionary contains an 'offset' key, set the offset attribute
        # to the corresponding value, otherwise set it to 0.0
        if 'offset' in _data:
            self.offset = _data['offset']
        else:
            self.offset = 0.0


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
class Unit:
    def __init__(
        self,
        name: str,  # the name of the unit
        base_name: str,  # the base name of the unit
        unit_id: int,  # the unit ID of the unit
        literals: List[UnitLiteral],  # a list of UnitLiteral objects that represent the literals for the unit
        export_macro: str,  # the export macro for the unit
        out_dir: os.path,  # the output directory for the unit
        base_dir: os.path,  # the base directory that is used out_dir is empty
        include_subdir='include',  # the subdirectory for the header files (defaults to 'include')
        src_subdir='src',  # the subdirectory for the source files (defaults to 'src')
    ):
        self.name = name
        # If the base name is an empty string or None, set the base_name attribute to the name of the unit system,
        # otherwise set it to the given base name
        if base_name == '' or base_name is None:
            self.base_name = name
        else:
            self.base_name = base_name
        self.unit_id = unit_id
        self.literals = literals
        self.export_macro = export_macro
        self.out_dir = out_dir
        self.include_subdir = include_subdir
        self.src_subdir = src_subdir
        self.base_dir = base_dir

    # returns the path to the header file for the unit system
    def get_header_path(self) -> str:
        # If an output directory was specified, use it, otherwise use the default output directory
        if self.out_dir:
            path = self.out_dir
        else:
            path = os.path.join(self.base_dir, self.include_subdir)
        
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
        if self.out_dir:
            path = self.out_dir
        else:
            path = os.path.join(self.base_dir, self.src_subdir)
        
        # Append the name of the unit system and the .cpp file extension
        # to the output directory to get the path to the source file
        path = os.path.join(path, self.name + '.cpp')

        # create any missing directories in the path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    # generates the source files for a given unit system
    def generate(self):
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
        }

        # generate the header
        generators.utils.fill_template(
            os.path.join(template_dir, 'header.template'),  # the path to the header template file
            fill_dict,  # the values to fill into the template
            self.get_header_path()  # the path to the output header file
        )

        # generate the source
        generators.utils.fill_template(
            os.path.join(template_dir, 'source.template'),  # the path to the source template file
            fill_dict,  # the values to fill into the template
            self.get_source_path()  # the path to the output source file
        )


# This function takes a JSON object string as its argument and returns a Unit object
def unit_from_json(json_object_str: Dict, base_dir: str) -> Unit:
    # Extract the values from the JSON object string and assign them to variables
    name = json_object_str['name']
    base_name = json_object_str['base_name']
    unit_id = json_object_str['unit_id']
    export_macro = ''
    out_dir = ''
    if 'export_macro' in json_object_str:
        export_macro = json_object_str['export_macro']
    if 'out_dir' in json_object_str:
        out_dir = json_object_str['out_dir']

    # Use the get() method to get the 'literals' value from the JSON object string,
    # with an empty list as the default value
    literals = json_object_str.get('literals', [])

    # Use a list comprehension to create the 'literals' list
    literals = [UnitLiteral(literal) for literal in literals]

    # Return a Unit object, using keyword arguments to specify the names of the arguments
    return Unit(name, base_name, unit_id, literals, export_macro, out_dir, base_dir)


def units_from_file(
        file_location: os.path,
        base_dir: os.path,
        out_dir: os.path,
        export_macro: str,
        print_files: bool = False
) -> (List[Unit], List[str]):

    json_string = generators.utils.load_file_to_string(file_location)
    units = [unit_from_json(unit, base_dir) for unit in json.loads(json_string)]

    # update the export macro and output directory for each unit
    for unit in units:
        unit.export_macro = export_macro
        unit.out_dir = out_dir
        unit.base_dir = base_dir

    unit_strings = []

    # iterate over the units, generating the source files for each unit and
    # appending the unit name to the 'unit_strings' list
    for unit in units:
        unit.generate()
        unit_strings += [unit.name]

        # if the 'printOutFiles' flag is set to True, print the paths of the generated files
        if print_files:
            print(unit.get_header_path())
            print(unit.get_source_path())

    return units, unit_strings
