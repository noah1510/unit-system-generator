# Generator target specification

This file contains all the requirements a generator target has to fulfill.
The premise of this project is to prevent accidental mistakes when using units in code.
Because of this not every language is suitable as a target for this project.

## Language requirements

For reference look into the C++17 implementation.
Since it supports all features it is the reference implementation.

### langauge feature list

The following requirements have to be fulfilled for a target to be accepted:

* Support for data structures (classes, structs, etc.)
* Preventing implicit conversions (e.g. assign a speed to a length)
* Support for functions that act on the data structures (e.g. member functions)

Optional features that improve usage of the units:

* Support for operator overloading (e.g. `length1 + length2`)
* Support for user defined literals (e.g. `l1 = 1.0_m`)

### languages without overloading

Ideally the target language is object-oriented and supports (operator) overloading.
This allows for a more natural usage of the units.
While a C target is possible, it is not recommended due to the lack of proper classes which makes the usage of units look like the following:

```c
length l1 = length_create(1.0, meter);
time_si t1 = time_si_create(1.0, second);
speed s1 = length_divide(l1, t1);
```

This is not very readable and the usage of the units is not obvious.
A lot of languages are going to have the same problem as C.
If that is the case for the language you want to use, please reconsider if you really need to use units in that language.

### languages without operator overloading

If a langauge does not support operator overloading but supports function overloading the code can be improved a lot.
Go and java are good examples for this.
The usage of units in Go looks like the following:

```go
l1 := length{1.0, meter}
t1 := time_si{1.0, second}

s1 := l1.divide(t1)
t2 := s1.divide(length{2.0, meter})
```

Since the same function name can be used for different types the usage is a lot more natural.
It is still worse than operator overloading, but it is still a lot better than C.
(Small side note Go does not support classes but structs that can mostly be used like classes.)

### languages with dynamic typing

Languages with dynamic types require the programmer to do more work to ensure that the correct units are passed to the function.
Python is a good example for this.
While python has type hints they are not enforced by the interpreter.
This means each function has to check if the correct units were passed.
An example of this is shown below:

```python
from unit_system_py import length, speed, time

def some_calculation(l1: length, t1: time) -> speed:
    # check if the correct units were passed
    if not l1.isinstance(length) or not t1.isinstance(time):
        raise TypeError("Wrong unit passed to function")
    
    # do the calculation
    return l1 / t1
```

As you can see the code is more readable than the C code but the programmer has to do more work to ensure that the correct units are passed to the function.
This is not ideal, but it is the best that can be done in python.
In general a strict type system is more suited as a target language than a dynamic type system.
C++, Rust and many more languages to not need these checks since the compiler will do them for you.
This simplifies the code even further.

### language with all features

One example of a langauge that supports all features is C++.
Below is a small example of how the units can be used in C++:

```cpp
time some_calculation(length l1 = 1.0_m, time_si t1 = 1.0_s) {
    auto s1 = l1 / t1;
    auto t2 = s1 / 2.0_m;
    return t2;
}
```

As you can see the code looks more or less like the formula would look like if written by hand.
This is the ideal case and the goal of this project.
Because of the strong type system the compiler will ensure that the correct units are passed to the function.
This means the programmer does not have to do any checks to ensure that the correct units are passed to the function.
The literals allow for a more natural creation of variables.

### Note on using a base class and inheriting the units

In earlier versions of this project the units were inherited from a base class.
This required extra workarounds and made the code slower that it had to be.
While some language might be able to use this approach it is not recommended.
In most cases it is better to generate a new class for each unit.
This (mostly) prevents casting one unit to another and thus prevents accidental mistakes.
***Unless it is not possible to implement it without a common base class, such implementations are not accepted upstream.***

## Implementation requirements

The following requirements have to be fulfilled for a target to be accepted:

Unit classes:

* prevent conversions from one unit to another
* have correctly working multiplier and offset
* have working comparisons
* have working arithmetic operations (add,subtract with same; multiply, divide with scalar; divide with same is scalar)
* have working integration with IO
* have a way to create a unit from a number and a literal
* have a way to create a unit from a value, multiplier and offset
* have a way to create a unit from a value and a multiplier
* have a way to create a unit from a value
* implement combinations of units (e.g. `length * length` return `area`)

If something is missing in this list it might be added later.

## Adding a new language

Before you add a new target please open an issue to discuss the target.
This is to prevent duplicate work and to ensure that the target is suitable for this project.
In that issue share your ideas on how to implement the target and what problems you might encounter.

### Overview of the process

Implementing a target consists of the following steps:

* Implement the unit class as jinja2 template
* Create the rest of the library tooling (e.g. cmake files) if needed as jinja2 templates
* Create the target json file
* Add your target to the documentation
* Add CI files including the tests for your target

### Creating the unit class and library tooling

Each target has its own folder in the `target_data` folder.
In there are folders for each language.
The langauge folders contain a `generic` and a `per_unit` folder.
In addition to that there are folders for each toolchain that has an implementation in this langauge.

* The `generic` folder contains the jinja2 templates that apply to all toolchains or are the bases for the toolchain specific templates.
* The `per_unit` folder contains the jinja2 templates that are specific to each unit. These are applied on every unit and only get all the data fields of the unit as input.
* The toolchain folders contains the data for each toolchain target.
You can write jinja2 templates that inherit the generic templates and overwrite specific parts of them.

All files with the `.template` extension are jinja2 templates and will be rendered during the generation process.
The output file will be the same as the input file but without the `.template` extension.
If you want to specify a template file that should not be copied to the output folder you can use the `.template_local` extension for the file.
These can be inherited but don't produce a file in the output folder.

All other files will simply be copied to the output folder.

### Format of the target json file

Each toolchain needs its own target json file.
These go in the `generator_code/targets` folder.
The file name has to be the same as the toolchain folder name.

#### Target json file format:

* `name` (String): The name of the target. This has to be the same as the toolchain folder name.
* `group` (String): The language folder name of the target. This is used to create a group target to generate all targets of a language.
* `help` (String): A short description of the target that is displayed in the help message.
* `extra_data` (Object): language or target specific extra data that is passed to the jinja2 templates.
* `per_unit_templates` (Array of template expansions): A list of template expansions that are applied to each unit and which files they produce.
* `data_override` (data override Object): A dictionary that overrides the data of the unit. This is used to modify the data to work around langauge specific problems.
* `formatter` (formatter object): A dictionary that specifies the code formatter to use for the target and its arguments.
* `post_gen_commands` (Array of command objects): A list of commands that are executed after the generation process.
* `test_commands` (Array of command objects): A list of commands that are executed to run the tests for the target.

#### Template expansion format:

* `filename` (String): The name of the template file. It needs to be in the `per_unit` folder.
* `output_location` (String): The location of the output file. This is relative to the output folder.
* `file_pattern` (String): The pattern that is used to generate the file name. This is a jinja2 template that gets the unit data as input.

Here is the data of the arduino target as an example:

```json
{
  "filename": "unit.cpp.template",
  "output_location": "src/units",
  "output_pattern": "{unit[name]}.cpp"
}
```
This expands the `unit.cpp.template` file in the `per_unit` folder to the `src/units/{unit[name]}.cpp` file.
`{unit[name]}.cpp` will expand to the name of the unit with the `.cpp` extension.
For example this will result in `src/units/length.cpp` for the length unit.

#### Data override format:

* `rename_unit` (Object): A dictionary that renames units. The key is the old name and the value is the new name.
* `literals` (Object): A dictionary that specifies the literals for each unit.
The key is the unit name and the value is a dictionary that specifies the literals for that unit.
The key is the literal name and the value is a dictionary that specifies the code literal for that literal.

**NOTE: rename is applied before the literals are applied. Make sure to use the changed unit names when overriding literals.**

This is the data of the arduino target as an example:

```json
{
  "rename_unit": {
    "time": "time_si"
  },
  "literals": {
    "time_si": {
      "minute": {
        "code_literal": "minute"
      }
    },
    "force": {
      "Newton": {
        "code_literal": "Newton"
      }
    },
    "temperature": {
      "Celsius": {
        "code_literal": "Celsius"
      }
    }
  }
}
```

Here the time unit is renamed to `time_si` and the literals for the time, force and temperature units are specified.
They change the code literals from `_N` to `Newton`, `_C` to `Celsius` and `_min` to `minute`.
This works around some globally defined macros.
Python uses this to rename `as` to `as_` since `as` is a keyword in python.

#### Formatter format:

* `name` (String): The name of the formatter. This is the program name used to run the formatter in the command line.
* `args` (Array of Strings): The arguments that are passed to the formatter.
* `file_patterns` (Array of Strings): The patterns that are used to find the files that should be formatted. They are regex by default.

This is the formatter of the arduino target as an example.

```json
{
    "name": "clang-format",
    "args": ["-i"],
    "file_patters": [
      "src/unit_system.hpp",
      "src/units/*.cpp"
    ]
}
```

Here `clang-format` is used to format the files.
Because of the `-i` argument the files are formatted in place.
All files in the `src/units` folder with the `.cpp` extension and the `src/unit_system.hpp` file are formatted.

#### Command format:

* `command` (Array of Strings): The command that is executed. The first element is the program name and the rest are the arguments.
* `environment` (Object): A dictionary that specifies the environment variables that are set for the command.

This is the meson setup command as an example:

```json
{
    "command":[
        "meson",
        "setup",
        "build",
        "--wipe"
    ],
    "environment": {
        "colorize_console": "1"
    }
}
```

Here the `meson setup build --wipe` command is executed.
The `colorize_console` environment variable is set to `1` for the command.

### Writing a CI file

For more information on how to write the CI and test file look into the `Ci_and_tests.md` file in the `docs` folder.
