# unit-system-generator

[![GitHub license](https://img.shields.io/github/license/noah1510/unit-system-generator.svg)](https://github.com/noah1510/unit-system-generator/blob/master/License)
[![stable release](https://img.shields.io/github/v/release/noah1510/unit-system-generator.svg)](https://GitHub.com/noah1510/unit-system-generator/releases/)
[![arduino-library-badge](https://www.ardu-badge.com/badge/unit-system.svg?)](https://www.ardu-badge.com/unit-system)

**This repository contains the code generator for the unit system.**
**If you want to use the unit system in your project use the generated code for that.**
**[meson sources](https://github.com/noah1510/unit-system), [arduino sources](https://github.com/noah1510/unit-system-adruino)**

## What is this?

This is an implementation of the SI unit system for software development.
All units, combinations, literals and constants are generated from templates.
If you feel like anything is missing just add it to the build system and open a pull request.

Although this library is focused on SI units it can be used to work with imperial units, but there will ***NEVER*** be upstream support for it.
If you want to use imperial units you can figure out how to convert and add literals by yourself.

## Notes on current targets

### meson C++17 (default)

The C++ target C++17 by default, but it can be changed to C++14 or C++20 if needed.
C++11 might work but is not tested and recommended.
Changing the C++ version is done by the build system, so there is no option in the code generator.

### Arduino C++

Arduino has its own code generator, because of annoying limitations of the arduino IDE and board implementations.
The Arduino code has fewer features and no support for the C++ standard library.
Also use the `UNIT_SYSTEM_ABS` macro instead of `abs` to get the absolute value of a unit.
Abs usually compares with 0 but that is not possible for units which is why the macro is needed.

## Usage examples

```c++
#include "unit_system.hpp"
#include <iostream>

using namespace sakurajin::unit_system;
using namespace sakurajin::unit_system::literals;

int main(){
    const auto t2 = 10.0_h;
    const auto s2 = 250.0_km;
    
    std::cout << s2 << " driven in " << t2 << " is an average speed of:" << s2/t2 << std::endl;
}

```

## Units that are currently supported

* unit_t -> a unit template that is the basis of all the units
* time_si -> time with seconds as base unit
* length -> length with meter as base unit
* mass -> mass with kg as base unit
* temperature -> temperature with K as base unit
* amount -> amount of substance with mole as base unit
* electric_current -> electric current with Ampere as base unit
* luminous_intensity -> luminous intensity with candela as base unit
* area -> area with `m^2` as base unit
* speed -> speed with `m / s` as base unit
* acceleration -> acceleration with `m / s^2` as base unit
* momentum -> momentum with `kg * m / s` as base unit
* force -> force with `kg * m / s^2` (Newton) as base unit
* energy -> energy with `kg * m^2 / s^2` (Joules) as base unit
* power -> power with `kg * m^2 / s^3` (Watts) as base unit

## Using the code generator

All you need for the code generator is python3.
The code generator is written in python3 and uses the jinja2 template engine to generate the code.
To install the dependencies run `pip3 install -r requirements.txt` in the root directory of this repository.

After the dependencies are installed you can run the code generator with `python3 ./genSources.py`.
The script takes the following arguments:

* `-o` or `--outDir` -> the output directory for the generated code. Default is `./output`
* `--arduino` -> generate code for arduino instead of meson
* `--printOutFiles` -> print which files are generated to stdout

## Adding new units

To add new units all you need to do is change the json files in the `type data` directory and rerun the code generator.
There are three json files:

* `units.json` -> contains all the units, their names and literals
* `constants.json` -> contains all the constants and their values
* `combinations.json` -> contains all the combinations of units

Add the new units to the `units.json` file and also specify how they are combined in the `combinations.json` file.
The combination file is used to generate the operators for the units.
Each object in that array specifies two units and the resulting unit.
The way this is interpreted is `factor1 * factor2 = product`.
The code automatically generates the inverse of the product as well as different orders.

Each unit needs a unique id.
That id is needed to prevent converting one unit into another by accident.
If you want to see the naming convention for the ids look into the `unit_t.hpp` header file.

## Planned features

At the moment the only generated language is C++.
But there are plans to add support for other languages in the future (e.g. python).
For this to be useful or even work at all, the language must support operator overloading (e.g. not java).

Once build system support is the C++ code will get a C++20 module interface.
This will make it easier to use the unit system in your project.
At the moment however no build system supports C++20 modules properly.
