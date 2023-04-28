import json
import os

import generators.utils
import generators.unit
import generators.specials

import distutils.file_util
import distutils.dir_util


class MesonConfig:
    def __init__(
            self,
            version: str,
            export_macro: str,
            main_script_dir: os.path,
            out_dir: os.path,
            base_dir: os.path,
            print_files: bool = False
    ):
        self.version = version
        self.export_macro = export_macro
        self.main_script_dir = main_script_dir
        self.out_dir = out_dir
        self.base_dir = base_dir
        self.print_files = print_files

        script_dir = os.path.realpath(os.path.dirname(__file__))
        self.template_dir = os.path.join(script_dir, 'meson')
        self.type_location = os.path.join(main_script_dir, 'type data')

        self.units = []
        self.unit_strings = []
        self.hasCombinations = True

    def generate_sources(self):
        self.units, self.unit_strings = generators.unit.units_from_file(
            os.path.join(self.type_location, 'units.json'),
            self.base_dir,
            self.out_dir,
            self.export_macro,
            self.print_files
        )

        # load the 'combinations.json' file and parse its contents as a JSON string
        json_string = generators.utils.load_file_to_string(os.path.join(self.type_location, 'combinations.json'))
        combinations = [[comb['factor1'], comb['factor2'], comb['product']] for comb in json.loads(json_string)]

        # load the 'constants.json' file and parse its contents as a JSON string
        json_string = generators.utils.load_file_to_string(os.path.join(self.type_location, 'constants.json'))
        constants = [constant for constant in json.loads(json_string)]

        # create a dictionary containing the values that will be used to generate the header files
        fill_dict = {
            'export_macro': self.export_macro,
            'units': self.unit_strings,
            'disable_std': False,
            'combinations': combinations,
            'constants': constants,
        }

        # generate the header files for the unit system library
        generators.specials.create_headers(
            fill_dict,
            True,
            True,
            True,
            True,
            self.out_dir,
            self.base_dir,
            self.print_files
        )

        # copy the general includes file to the output directory
        includes_folder = os.path.realpath(os.path.join(self.main_script_dir, 'include'))
        if self.out_dir != '':
            output_header = os.path.realpath(os.path.join(self.out_dir, 'include'))
        else:
            output_header = os.path.realpath(os.path.join(self.base_dir, 'include'))

        distutils.dir_util.copy_tree(includes_folder, output_header)

    def generate_system(self):

        if self.out_dir == '':
            self.out_dir = self.base_dir

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(self.template_dir, 'meson.build.template'),
            {
                'version': self.version,
                'export_macro': self.export_macro,
                'units': self.unit_strings,
                'hasCombinations': self.hasCombinations,
            },
            os.path.join(self.out_dir, 'meson.build')
        )

        # copy the meson options file
        meson_options = os.path.join(self.template_dir, 'meson_options.txt')
        distutils.file_util.copy_file(meson_options, os.path.join(self.out_dir, 'meson_options.txt'))

        # copy the tests
        tests_dir = os.path.join(self.template_dir, 'tests')
        distutils.dir_util.copy_tree(tests_dir, os.path.join(self.out_dir, 'tests'))

        # copy the subprojects folder
        subprojects_dir = os.path.join(self.template_dir, 'subprojects')
        distutils.dir_util.copy_tree(subprojects_dir, os.path.join(self.out_dir, 'subprojects'))

    def generate(self):
        self.generate_sources()
        self.generate_system()
