# Documentation of the type configuration formats

The configuration data is split into three files:

* `units.json` -> contains all units, their names and literals
* `combinations.json` -> contains information on how units can be combined and what the result is
* `constants.json` -> contains all constants and their values

## units.json

This file contains all the units and their names and literals.
Each unit has the following properties:

* `name` (required) -> the name of the unit
* `base_literal` (required) -> the literal that is used as the base unit
* `unit_id` (required) -> An Unique ID for the unit. This is used to prevent some languages from converting one unit into another by accident.
* `literals` (required) -> An array of all the literals of the unit
* `generated_multipliers` (optional) -> An object that contains all the generated multipliers for each literal

Each literal has the following properties:

* `name` (required) -> the name of the literal
* `multiplier` (required) -> the multiplier of the literal
* `code_literal` (required) -> the literal that is used in the code
* `udl_override` (optional) -> overrides the code literal to prevent duplication
* `code_alternative` (optional) -> the alternative code literal that is used in case the normal one does not work on a platform

The generated multipliers define which SI-prefixes are generated for each literal.
For example if the literal for second in s and milli should be generated as a prefix this creates a new literal called ms with the multiplier 0.001.

Below is the time_si unit as an example on how a unit might look like:

```json
{
    "name": "time_si",
    "base_literal": "second",
    "unit_id": 1,
    "literals": [
      {
        "name": "year",
        "code_literal":"a",
        "multiplier": 31536000000
      },
      {
        "name": "day",
        "code_literal": "d",
        "multiplier": 86400000
      },
      {
        "name": "hour",
        "code_literal": "h",
        "multiplier": 3600
      },
      {
        "name": "minute",
        "code_literal": "m",
        "udl_override": "minute",
        "multiplier": 60
      },
      {
        "name": "second",
        "code_literal": "s",
        "multiplier": 1e0
      }
    ],
    "generated_multipliers": {
      "second": [
        "milli",
        "micro",
        "nano",
        "pico",
        "femto",
        "atto"
      ]
    }
}
```

## combinations.json

This file contains the information on how the units can be combined and what the result is.
Each combination has the following properties:

* `factor1` (required) -> the first unit
* `factor2` (required) -> the second unit
* `result` (required) -> the result of the multiplication of the factors

Below is the combination of length and time as an example on how a combination might look like:

```json
{
    "factor1": "speed",
    "factor2": "time_si",
    "result": "length"
}
```

The generator will generate the following combinations:

* speed * time_si = length
* time_si * speed = length
* length / speed = time_si
* length / time_si = speed

Because of this only one multiplication has to be specified and all other variations still work in the code.
Due to language limitations it is only possible to have two factors and one result.
Combining more units can be done by combining multiple combinations.

If factor1 and factor2 are the same the generator will generate the following combinations:

* factor1 * factor2 = result
* square(factor1) = result
* sqrt(result) = factor1

This feature is required for units like area where the unit is the square of the base unit.

## constants.json

This file contains all the constants and their values.
Each constant has the following properties:

* `name` (required) -> the name of the constant
* `value` (required) -> the value of the constant

For now all constants can only be floats (no unit system units).
This may change in the future.

## Adding a new unit

To add a new units you have to first add the unit and its literals to the units.json file.
After that you need to specify the combinations that the unit can be used in.
Lastly if you need to add a constant you can add it to the constants.json file.
