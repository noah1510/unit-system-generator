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

Langauges with dynamic types require the programmer to do more work to ensure that the correct units are passed to the function.
Python is a good example for this.
While python has type hints they are not enforced by the interpreter.
This means each function has to check if the correct units were passed.
An example of this is shown below:

```python
def some_calculation(l1: length, t1: time_si) -> speed:
    # check if the correct units were passed
    if not l1.isinstance(length) or not t1.isinstance(time_si):
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

## Adding a new target

Before you add a new target please open an issue to discuss the target.
This is to prevent duplicate work and to ensure that the target is suitable for this project.
In that issue share your ideas on how to implement the target and what problems you might encounter.

Implementing a target consists of the following steps:

* Implement the unit class as jinja2 template
* Create the rest of the library tooling (e.g. cmake files) if needed as jinja2 templates
* Add your target to targets.py to actually generate the files
* Add your target to the documentation
* Add CI files including the tests for your target

Each target has its own folder in the `generator` folder.
Since some targets might share code it is recommended to create a subdir for the tooling while keeping the language specific files in the root of the target folder.

For more information on how to write the CI and test file look into the `Ci_and_tests.md` file in the `docs` folder.
