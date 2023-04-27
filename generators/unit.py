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


# generates the source files for a given unit system
def generate_sources(current_unit: Unit):
    # the directory containing the template files
    template_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'templates')

    # the values to fill into the templates
    fill_dict = {
        'unit_name': current_unit.name,  # the name of the unit system
        'unit_base_name': current_unit.base_name,  # the base name of the unit system
        'unit_id': current_unit.unit_id,  # the unit ID of the unit system
        'literals': current_unit.literals,  # a list of UnitLiteral objects that represent
                                            # the literals for the unit system
        'create_literals': len(current_unit.literals) > 0,  # create literals if there is at least one
        'export_macro': current_unit.export_macro,  # the export macro for the unit system
    }

    # generate the header
    generators.utils.fill_template(
        os.path.join(template_dir, 'header.template'),  # the path to the header template file
        fill_dict,  # the values to fill into the template
        current_unit.get_header_path()  # the path to the output header file
    )

    # generate the source
    generators.utils.fill_template(
        os.path.join(template_dir, 'source.template'),  # the path to the source template file
        fill_dict,  # the values to fill into the template
        current_unit.get_source_path()  # the path to the output source file
    )


# if the script is run directly (not imported as a module), execute the code below
if __name__ == "__main__":
    # create the parser for the cmd inputs
    msg = "A code generator for the unit system library.\n"
    msg += "This script generates all headers that build on top of the individual units."

    parser = argparse.ArgumentParser(
        description=msg
    )

    # define the 'name' argument, which is required and should be a string
    parser.add_argument(
        "-n",
        "--name",
        help="name of the unit",
        required=True,
        type=str,
        dest='name'
    )

    # define the 'baseName' argument, which is optional and should be a string
    parser.add_argument(
        "--baseName",
        help="the name of the basic unit (e.g. meters for length).",
        required=False,
        type=str,
        dest='baseName'
    )

    # define the 'unit_identifier' argument, which is required and should be an integer
    parser.add_argument(
        "-id",
        "--unit_identifier",
        help="id of the unit",
        required=True,
        type=int,
        dest='unit_id'
    )

    # define the 'literals' argument, which is optional, should be a string, and can be provided multiple times
    parser.add_argument(
        "-l",
        "--literal",
        help="a literal of the unit in json format. One literal per argument.",
        required=False,
        type=str,
        dest='literals',
        action='append'
    )

    # define the 'baseDir' argument, which is optional, should be a string, and has a default value of 'generated'
    parser.add_argument(
        "--baseDir",
        help="the base directory to output to",
        required=False,
        default='generated',
        type=str,
        dest='baseDir'
    )

    # define the 'exportMacro' argument, which is optional, has a default value of '',
    # and is set to 'UNIT_SYSTEM_EXPORT_MACRO '
    # if the argument is provided
    parser.add_argument(
        "--exportMacro",
        help="the export macro that should be used for the types",
        required=False,
        default='',
        dest='exportMacro',
        action='store_const',
        const='UNIT_SYSTEM_EXPORT_MACRO '
    )

    # define the 'outDir' argument, which is optional, should be a string, and has a default value of ''
    parser.add_argument(
        "--outDir",
        help="Put all files in the same given directory. This overwrites the baseDir.",
        required=False,
        default='',
        dest='outDir',
        type=str,
    )

    args = vars(parser.parse_args())

    # create a list of UnitLiteral objects from the literals provided in the arguments
    currLiteral = []
    if args['literals']:
        for data in args['literals']:
            currLiteral.append(UnitLiteral(json.loads(data)))

    # create a Unit object using the provided arguments
    currUnit = Unit(
        args['name'],
        args['baseName'],
        args['unit_id'],
        currLiteral,
        args['exportMacro'],
        args['outDir'],
        args['baseDir'],
    )

    # generate the sources for the unit
    generate_sources(currUnit)
