import os

import generators.utils
import generators.embedded.unit
import generators.embedded.specials

import distutils.file_util
import distutils.dir_util


class ArduinoConfig:
    def __init__(
            self,
            version: str,
            main_script_dir: os.path,
            base_dir: os.path,
            print_files: bool = False
    ):
        self.version = version
        self.export_macro = ''
        self.main_script_dir = main_script_dir
        self.base_dir = base_dir
        self.source_dir = os.path.join(base_dir, 'src')
        self.print_files = print_files

        script_dir = os.path.realpath(os.path.dirname(__file__))
        self.template_dir = os.path.join(script_dir, 'arduino')
        self.type_location = os.path.join(main_script_dir, 'type data')

        self.units = []
        self.unit_strings = []
        self.hasCombinations = True

    def generate_sources(self):
        self.units, self.unit_strings = generators.embedded.unit.units_from_file(
            os.path.join(self.type_location, 'units.json'),
            self.source_dir,
            self.export_macro,
            self.print_files,
            create_subdir=False,
            use_alternate_names=True
        )

        fill_dict = generators.embedded.specials.fill_from_files(
            self.type_location,
            self.export_macro,
            self.unit_strings,
        )

        fill_dict['target'] = 'arduino'

        # generate the header files for the unit system library
        generators.embedded.specials.create_headers(
            fill_dict,
            self.source_dir,
            create_subdir=False
        )

    def generate_system(self):

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(self.template_dir, 'library.properties.template'),
            {'version': self.version},
            os.path.join(self.base_dir, 'library.properties')
        )

        # copy the .github folder
        ci_dir = os.path.join(self.template_dir, '.github')
        distutils.dir_util.copy_tree(ci_dir, os.path.join(self.base_dir, '.github'))

        # copy the examples folder
        examples_dir = os.path.join(self.template_dir, 'examples')
        distutils.dir_util.copy_tree(examples_dir, os.path.join(self.base_dir, 'examples'))

    def generate(self):
        self.generate_sources()
        self.generate_system()
