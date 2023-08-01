import unittest
from unit_system.units import length, area
from unit_system.prefixes import Prefix


class TestLength(unittest.TestCase):
    def test_length_prefix(self):
        self.assertAlmostEqual(float(length(5, Prefix.milli())), 0.005)
        self.assertAlmostEqual(float(length(5, Prefix.from_string('milli'))), 0.005)
        self.assertAlmostEqual(float(length(5, Prefix.from_string('centi^2'))), 0.0005)

    def test_length_square(self):
        l1 = length(5, Prefix.milli())
        a1 = l1.square()
        self.assertAlmostEqual(a1.cast_to_values().value, 0.000025)
        self.assertAlmostEqual(float(a1), float(l1 * l1))
        self.assertAlmostEqual(float(a1.sqrt()), float(l1))

    def test_unit_type(self):
        l1 = length(5, Prefix.milli())
        a1 = area(5, Prefix.milli())
        self.assertRaises(TypeError, lambda: l1 + a1)
        self.assertRaises(TypeError, lambda: l1 - a1)
        self.assertRaises(TypeError, lambda: l1 + 5)
        self.assertRaises(TypeError, lambda: l1 - 5)


if __name__ == '__main__':
    unittest.main()
