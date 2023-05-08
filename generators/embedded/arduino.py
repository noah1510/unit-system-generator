import os

import generators.utils
import generators.target
import generators.unit
import generators.embedded.unit
import generators.embedded.specials


class ArduinoConfig(generators.target.Target):
    def __init__(
            self,
            version: str,
            main_script_dir: os.path,
            base_dir: os.path,
            print_files: bool = False
    ):
        super().__init__(
            version,
            main_script_dir,
            base_dir,
            print_files,
            enable_export_macro=False,
            target_name='arduino',
            script_dir=os.path.realpath(os.path.dirname(__file__))
        )

        self.source_dir = os.path.join(base_dir, 'src')

    def generate_sources(self):
        self.units, self.unit_strings = generators.unit.units_from_file(
            os.path.join(self.type_location, 'units.json'),
            self.source_dir,
            self.export_macro,
            self.print_files,
            create_subdir=False,
            use_alternate_names=True,
            unit_type=generators.embedded.unit.UnitEmbedded
        )

        self.generate_fill_dict()

        # generate the header files for the unit system library
        generators.embedded.specials.create_headers(
            self.fill_dict,
            self.source_dir,
            create_subdir=False
        )

    def generate_system(self):

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(self.target_dir, 'library.properties.template'),
            {'version': self.version},
            os.path.join(self.base_dir, 'library.properties')
        )

        # copy the .github folder
        generators.utils.copy_folder_to(self.target_dir, self.base_dir, '.github')

        # copy the examples folder
        generators.utils.copy_folder_to(self.target_dir, self.base_dir, 'examples')

        # copy the README.md file
        generators.utils.copy_file_to(self.template_dir, self.base_dir, 'README.md')

        # copy the LICENSE file
        generators.utils.copy_file_to(self.template_dir, self.base_dir, 'LICENSE')

    def generate(self):
        self.generate_sources()
        self.generate_system()
