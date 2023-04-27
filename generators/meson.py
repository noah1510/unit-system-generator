import os

import generators.utils
import distutils.file_util
import distutils.dir_util


class MesonConfig:
    def __init__(
            self,
            version: str,
            export_macro: str,
            units: list[str],
            has_combinations: bool,
    ):
        self.version = version
        self.export_macro = export_macro
        self.units = units
        self.hasCombinations = has_combinations

    def generate(self, out_dir: os.path, base_dir: os.path):
        script_dir = os.path.realpath(os.path.dirname(__file__))
        template_dir = os.path.join(script_dir, 'meson parts')

        if out_dir == '':
            out_dir = base_dir

        # Fill in the "meson.build.template" file with the data in `fill_dict`
        # and write the output to the "meson.build" file in the output directory.
        generators.utils.fill_template(
            os.path.join(template_dir, 'meson.build.template'),
            {
                'version': self.version,
                'export_macro': self.export_macro,
                'units': self.units,
                'hasCombinations': self.hasCombinations,
            },
            os.path.join(out_dir, 'meson.build')
        )

        # copy the meson options file
        meson_options = os.path.join(template_dir, 'meson_options.txt')
        distutils.file_util.copy_file(meson_options, os.path.join(out_dir, 'meson_options.txt'))

        # copy the tests
        tests_dir = os.path.join(template_dir, 'tests')
        distutils.dir_util.copy_tree(tests_dir, os.path.join(out_dir, 'tests'))

        # copy the subprojects folder
        subprojects_dir = os.path.join(template_dir, 'subprojects')
        distutils.dir_util.copy_tree(subprojects_dir, os.path.join(out_dir, 'subprojects'))

