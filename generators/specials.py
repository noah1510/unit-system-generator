import argparse
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
    gen_unit_t: bool,
    gen_unit_header: bool,
    gen_combinations: bool,
    gen_constants: bool,
    output_dir: os.path,
    base_dir: os.path,
    print_file: False,
):
    # Get the absolute path of the script directory.
    script_dir = os.path.realpath(os.path.dirname(__file__))

    # Get the absolute path of the templates' directory, which is in the script directory.
    template_dir = os.path.join(script_dir, 'templates')

    # set the correct header and source directories
    if output_dir == '':
        header_dir = os.path.join(base_dir, 'include')
        header_dir = os.path.join(header_dir, 'unit_system')

        source_dir = os.path.join(base_dir, 'src')
    else:
        header_dir = output_dir
        source_dir = output_dir

    # If `gen_unit_t` is `True`, fill in the "unit_type.template" file with the data in `fill_dict`
    # and write the output to the "unit_t.hpp" file in the output directory.
    if gen_unit_t:
        generators.utils.fill_template(
            os.path.join(template_dir, 'unit_type.template'),
            fill_dict,
            os.path.join(header_dir, 'unit_t.hpp')
        )
        if print_file:
            print(os.path.join(header_dir, 'unit_t.hpp'))

    # If `gen_unit_header` is `True`, fill in the "units.template" file with the data in `fill_dict`
    # and write the output to the "units.hpp" file in the output directory.
    if gen_unit_header:
        generators.utils.fill_template(
            os.path.join(template_dir, 'units.template'),
            fill_dict,
            os.path.join(header_dir, 'units.hpp')
        )
        if print_file:
            print(os.path.join(header_dir, 'units.hpp'))

    # If `gen_combinations` is `True`, fill in the "header_combine.template" file with the data in `fill_dict`
    # and write the output to the "combinations.hpp" file in the output directory.
    if gen_combinations:
        generators.utils.fill_template(
            os.path.join(template_dir, 'header_combine.template'),
            fill_dict,
            os.path.join(header_dir, 'combinations.hpp')
        )

        # Also fill in the "source_combine.template" file with the data in `fill_dict`
        # and write the output to the "combinations.cpp" file in the output directory.
        generators.utils.fill_template(
            os.path.join(template_dir, 'source_combine.template'),
            fill_dict,
            os.path.join(source_dir, 'combinations.cpp')
        )
        if print_file:
            print(os.path.join(header_dir, 'combinations.hpp'))
            print(os.path.join(source_dir, 'combinations.cpp'))

    # If `gen_constants` is `True`, fill in the "constants.template" file with the data in `fill_dict`
    # and write the output to the "constants.hpp" file in the output directory.
    if gen_constants:
        generators.utils.fill_template(
            os.path.join(template_dir, 'constants.template'),
            fill_dict,
            os.path.join(header_dir, 'constants.hpp')
        )
        if print_file:
            print(os.path.join(header_dir, 'constants.hpp'))


# If this script is run directly (as opposed to being imported as a module),
# parse the command-line arguments and call `create_headers()` with the appropriate arguments.
if __name__ == "__main__":
    # Set the description message for the command-line interface (CLI).
    msg = "A code generator for the unit system library.\n"
    msg += "This script generates the sources for all of the individual units."

    # Create a new `ArgumentParser` object.
    parser = argparse.ArgumentParser(
        description=msg
    )

    # Define a command-line argument for specifying one or more units.
    parser.add_argument(
        "-u",
        "--unit",
        help="a unit that is enabled and generated. One literal per argument.",
        required=False,
        type=str,
        dest='units',
        action='append'
    )

    # Define a command-line argument for specifying one or more unit combinations.
    parser.add_argument(
        "-c",
        "--combine",
        help="combine two units, so that unit0 * unit1 = unit2",
        required=False,
        type=str,
        dest='combinations',
        action='append',
        nargs=3,
    )

    # Define a command-line argument for specifying one or more constant values.
    parser.add_argument(
        "--constant",
        help="a constant value that gets defined.",
        required=False,
        type=str,
        dest='constants',
        action='append',
        nargs=2,
    )

    # Define a command-line argument for specifying the export macro to use for the types.
    parser.add_argument(
        "--exportMacro",
        help="the export macro that should be used for the types",
        required=False,
        default='',
        dest='exportMacro',
        action='store_const',
        const='UNIT_SYSTEM_EXPORT_MACRO '
    )

    # Define a command-line argument for specifying the output directory.
    parser.add_argument(
        "--outDir",
        help="Put all files in the same given directory. This overwrites the baseDir.",
        required=True,
        default='',
        dest='outDir',
        type=str,
    )

    # Define a command-line argument for specifying whether to generate the "units.hpp" file.
    parser.add_argument(
        "--unitHeader",
        help="This should generate the unitHeader",
        required=False,
        default=False,
        dest='unitHeader',
        action='store_true'
    )

    # Define a command-line argument for specifying whether to generate the
    # "combinations.cpp" and "combinations.hpp" files.
    parser.add_argument(
        "--combinations",
        help="This should generate the combinations headers and sources",
        required=False,
        default=False,
        dest='genCombinations',
        action='store_true'
    )

    # Define a command-line argument for specifying whether to generate the "constants.hpp" file.
    parser.add_argument(
        "--genConstants",
        help="This should generate the constants headers",
        required=False,
        default=False,
        dest='genConstants',
        action='store_true'
    )

    # Define a command-line argument for specifying whether to include the standard library headers.
    parser.add_argument(
        "--disableSTD",
        help="This disables the inclusion of standard library headers",
        required=False,
        default=False,
        dest='disableSTD',
        action='store_true'
    )

    # Define a command-line argument for specifying whether to generate the "unit_t.hpp" file.
    parser.add_argument(
        "--genUnit_t",
        help="This should generate the unit_t header",
        required=False,
        default=False,
        dest='genUnit_t',
        action='store_true'
    )

    # Parse the command-line arguments.
    args = parser.parse_args()

    # Initialize an empty dictionary for storing the data to fill in the templates.
    fillDict = {}

    # If the `units` argument was provided, set the `units` key in the `fill_dict` dictionary
    # to a list of the specified unit literals.
    if args.units is not None:
        fillDict['units'] = args.units

    # If the `combinations` argument was provided, set the `combinations` key in the `fill_dict` dictionary
    # to a list of the specified unit combination tuples.
    if args.combinations is not None:
        fillDict['combinations'] = args.combinations

    # If the `constants` argument was provided, set the `constants` key in the `fill_dict` dictionary
    # to a list of the specified constant value tuples.
    if args.constants is not None:
        fillDict['constants'] = args.constants

    # If the `exportMacro` argument was provided, set the `exportMacro` key in the `fill_dict` dictionary
    # to the specified export macro.
    if args.exportMacro is not None:
        fillDict['exportMacro'] = args.exportMacro

    outputDir = ''
    # If the `outDir` argument was provided, set the `output_dir` variable to the specified output directory.
    if args.outDir is not None:
        outputDir = args.outDir

    # Call the `create_headers()` function to generate the specified files.
    create_headers(
        fillDict,
        gen_unit_t=True,
        gen_unit_header=args.unitHeader,
        gen_combinations=args.genCombinations,
        gen_constants=True,
        output_dir=outputDir
    )
