# loads the contents of a file at the given filepath as a string
import distutils.dir_util
import distutils.file_util
import json
import os
from typing import Dict, List

import jinja2


# copies a file from the given input location to the given output folder
# if no filename is given, the input_location is assumed to be a file
# and the filename is taken from that
# if a filename is given, the input_location is assumed to be a folder
def copy_file_to(input_location: os.path, output_folder: os.path, filename: str = ''):
    if filename == '':
        filename = os.path.basename(input_location)
    else:
        input_location = os.path.join(input_location, filename)

    output_location = os.path.join(output_folder, filename)
    distutils.file_util.copy_file(input_location, output_location)


# copies a folder from the given input location to the given output folder
# if a folder_name is given, a folder_name with folder_name from the input_location is copied
def copy_folder_to(input_location: os.path, output_path: os.path, folder_name: str = ''):
    if folder_name == '':
        folder_name = os.path.basename(input_location)
    else:
        input_location = os.path.join(input_location, folder_name)

    output_location = os.path.join(output_path, folder_name)
    distutils.dir_util.copy_tree(input_location, output_location)


def fill_from_files(
        type_location: os.path,
        export_macro: str,
        unit_strings: List[str],
) -> Dict:

    # load the 'combinations.json' file and parse its contents as a JSON string
    json_string = load_file_to_string(os.path.join(type_location, 'combinations.json'))
    combinations = [[comb['factor1'], comb['factor2'], comb['product']] for comb in json.loads(json_string)]

    # load the 'constants.json' file and parse its contents as a JSON string
    json_string = load_file_to_string(os.path.join(type_location, 'constants.json'))
    constants = [constant for constant in json.loads(json_string)]

    # create a dictionary containing the values that will be used to generate the header files
    fill_dict = {
        'export_macro': export_macro,
        'units': unit_strings,
        'combinations': combinations,
        'constants': constants,
    }

    return fill_dict


def load_file_to_string(filepath: os.path) -> str:
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
def fill_template_file(filepath: os.path, values: Dict) -> str:
    # load the template file as a string
    template_str = load_file_to_string(filepath)
    # fill the template string with the given values and return the result
    return fill_template_string(template_str, values)


# writes the given string to a file at the given filepath
def write_str_to_file(data_str: str, outfile: os.path):
    # ensure the output directory exists
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    # open the file for writing
    source_file = open(outfile, "w")
    # write the data string to the file
    source_file.write(data_str)
    # close the file
    source_file.close()


# fills a template file at the given filepath with the given values and writes the result to the output file
def fill_template(infile: os.path, values: Dict, outfile: os.path):
    # fill the template file with the given values
    filled_template = fill_template_file(infile, values)
    # write the filled template to the output file
    write_str_to_file(filled_template, outfile)


