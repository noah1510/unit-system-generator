# loads the contents of a file at the given filepath as a string
import distutils.dir_util
import distutils.file_util
import json
import os
from pathlib import Path
from typing import Dict, List

import jinja2
import generators.combination


# copies a file from the given input location to the given output folder
# if no filename is given, the input_location is assumed to be a file
# and the filename is taken from that
# if a filename is given, the input_location is assumed to be a folder
def copy_file_to(input_location: Path, output_folder: Path, filename: str = ''):
    if filename == '':
        filename = input_location.name
    else:
        input_location = input_location / filename

    input_location = input_location.expanduser()
    if not input_location.exists():
        raise FileNotFoundError(f'File {input_location} does not exist')

    output_location = output_folder / filename
    distutils.file_util.copy_file(str(input_location), str(output_location))


# copies a folder from the given input location to the given output folder
# if a folder_name is given, a folder_name with folder_name from the input_location is copied
def copy_folder_to(input_location: Path, output_path: Path, folder_name: str = ''):
    if folder_name == '':
        if not input_location.is_dir():
            raise ValueError('input_location must be a folder if no folder_name is given')
        folder_name = input_location.name
    else:
        input_location = input_location / folder_name
        if input_location.exists() and not input_location.is_dir():
            raise ValueError('input_location/folder_name must be a folder')

    input_location = input_location.expanduser()
    output_location = output_path / folder_name
    distutils.dir_util.copy_tree(str(input_location), str(output_location))


def fill_from_files(
        type_location: Path,
        export_macro: str,
        unit_strings: List[str],
) -> Dict:

    # load the 'combinations.json' file and parse its contents as a JSON string
    combinations = generators.combination.load_all_combinations(type_location / 'combinations.json')

    # load the 'constants.json' file and parse its contents as a JSON string
    json_string = load_file_to_string(type_location / 'constants.json')
    constants = [constant for constant in json.loads(json_string)]

    # create a dictionary containing the values that will be used to generate the header files
    fill_dict = {
        'export_macro': export_macro,
        'units': unit_strings,
        'combinations': combinations,
        'constants': constants,
    }

    return fill_dict


def load_file_to_string(filepath: Path) -> str:
    # open the file for reading
    template_file = open(filepath, "r")
    # read the contents of the file
    template_string = template_file.read()
    # close the file
    template_file.close()

    # return the file contents as a string
    return template_string


# fills a template string with the given values
def fill_template_string(template_str: str, values: Dict) -> str:
    # create a jinja2 template from the given string
    template = jinja2.Template(template_str)
    # render the template with the given values and return the result
    return template.render(values)


# fills a template file at the given filepath with the given values
def fill_template_file(filepath: Path, values: Dict) -> str:
    # load the template file as a string
    template_str = load_file_to_string(filepath)
    # fill the template string with the given values and return the result
    return fill_template_string(template_str, values)


# writes the given string to a file at the given filepath
def write_str_to_file(data_str: str, outfile: Path):
    # ensure the output directory exists
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    # open the file for writing
    source_file = open(outfile, "w")
    # write the data string to the file
    source_file.write(data_str)
    # close the file
    source_file.close()


# fills a template file at the given filepath with the given values and writes the result to the output file
def fill_template(infile: Path, values: Dict, outfile: Path):
    # fill the template file with the given values
    filled_template = fill_template_file(infile, values)
    # write the filled template to the output file
    write_str_to_file(filled_template, outfile)


class Prefix:
    def __init__(self):
        self.prefix = ''

    @staticmethod
    def from_string(data: str) -> (float, str):
        if '^' in data:
            name, exponent = data.split('^')
        else:
            name = data
            exponent = 1

        try:
            exponent = int(exponent)
            amount, prefix = Prefix.direct_prefix_string(name)
        except ValueError:
            raise ValueError('Invalid prefix string: ' + data)

        return amount ** exponent, prefix

    @staticmethod
    def direct_prefix_string(raw_str: str) -> (float, str):
        if raw_str == 'quetta':
            return Prefix.quetta()
        elif raw_str == 'ronna':
            return Prefix.ronna()
        elif raw_str == 'yotta':
            return Prefix.yotta()
        elif raw_str == 'zetta':
            return Prefix.zetta()
        elif raw_str == 'exa':
            return Prefix.exa()
        elif raw_str == 'peta':
            return Prefix.peta()
        elif raw_str == 'tera':
            return Prefix.tera()
        elif raw_str == 'giga':
            return Prefix.giga()
        elif raw_str == 'mega':
            return Prefix.mega()
        elif raw_str == 'kilo':
            return Prefix.kilo()
        elif raw_str == 'hecto':
            return Prefix.hecto()
        elif raw_str == 'deca':
            return Prefix.deca()
        elif raw_str == 'deci':
            return Prefix.deci()
        elif raw_str == 'centi':
            return Prefix.centi()
        elif raw_str == 'milli':
            return Prefix.milli()
        elif raw_str == 'micro':
            return Prefix.micro()
        elif raw_str == 'nano':
            return Prefix.nano()
        elif raw_str == 'pico':
            return Prefix.pico()
        elif raw_str == 'femto':
            return Prefix.femto()
        elif raw_str == 'atto':
            return Prefix.atto()
        elif raw_str == 'zepto':
            return Prefix.zepto()
        elif raw_str == 'yocto':
            return Prefix.yocto()
        elif raw_str == 'ronto':
            return Prefix.ronto()
        elif raw_str == 'quecto':
            return Prefix.quecto()
        else:
            raise ValueError('Invalid prefix string: ' + raw_str)

    @staticmethod
    def quetta() -> (float, str):
        return 1e30, 'Q'

    @staticmethod
    def ronna() -> (float, str):
        return 1e27, 'R'

    @staticmethod
    def yotta() -> (float, str):
        return 1e24, 'Y'

    @staticmethod
    def zetta() -> (float, str):
        return 1e21, 'Z'

    @staticmethod
    def exa() -> (float, str):
        return 1e18, 'E'

    @staticmethod
    def peta() -> (float, str):
        return 1e15, 'P'

    @staticmethod
    def tera() -> (float, str):
        return 1e12, 'T'

    @staticmethod
    def giga() -> (float, str):
        return 1e9, 'G'

    @staticmethod
    def mega() -> (float, str):
        return 1e6, 'M'

    @staticmethod
    def kilo() -> (float, str):
        return 1e3, 'k'

    @staticmethod
    def hecto() -> (float, str):
        return 1e2, 'h'

    @staticmethod
    def deca() -> (float, str):
        return 1e1, 'da'
    @staticmethod
    def deci() -> (float, str):
        return 1e-1, 'd'

    @staticmethod
    def centi() -> (float, str):
        return 1e-2, 'c'

    @staticmethod
    def milli() -> (float, str):
        return 1e-3, 'm'

    @staticmethod
    def micro() -> (float, str):
        return 1e-6, 'u'

    @staticmethod
    def nano() -> (float, str):
        return 1e-9, 'n'

    @staticmethod
    def pico() -> (float, str):
        return 1e-12, 'p'

    @staticmethod
    def femto() -> (float, str):
        return 1e-15, 'f'

    @staticmethod
    def atto() -> (float, str):
        return 1e-18, 'a'

    @staticmethod
    def zepto() -> (float, str):
        return 1e-21, 'z'

    @staticmethod
    def yocto() -> (float, str):
        return 1e-24, 'y'

    @staticmethod
    def ronto() -> (float, str):
        return 1e-27, 'r'

    @staticmethod
    def quecto() -> (float, str):
        return 1e-30, 'q'
