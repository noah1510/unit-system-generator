import os
from pathlib import Path
from typing import List, Dict

import generators.utils
import generators.python.generic.prefixes
import generators.combination


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
        self.code_literal = _data['code_literal']

        # Set the UDL that should be used for the literal instead of the normal literal
        if 'udl_override' in _data:
            self.udl = _data['udl_override']
        else:
            self.udl = self.code_literal

        # Set the alternative name that should be used on problematic platforms
        if 'code_alternative' in _data:
            self.alternative = _data['code_alternative']
        else:
            self.alternative = self.udl

        # If the input dictionary contains a 'multiplier' key, set the multiplier attribute
        # to the corresponding value, otherwise set it to 1.0
        if 'multiplier' in _data:
            self.multiplier = float(_data['multiplier'])
        else:
            self.multiplier = 1.0

        # If the input dictionary contains an 'offset' key, set the offset attribute
        # to the corresponding value, otherwise set it to 0.0
        if 'offset' in _data:
            self.offset = float(_data['offset'])
        else:
            self.offset = 0.0


# A class representing a unit fo the unit system.
#
# Attributes of the data dictionary:
#   required:
#     name: The name of the unit.
#     unit_id: The unique ID of the unit.
#
#   optional:
#     base_name: The base name of the unit. If the base name is not provided, this will be
#                set to the value of the `name` attribute.
#     literals: A list of `UnitLiteral` objects that represent the literals for the unit.
#     combinations: A list of 'Combinations' objects that represent the combinations for the unit.
#     export_macro: The export macro for the unit.
#     force_flat_headers: Whether to force the header files to be in the same directory as the source files
#     use_alternate_names: Whether to use alternate names for literals on problematic platforms
#     extra_data: A dictionary containing extra data that should be passed to the templates.
#
# other parameters:
#     templates: A list of Templates that should be generated from this Unit.
class Unit(Dict):
    def __init__(
            self,
            data: Dict,
            templates: List[generators.utils.Template] = None,
    ):

        # first check if all required keys are present and raise an error if they are not
        if 'name' not in data:
            raise ValueError('Unit must have a name')

        if 'unit_id' not in data:
            raise ValueError('Unit must have a unit ID')

        if 'base_literal' not in data or data['base_literal'] is None or data['base_literal'] == '':
            data['base_name'] = data['name']
        else:
            data['base_name'] = data['base_literal']

        # If the base name is an empty string or None, set the base_name attribute to the name of the unit system,
        # otherwise set it to the given base name
        if 'base_name' not in data or data['base_name'] == '' or data['base_name'] is None:
            data['base_name'] = data['name']

        super().__init__({
            'name': data['name'],
            'base_name': data['base_name'],
            'unit_id': data['unit_id'],
            'literals': data.get('literals', []),
            'combinations': data.get('combinations', []),
            'dependencies': generators.combination.get_all_deps_for(data['name'], data.get('combinations', [])),
            'multiplications': generators.combination.get_multiplication_for(data['name'], data.get('combinations', [])),
            'divisions': generators.combination.get_division_for(data['name'], data.get('combinations', [])),
            'extra_data': data.get('extra_data', {}),
        })

        self.templates = templates

    def add_template(self, template: generators.utils.Template):
        if self.templates is None:
            self.templates = []

        self.templates.append(template)

    def generate(self, print_files: bool = False):
        if self.templates is None:
            return

        for template in self.templates:
            template.fill_with(self)
            if print_files:
                print(template.output_file)


def units_from_file(
        main_script_dir: Path,
        print_files: bool = False,
        extra_data: Dict = None,
        per_unit_templates: List[Dict] = None,
        unit_type: type(Unit) = Unit,
) -> List[type(Unit)]:

    file_location = main_script_dir / 'type data' / 'units.json'
    units_file = generators.utils.File(file_location.expanduser().absolute())

    combinations = generators.combination.load_all_combinations(main_script_dir / 'type data' / 'combinations.json')

    # create a list of Unit objects from the JSON object string
    units = [generators.unit.unit_from_json(
        unit,
        combinations=combinations,
        extra_data=extra_data,
        unit_type=unit_type
    ) for unit in units_file.read_json()]

    # iterate over the units, generating the source files for each unit and
    # appending the unit name to the 'unit_strings' list
    for unit in units:
        if per_unit_templates is not None:
            for fileinfo in per_unit_templates:
                infile = fileinfo['infile'].get()
                out_dir = fileinfo['out_dir']

                out_filename = fileinfo['file_format'].format(unit=unit)
                out_path = out_dir / out_filename

                unit.add_template(generators.utils.Template(infile, out_path))

    return units


# This function takes a JSON object string as its argument and returns a Unit object
def unit_from_json(
        json_object_str: Dict,
        extra_data: Dict = None,
        combinations: List[generators.combination.Combination] = None,
        unit_type: type(Unit) = Unit,
):

    # Use the get() method to get the 'literals' value from the JSON object string,
    # with an empty list as the default value
    literals = json_object_str.get('literals', [])

    # Use a list comprehension to create the 'literals' list
    literals = [UnitLiteral(literal) for literal in literals]
    try:
        literals = generate_prefixed_literals(literals, json_object_str)
    except KeyError:
        pass

    json_object_str['literals'] = literals

    if combinations is not None:
        json_object_str['combinations'] = generators.combination.get_defined_for(json_object_str['name'], combinations)
        json_object_str['dependencies'] = generators.combination.get_all_deps_for(json_object_str['name'], combinations)

    if extra_data is None:
        extra_data = {}

    json_object_str['extra_data'] = extra_data

    # Return a Unit object, using keyword arguments to specify the names of the arguments
    return unit_type(json_object_str)


def generate_prefixed_literals(
        literals: List[UnitLiteral],
        json_object_str: Dict,
) -> List[UnitLiteral]:

    if 'generated_multipliers' not in json_object_str:
        return literals

    # get the prefixes that should be generated
    all_literals = literals
    prefixes = json_object_str['generated_multipliers']
    for literal in literals:
        if literal.name in prefixes:
            prefixes_to_generate = prefixes[literal.name]
            for prefix in prefixes_to_generate:
                try:
                    multiplier, code_literal = generators.python.generic.prefixes.Prefix.from_string(prefix)
                except ValueError as Error:
                    print(Error)
                    raise ValueError(
                        f'Invalid prefix {prefix} for unit {literal.name} in unit system {json_object_str["name"]}'
                    )

                prefix_json = {
                    "name": prefix + literal.name,
                    "multiplier": multiplier * literal.multiplier,
                    "code_literal": code_literal + literal.code_literal,
                    "code_alternative": code_literal + literal.alternative,
                    "offset": literal.offset,
                }
                all_literals.append(UnitLiteral(prefix_json))

    return all_literals


def fill_from_files(
        type_location: Path,
        units: List[Unit],
        extra_data: Dict = None,
) -> Dict:

    # load the 'combinations.json' file and parse its contents as a JSON string
    combinations = generators.combination.load_all_combinations(type_location / 'combinations.json')

    # load the 'constants.json' file and parse its contents as a JSON string
    constants_file = generators.utils.File(type_location / 'constants.json')
    constants = [constant for constant in constants_file.read_json()]

    # create a dictionary containing the values that will be used to generate the header files
    fill_dict = {
        'units': units,
        'combinations': combinations,
        'constants': constants,
        'extra_data': extra_data,
    }

    return fill_dict
