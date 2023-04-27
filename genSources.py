import json
import os.path
import argparse
import distutils.dir_util

import generators.utils
import generators.specials
import generators.unit
import generators.meson

# comments mostly generated by ChatGPT from openai and tweaked by me

# This block of code will only be executed if this script is run directly,
# rather than being imported by another script.
if __name__ == "__main__":
    # define the message that will be displayed when the user runs the script with the -h flag
    msg = "A code generator for the unit system library.\n"
    msg += "This script generates all units and contains all of the unit definitions."

    # create an ArgumentParser object to parse command line arguments
    parser = argparse.ArgumentParser(
        description=msg
    )

    # define the 'genArduino' argument, which is a flag that indicates whether
    # the output should be generated for Arduino
    parser.add_argument(
        "--genArduino",
        help="Generate the output for arduino",
        required=False,
        default=False,
        dest='genArduino',
        action='store_true'
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

    # define the 'exportMacro' argument, which is optional and has a default value of ''
    parser.add_argument(
        "--exportMacro",
        help="the export macro that should be used for the types",
        required=False,
        default='',
        dest='exportMacro',
        action='store_const',
        const='UNIT_SYSTEM_EXPORT_MACRO '
    )

    # define the 'printOutFiles' argument, which is a flag that indicates whether
    # the generated files should be printed
    parser.add_argument(
        "--printOutFiles",
        help="set to true if the generated file should be print",
        required=False,
        default=False,
        dest='printOutFiles',
        action='store_true',
    )

    # parse the command line arguments
    args = vars(parser.parse_args())

    # get the directory containing the script
    main_script_dir = os.path.realpath(os.path.dirname(__file__))
    base_dir = os.path.join(main_script_dir, 'output')

    # get the path of the templates directory
    template_dir = os.path.join(main_script_dir, 'templates')
    type_data_dir = os.path.join(main_script_dir, 'type data')

    # get the value of the 'printOutFiles' argument
    printFiles = args['printOutFiles']

    # set the 'genStd' flag to True
    genStd = True

    # get the value of the 'outDir' argument
    outDir = args['outDir']

    # if the 'genArduino' flag is set to True, set the 'outDir' to the 'src'
    # subdirectory of the 'unit-system-adruino' directory
    if args['genArduino']:
        # get the path of the 'src' subdirectory of the 'unit-system-adruino' directory
        arduino_src_dir = os.path.join(main_script_dir, 'unit-system-adruino')
        arduino_src_dir = os.path.join(arduino_src_dir, 'src')

        # if the 'outDir' argument was not provided, set the 'outDir' to the 'src' directory
        if outDir == '':
            outDir = arduino_src_dir

        # set the 'genStd' flag to False
        genStd = False

    # load the 'units.json' file and parse its contents as a JSON string
    json_string = generators.utils.load_file_to_string(os.path.join(type_data_dir, 'units.json'))

    # Use a list comprehension to parse the JSON string and create the 'units' list
    units = [generators.unit.unit_from_json(unit, base_dir) for unit in json.loads(json_string)]

    # Use the update() method to update the 'export_macro' and 'out_dir' keys in the 'units' list
    for unit in units:
        unit.export_macro = args['exportMacro']
        unit.out_dir = outDir

    # load the 'combinations.json' file and parse its contents as a JSON string
    json_string = generators.utils.load_file_to_string(os.path.join(type_data_dir, 'combinations.json'))
    combinations = [[comb['factor1'], comb['factor2'], comb['product']] for comb in json.loads(json_string)]

    # load the 'constants.json' file and parse its contents as a JSON string
    json_string = generators.utils.load_file_to_string(os.path.join(type_data_dir, 'constants.json'))
    constants = [constant for constant in json.loads(json_string)]

    # create an empty list to store the unit names
    unit_strings = []

    # iterate over the units, generating the source files for each unit and
    # appending the unit name to the 'unit_strings' list
    for unit in units:
        generators.unit.generate_sources(unit)
        unit_strings += [unit.name]

        # if the 'printOutFiles' flag is set to True, print the paths of the generated files
        if printFiles:
            print(unit.get_header_path())
            print(unit.get_source_path())

    # create a dictionary containing the values that will be used to generate the header files
    fillDict = {
        'export_macro': args['exportMacro'],
        'units': unit_strings,
        'disable_std': not genStd,
        'combinations': combinations,
        'constants': constants,
    }

    # generate the header files for the unit system library
    generators.specials.create_headers(
        fillDict,
        True,
        True,
        True,
        True,
        outDir,
        base_dir,
        printFiles
    )

    # copy the general includes file to the output directory
    includes_folder = os.path.realpath(os.path.join(main_script_dir, 'include'))
    if outDir != '':
        output_header = os.path.realpath(os.path.join(outDir, 'include'))
    else:
        output_header = os.path.realpath(os.path.join(base_dir, 'include'))
    distutils.dir_util.copy_tree(includes_folder, output_header)

    meson_conf = generators.meson.MesonConfig(
        '0.7.0',
        args['exportMacro'],
        unit_strings,
        True
    )

    meson_conf.generate(outDir, base_dir)
