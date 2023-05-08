import os
from typing import Dict

import generators.utils


# The `create_headers()` function generates several files based on templates and provided input data.
# It takes the following arguments:
#
# fill_dict: A dictionary containing the data to fill in the templates.
# gen_unit_t: A boolean indicating whether to generate the "unit_t.hpp" file.
# gen_unit_header: A boolean indicating whether to generate the "units.hpp" file.
# gen_combinations: A boolean indicating whether to generate the "combinations.cpp" and "combinations.hpp" files.
# gen_constants: A boolean indicating whether to generate the "constants.hpp" file.
# output_dir: The directory where the generated files should be saved.
# print_file: set to True to print the files that are generated
def create_headers(
    fill_dict: Dict,
    base_dir: os.path,
    print_file=False,
    create_subdir=True,  # control if the src and include directories should be created
    force_flat_headers=False,  # control if the unit_system directory should be created
):
    # Get the absolute path of the script directory.
    script_dir = os.path.realpath(os.path.dirname(__file__))

    # Get the absolute path of the templates' directory, which is in the script directory.
    template_dir = os.path.join(script_dir, 'templates')

    header_dir = base_dir
    header_base_dir = base_dir
    source_dir = base_dir
    if not force_flat_headers:
        if create_subdir:
            header_base_dir = os.path.join(header_base_dir, 'include')
            source_dir = os.path.join(source_dir, 'src')

        header_dir = os.path.join(header_base_dir, 'unit_system')

    fill_dict["force_flat_headers"] = force_flat_headers

    # If `gen_unit_t` is `True`, fill in the "unit_type.template" file with the data in `fill_dict`
    # and write the output to the "unit_t.hpp" file in the output directory.
    generators.utils.fill_template(
        os.path.join(template_dir, 'unit_type.hpp.template'),
        fill_dict,
        os.path.join(header_dir, 'unit_t.hpp')
    )

    # If `gen_unit_header` is `True`, fill in the "units.template" file with the data in `fill_dict`
    # and write the output to the "units.hpp" file in the output directory.
    generators.utils.fill_template(
        os.path.join(template_dir, 'units.hpp.template'),
        fill_dict,
        os.path.join(header_dir, 'units.hpp')
    )

    # If `gen_combinations` is `True`, fill in the "header_combine.template" file with the data in `fill_dict`
    # and write the output to the "combinations.hpp" file in the output directory.
    generators.utils.fill_template(
        os.path.join(template_dir, 'combinations.hpp.template'),
        fill_dict,
        os.path.join(header_dir, 'combinations.hpp')
    )

    # Also fill in the "source_combine.template" file with the data in `fill_dict`
    # and write the output to the "combinations.cpp" file in the output directory.
    generators.utils.fill_template(
        os.path.join(template_dir, 'combinations.cpp.template'),
        fill_dict,
        os.path.join(source_dir, 'combinations.cpp')
    )

    # If `gen_constants` is `True`, fill in the "constants.template" file with the data in `fill_dict`
    # and write the output to the "constants.hpp" file in the output directory.
    generators.utils.fill_template(
        os.path.join(template_dir, 'constants.hpp.template'),
        fill_dict,
        os.path.join(header_dir, 'constants.hpp')
    )

    generators.utils.fill_template(
        os.path.join(template_dir, 'std_implements.hpp.template'),
        fill_dict,
        os.path.join(header_dir, 'std_implements.hpp')
    )

    generators.utils.fill_template(
        os.path.join(template_dir, 'unit_system.hpp.template'),
        fill_dict,
        os.path.join(header_base_dir, 'unit_system.hpp')
    )

    if print_file:
        print(os.path.join(header_dir, 'unit_t.hpp'))
        print(os.path.join(header_dir, 'units.hpp'))
        print(os.path.join(header_dir, 'combinations.hpp'))
        print(os.path.join(source_dir, 'combinations.cpp'))
        print(os.path.join(header_dir, 'constants.hpp'))
        print(os.path.join(header_dir, 'std_implements.hpp'))
        print(os.path.join(header_dir, 'unit_system.hpp'))
