# loads the contents of a file at the given filepath as a string
import os
from typing import Dict

import jinja2


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


