import os
from pathlib import Path
from typing import List, Dict

import generator_code.utils
import generator_code.prefixes
import generator_code.combination


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
            templates: List[generator_code.utils.Template] = None,
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
            'name_pascal': data['name'].replace("_", " ").title().replace(" ", ""),
            'unit_id': data['unit_id'],
            'literals': data.get('literals', []),
            'combinations': data.get('combinations', []),
            'dependencies': generator_code.combination.get_all_deps_for(data['name'], data.get('combinations', [])),
            'multiplications': generator_code.combination.get_multiplication_for(data['name'], data.get('combinations', [])),
            'divisions': generator_code.combination.get_division_for(data['name'], data.get('combinations', [])),
            'sqrt_result': generator_code.combination.get_sqrt_for(data['name'], data.get('combinations', [])),
            'square_result': generator_code.combination.get_square_for(data['name'], data.get('combinations', [])),
            'extra_data': data.get('extra_data', {}),
        })

        self.templates = templates

    def add_template(self, template: generator_code.utils.Template):
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


def generate_data(
        main_script_dir: Path,
        extra_data: Dict = None,
        data_overrides: Dict = None,
        print_files: bool = False,
        per_unit_templates: List[Dict] = None,
        unit_type: type(Unit) = Unit,
) -> Dict:

    type_location = (main_script_dir / 'type data').expanduser().absolute()

    # load all files into json objects
    units_json = generator_code.utils.File(type_location / 'units.json').read_json()
    combinations = generator_code.combination.load_all_combinations(type_location / 'combinations.json')
    constants_json = generator_code.utils.File(type_location / 'constants.json').read_json()

    # apply the rename part of the overrides
    if data_overrides is not None and 'rename_unit' in data_overrides:
        rename_unit = data_overrides['rename_unit']
        for comb in combinations:
            comb.apply_rename(rename_unit)

        for unit in units_json:
            if unit['name'] in rename_unit:
                unit['name'] = rename_unit[unit['name']]

    # create the unit objects
    units = [generator_code.unit.unit_from_json(
        unit,
        combinations=combinations,
        extra_data=extra_data,
        unit_type=unit_type,
        literal_override=data_overrides.get('literals', {}).get(unit['name'], None),
    ) for unit in units_json]

    # add the template files for the per-unit templates to each unit
    for unit in units:
        if per_unit_templates is not None:
            for fileinfo in per_unit_templates:
                infile = fileinfo['infile'].get()
                out_dir = fileinfo['out_dir']

                out_filename = fileinfo['file_format'].format(unit=unit)
                out_path = out_dir / out_filename

                unit.add_template(generator_code.utils.Template(infile, out_path))

    # create a fict will all the generated data
    fill_dict = {
        'units': units,
        'combinations': combinations,
        'constants': [constant for constant in constants_json],
        'extra_data': extra_data,
    }

    return fill_dict


# This function takes a JSON object string as its argument and returns a Unit object
def unit_from_json(
        json_object_str: Dict,
        extra_data: Dict = None,
        combinations: List[generator_code.combination.Combination] = None,
        literal_override: Dict = None,
        unit_type: type(Unit) = Unit,
):

    # Use the get() method to get the 'literals' value from the JSON object string,
    # with an empty list as the default value
    literals = json_object_str.get('literals', [])

    # Use a list comprehension to create the 'literals' list
    literals = [UnitLiteral(literal) for literal in literals]
    try:
        literals = generate_prefixed_literals(
            literals,
            json_object_str.get('generated_multipliers', None),
            literal_override
        )
    except KeyError:
        pass

    json_object_str['literals'] = literals

    if combinations is not None:
        json_object_str['combinations'] = (
            generator_code.combination.get_defined_for(json_object_str['name'], combinations))

    if extra_data is None:
        extra_data = {}

    json_object_str['extra_data'] = extra_data

    # Return a Unit object, using keyword arguments to specify the names of the arguments
    return unit_type(json_object_str)


def generate_prefixed_literals(
        literals: List[UnitLiteral],
        generated_multipliers: Dict = None,
        literal_override: Dict = None,
) -> List[UnitLiteral]:

    # get the prefixes that should be generated
    all_literals = literals

    # generate the multipliers if needed
    if generated_multipliers is not None:
        for literal in literals:
            if literal.name in generated_multipliers:
                prefixes_to_generate = generated_multipliers[literal.name]
                for prefix in prefixes_to_generate:
                    try:
                        prefix_data = generator_code.prefixes.Prefix.from_string(prefix)
                    except ValueError as Error:
                        print(Error)
                        raise ValueError(
                            f'Invalid prefix {prefix} for literal {literal.name}'
                        )

                    prefix_json = {
                        "name": prefix + literal.name,
                        "multiplier": prefix_data.value() * literal.multiplier,
                        "code_literal": prefix_data.short() + literal.code_literal,
                        "offset": literal.offset,
                    }
                    all_literals.append(UnitLiteral(prefix_json))

    # apply the overrides to the full list of literals
    if literal_override is not None:
        for literal in all_literals:
            if literal.name in literal_override:
                override_data = literal_override[literal.name]
                literal.name = override_data.get('name', literal.name)
                literal.code_literal = override_data.get('code_literal', literal.code_literal)
                literal.multiplier = override_data.get('multiplier', literal.multiplier)
                literal.offset = override_data.get('offset', literal.offset)

    return all_literals
