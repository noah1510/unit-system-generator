import os.path
import argparse

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
        "--noExportMacro",
        help="the export macro that should be used for the types",
        required=False,
        default='UNIT_SYSTEM_EXPORT_MACRO',
        dest='exportMacro',
        action='store_const',
        const=''
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

    # get the value of the 'outDir' argument
    outDir = args['outDir']

    # if the 'genArduino' flag is set to True, use the arduino generator
    # otherwise, use the meson generator
    if args['genArduino']:
        # get the path of the 'src' subdirectory of the 'unit-system-adruino' directory
        arduino_src_dir = os.path.join(main_script_dir, 'unit-system-adruino')
        arduino_src_dir = os.path.join(arduino_src_dir, 'src')

        # if the 'outDir' argument was not provided, set the 'outDir' to the 'src' directory
        if outDir == '':
            outDir = arduino_src_dir

        # set the 'genStd' flag to False
        genStd = False

    else:
        # generate all meson build system files
        meson_conf = generators.meson.MesonConfig(
            '0.7.0',
            args['exportMacro'],
            main_script_dir,
            outDir,
            base_dir,
            args['printOutFiles']
        )

        meson_conf.generate()
