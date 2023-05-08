import os

import generators.utils
import generators.Cpp17.unit
import generators.Cpp17.specials

import distutils.file_util
import distutils.dir_util


class MesonConfig:
    def __init__(
            self,
            version: str,
            main_script_dir: os.path,
            base_dir: os.path,
            print_files: bool = False
    ):
        self.version = version
        self.export_macro = 'UNIT_SYSTEM_EXPORT_MACRO'
        self.main_script_dir = main_script_dir
        self.base_dir = base_dir
        self.print_files = print_files

        script_dir = os.path.realpath(os.path.dirname(__file__))
        self.template_dir = os.path.join(script_dir, 'meson')
        self.type_location = os.path.join(main_script_dir, 'type data')

        self.units = []
        self.unit_strings = []
        self.hasCombinations = True

    def generate_sources(self):
        self.units, self.unit_strings = generators.Cpp17.unit.units_from_file(
            os.path.join(self.type_location, 'units.json'),
            self.base_dir,
            self.export_macro,
            self.print_files
        )

        fill_dict = generators.Cpp17.specials.fill_from_files(
            self.type_location,
            self.export_macro,
            self.unit_strings
        )

        # generate the header files for the unit system library
        generators.Cpp17.specials.create_headers(
            fill_dict,
            self.base_dir
        )

    def generate_system(self):

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(self.template_dir, 'meson.build.template'),
            {
                'version': self.version,
                'export_macro': self.export_macro,
                'units': self.unit_strings,
            },
            os.path.join(self.base_dir, 'meson.build')
        )

        # copy the meson options file
        meson_options = os.path.join(self.template_dir, 'meson_options.txt')
        distutils.file_util.copy_file(meson_options, os.path.join(self.base_dir, 'meson_options.txt'))

        # copy the tests
        tests_dir = os.path.join(self.template_dir, 'tests')
        distutils.dir_util.copy_tree(tests_dir, os.path.join(self.base_dir, 'tests'))

        # copy the subprojects folder
        subprojects_dir = os.path.join(self.template_dir, 'subprojects')
        distutils.dir_util.copy_tree(subprojects_dir, os.path.join(self.base_dir, 'subprojects'))

    def generate(self):
        self.generate_sources()
        self.generate_system()
