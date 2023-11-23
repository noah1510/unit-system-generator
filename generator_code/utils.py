# loads the contents of a file at the given filepath as a string
import shutil
import json
import os
import subprocess
from pathlib import Path
from typing import Dict

import jinja2


# A lightweight class for loading and writing files
# It supports copying files and directories to other locations, and reading and writing files as strings.
class File:
    def __init__(self, path):
        self.path = Path(path)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return repr(self.path)

    def get(self):
        return self.path

    # reads the contents of this file and returns them as a string
    def read_string(self) -> str:
        if not self.get().exists():
            raise FileNotFoundError(f'File {self} does not exist')

        # open the file for reading
        read_file = open(self.get(), "r")
        # read the contents of the file
        file_data = read_file.read()
        # close the file
        read_file.close()

        # return the file contents as a string
        return file_data

    # writes the given string to this file
    def write_string(self, output_data: str):
        # ensure the output directory exists
        if not self.get().parent.exists():
            os.makedirs(self.get().parent, exist_ok=True)

        # open the file for writing
        source_file = open(self.get(), "w")
        # write the data string to the file
        source_file.write(output_data)
        # close the file
        source_file.close()

    # copies this file to the given output folder
    # if copy_as_subfile is True, the file will be copied to the output folder as a subfile
    # otherwise, the file will be copied to the output folder as a file with the same name
    # If this file is a directory, it will be copied recursively to the output folder.
    # If the output folder does not exist, it will be created.
    def copy(
            self,
            output_folder: Path,
            copy_as_subfile: bool = True,
    ) -> 'File':
        if copy_as_subfile:
            output_folder = output_folder / self.get().name

        if not output_folder.parent.exists():
            os.makedirs(output_folder.parent, exist_ok=True)

        if self.get().is_file():
            shutil.copy(str(self), str(output_folder))
        else:
            shutil.copytree(str(self), str(output_folder))

        return File(output_folder)

    def read_json(self) -> Dict:
        return json.loads(self.read_string())

    def clean(self):
        if self.get().exists():
            if self.get().is_file():
                self.get().unlink()
            else:
                shutil.rmtree(str(self.get()))


# A class to represent a template file or directory
# It handles filling the template with the given values and writing the output to the output file
class Template:
    def __init__(
            self,
            template_file: Path,
            output_file: Path,
            extra_infos: Dict = None,
            group_path: Path = None,
    ):

        if extra_infos is None:
            extra_infos = {}

        self.template_file = File(template_file)
        self.output_file = File(output_file)
        self.extra_infos = extra_infos
        self.group_path = group_path

    # Fill the template file with the given values and write the output to the output file
    # If the input is a directory, it will be copied recursively to the output folder and each file with a .template
    # extension will be filled with the given values and written to the output folder without the .template extension.
    def fill_with(self, values: Dict):
        if self.template_file.get().is_file():
            if self.template_file.get().suffix != '.template':
                if self.template_file.get().suffix != '.template_local':
                    self.template_file.copy(self.output_file.get(), copy_as_subfile=False)
                return

            try:
                # load the template file as a string
                template_str = self.template_file.read_string()

                # load the template string into a jinja2 template
                if self.group_path is None:
                    template = jinja2.Environment(
                        loader=jinja2.FileSystemLoader(self.template_file.get().parent)
                    ).from_string(template_str)
                else:
                    template = jinja2.Environment(
                        loader=jinja2.FileSystemLoader(self.group_path)
                    ).from_string(template_str)

                # fill the template with the given values
                filled_template = template.render(values)

                # write the filled template to the output file
                self.output_file.write_string(filled_template)
            except Exception as e:
                raise ValueError(f'Error filling template {self.template_file} with values {values}') from e

        elif self.template_file.get().is_dir():
            self.output_file.get().mkdir(exist_ok=True, parents=True)
            if not self.output_file.get().is_dir():
                raise ValueError(f'Output file {self.output_file} is not a directory')

            # get a list of all files in the template directory
            files = [File(file) for file in os.listdir(self.template_file.get())]

            # recursively fill each file in the template directory
            # If the name of the file ends with '.template', the output file will have the same name without the
            # '.template' extension. Otherwise, the output file will have the same name as the input file.
            for file in files:
                infile = self.template_file.get() / file.get().name
                outfile = self.output_file.get() / file.get().name
                if outfile.suffix == '.template':
                    outfile = outfile.with_suffix('')

                Template(
                    infile,
                    outfile,
                    extra_infos=self.extra_infos,
                    group_path=self.group_path,
                ).fill_with(values)


# A class to represent a subprocess command for easier use
class Command:
    def __init__(self, command_dict: Dict):
        self.env = command_dict.get('environment', {})
        self.cmd = command_dict.get("command", "")
        self.wasExecuted = False
        self.output: subprocess.CompletedProcess = None

    def run(self, cwd: Path = None):
        if cwd is None:
            cwd = Path.cwd()

        env = os.environ.copy()
        env.update(self.env)
        self.output = subprocess.run(
            self.cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
        )
        self.wasExecuted = True

    def print_output(self):
        if self.wasExecuted:
            print(self.output.stdout)
        else:
            raise RuntimeError('Command was not executed')

    def print_info(self):
        print('command: ', self.cmd)
        print('env extras: ' + str(self.env))

    def check_returncode(self):
        if self.wasExecuted:
            self.output.check_returncode()
        else:
            raise RuntimeError('Command was not executed')
