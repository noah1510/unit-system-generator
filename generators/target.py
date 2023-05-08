import os
import generators.utils

# A class that represents a target for the code generator
# This class is used to generalize the code generator so that more targets can be added easily
# while still keeping the code clean and readable
class Target:
    def __init__(
            self,
            version: str,
            main_script_dir: os.path,
            base_dir: os.path,
            print_files: bool = False,
            enable_export_macro: bool = True,
            target_name: str = '',
            script_dir: os.path = os.path.realpath(os.path.dirname(__file__)),
    ):
        self.version = version
        self.target_name = target_name
        if enable_export_macro:
            self.export_macro = 'UNIT_SYSTEM_EXPORT_MACRO'
        else:
            self.export_macro = ''

        self.main_script_dir = main_script_dir
        self.base_dir = base_dir
        self.print_files = print_files

        self.target_dir = os.path.join(script_dir, self.target_name)
        self.template_dir = os.path.join(script_dir, 'templates')
        self.type_location = os.path.join(main_script_dir, 'type data')

        self.units = []
        self.unit_strings = []
        self.hasCombinations = True
        self.fill_dict = {}

    def generate_fill_dict(self):
        self.fill_dict = generators.utils.fill_from_files(
            self.type_location,
            self.export_macro,
            self.unit_strings
        )

        self.fill_dict['target'] = self.target_name
        return

    def generate_sources(self):
        return

    def generate_system(self):
        return

    def generate(self):
        self.generate_sources()
        self.generate_system()
