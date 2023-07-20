# unit-system Desktop C++17

[![GitHub license](https://img.shields.io/github/license/noah1510/unit-system.svg)](https://github.com/noah1510/unit-system/blob/master/License)
[![stable release](https://img.shields.io/github/v/release/noah1510/unit-system.svg)](https://GitHub.com/noah1510/unit-system/releases/)

**As of version 0.6.0 all the source code is generated by python scripts.**
**This repository only contains the generated source files.**
**If you want to report a bug or change something check the [generator repository](https:://github.com/noah1510/unit-system-generator).**


This is an implementation of the SI unit system for C++17 development.
All units, combinations, literals and constants are generated from templates.
If you feel something is missing open an issue or a pull request on the [generator repository](https:://github.com/noah1510/unit-system-generator).

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

## Including the unit-system library

Depending on your build system you might have to figure out how to include and link this library by yourself.

### meson

unit-system is written in C++ with the meson build system.
Integrating this library is very easy.
Just use the wrapdb to download the version you need, and then you can add the library as a dependency object.

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

## Upgrade Instructions

### from version 0.6.x to 0.7.x

Nothing much changed in the API.
The most important change is that when using meson, the std is now required and the fallbacks are removed.
This means that you have to use a compiler that supports C++14 or higher.
In addition to that the generator repository and the unit-system repository are now split.
This means that python is no longer required to build the code.
The unit-system repository now only contains the generated code.

One other major change is that Arduino and C++17 have separate templates.
Because of this the Arduino API is slightly different but should work on almost every board.

###  from version pre 0.6.0 to 0.6.x

As of version 0.6.0 there are no longer sub namespaces for base and common units.
Just change `sakurajin::unit_system::base` and `sakurajin::unit_system::common` to `sakurajin::unit_system`.
This also affects literals and constants so they are now all under `sakurajin::unit_system::literals` and `sakurajin::unit_system::constants`.

In addition to that a lot of data was moved around in the headers.
Because of that it is no longer recommended to include only some parts of the library.
So instead of including the units directly just include the main header for this library `#include "unit_system.hpp"`.
