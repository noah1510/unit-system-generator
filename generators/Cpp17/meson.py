import os

import generators.utils
import generators.target
import generators.unit
import generators.Cpp17.unit
import generators.Cpp17.specials


class MesonConfig(generators.target.Target):
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
            enable_export_macro=True,
            target_name='meson',
            script_dir=os.path.realpath(os.path.dirname(__file__))
        )

    def generate_sources(self):
        self.units, self.unit_strings = generators.unit.units_from_file(
            os.path.join(self.type_location, 'units.json'),
            self.base_dir,
            self.export_macro,
            self.print_files,
            unit_type=generators.Cpp17.unit.UnitCpp17
        )

        self.generate_fill_dict()

        # generate the header files for the unit system library
        generators.Cpp17.specials.create_headers(
            self.fill_dict,
            self.base_dir
        )

    def generate_system(self):

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(self.target_dir, 'meson.build.template'),
            {
                'version': self.version,
                'export_macro': self.export_macro,
                'units': self.unit_strings,
            },
            os.path.join(self.base_dir, 'meson.build')
        )

        # copy the meson options file
        generators.utils.copy_file_to(self.target_dir, self.target_dir, 'meson_options.txt')

        # copy the tests
        generators.utils.copy_folder_to(self.target_dir, self.base_dir, 'tests')

        # copy the subprojects folder
        generators.utils.copy_folder_to(self.target_dir, self.base_dir, 'subprojects')

        # copy the README.md file
        generators.utils.copy_file_to(self.template_dir, self.base_dir, 'README.md')

        # copy the LICENSE file
        generators.utils.copy_file_to(self.template_dir, self.base_dir, 'LICENSE')
