import typing

# forward declare all units to allow for circular dependencies of units
# This is mostly needed for combinations which require the usage of not yet defined units
#{% for unit in units %}
#{{ unit.name }} = typing.NewType("{{ unit.name }}", None)
#{% endfor %}

#{% for unit in units %}

#{% endfor %}

Speed = typing.NewType("Speed", None)


# A class representing the unit {{ unit.name }}.
class Speed:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = value
        self.multiplier = multiplier
        self.offset = offset

    def __str__(self):
        return f'{self.value} m/s'

    def __repr__(self):
        return f'Speed({self.value}, {self.multiplier}, {self.offset})'

    def __add__(self, other: 'Speed') -> 'Speed':
        other = other.cast_to_values(self.multiplier, self.offset)
        return Speed(self.value + other.value)

    def __sub__(self, other: 'Speed') -> 'Speed':
        other = other.cast_to_values(self.multiplier, self.offset)
        return Speed(self.value - other.value)

    def __truediv__(self, value: typing.Union[float, 'Speed']):
        if isinstance(value, float):
            return Speed(self.value / value)
        elif isinstance(value, Speed):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        else:
            raise TypeError(f'Cannot divide Speed by {type(value)}')

    def __mul__(self, value: typing.Union[
        float
    ]):
        if isinstance(value, float):
            return Speed(self.value * value)
        else:
            raise TypeError(f'Cannot multiply Speed by {type(value)}')

    def cast_to_other(self, other: 'Speed'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        return Speed(self.value * multiplier + offset)
    