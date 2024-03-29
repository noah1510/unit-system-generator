import unittest
from unit_system_py import literals


class TestLength(unittest.TestCase):
    def assertUnitEqual(self, u1, u2):
        self.assertEqual(type(u1), type(u2))
        self.assertAlmostEqual(float(u1), float(u2))

    def test_length_literals(self):
        # test if the prefix is correctly applied
        self.assertAlmostEqual(float(literals.mm(5)), 0.005)
        self.assertUnitEqual(literals.mm(5), literals.cm(0.5))

    def test_length_square(self):
        l1 = literals.mm(5)
        a1 = l1.square()
        a2 = literals.mm2(25)

        # test if squaring and square root works
        self.assertAlmostEqual(a1.cast_to_values().value, 0.000025)
        self.assertUnitEqual(a1, l1 * l1)
        self.assertUnitEqual(a1.sqrt(), l1)
        self.assertUnitEqual(a1, a2)

    def test_math_operator_type(self):
        l1 = literals.mm(5)
        a1 = literals.mm2(5000)

        # check that the type is checked in all math operations
        self.assertRaises(TypeError, lambda: l1 + a1)
        self.assertRaises(TypeError, lambda: l1 - a1)
        self.assertRaises(TypeError, lambda: l1 + 5)
        self.assertRaises(TypeError, lambda: l1 - 5)
        with self.assertRaises(TypeError):
            l1 += a1
        with self.assertRaises(TypeError):
            l1 -= a1
        with self.assertRaises(TypeError):
            l1 += 5
        with self.assertRaises(TypeError):
            l1 -= 5
        with self.assertRaises(TypeError):
            l1 *= a1
        with self.assertRaises(TypeError):
            l1 /= a1

    def test_math_operator_value(self):
        l1 = literals.mm(5)
        l2 = literals.um(5000)
        l3 = literals.mm(10)

        self.assertUnitEqual(l1, l2)
        self.assertUnitEqual(l1 + l2, l3)
        self.assertUnitEqual(l1 - l2, literals.m(0))
        self.assertUnitEqual(l1 * 2, l3)
        self.assertUnitEqual(l3 / 2, l2)
        self.assertUnitEqual(l1 * l2, l1.square())
        self.assertUnitEqual(l1 / l2, l2 / l1)
        self.assertUnitEqual(l1/l1, 1.0)

    def test_comparison_operators(self):
        v1 = literals.m(1000)
        v2 = literals.m(1)
        v3 = literals.km(1)
        v4 = literals.m2(1)
        v5 = literals.m(-1)

        # test if positive and negative values are compared correctly
        self.assertTrue(v2 < v3)
        self.assertTrue(v3 > v2)
        self.assertTrue(v2 <= v3)
        self.assertTrue(v3 >= v2)

        self.assertTrue(v5 < v2)
        self.assertTrue(v5 <= v2)
        self.assertTrue(v2 > v5)
        self.assertTrue(v2 >= v5)

        # try comparing different units
        self.assertRaises(TypeError, lambda: v1 < v4)
        self.assertRaises(TypeError, lambda: v1 > v4)
        self.assertRaises(TypeError, lambda: v1 <= v4)
        self.assertRaises(TypeError, lambda: v1 >= v4)

        # tray comparing with number
        self.assertRaises(TypeError, lambda: v1 < 1)
        self.assertRaises(TypeError, lambda: v1 > 1)
        self.assertRaises(TypeError, lambda: v1 <= 1)
        self.assertRaises(TypeError, lambda: v1 >= 1)

    def test_function_overloads(self):
        v1 = literals.m(1)
        v2 = literals.m(-1)

        # test if abs works
        self.assertUnitEqual(abs(v1), v1)
        self.assertUnitEqual(abs(v2), v1)

        # test if - works
        self.assertUnitEqual(-v1, v2)
        self.assertUnitEqual(-v2, v1)

        # test if + works
        self.assertUnitEqual(+v1, v1)
        self.assertUnitEqual(+v2, v2)


if __name__ == '__main__':
    unittest.main()
