from math import pi
from unittest import TestCase, TestSuite, makeSuite

from pycalc.tokentypes.tokens import Function
from pycalc.interpreter.interpret import Interpreter


interpreter = Interpreter()
basic_namespace = {
    "pi": pi,
    "rt": lambda a, b: a ** (1/b)
}

evaluate = lambda code: interpreter.interpret(code, basic_namespace)


class TestNumbers(TestCase):
    def test_integer(self):
        self.assertEqual(evaluate("100"), 100)

    def test_float(self):
        self.assertEqual(evaluate("0.1"), 0.1)
        self.assertEqual(evaluate(".1"), 0.1)


class TestBasicOperations(TestCase):
    def test_addition(self):
        self.assertEqual(evaluate("1+1"), 2)

    def test_subtraction(self):
        self.assertEqual(evaluate("1-1"), 0)

    def test_multiplication(self):
        self.assertEqual(evaluate("1*1"), 1)

    def test_division(self):
        self.assertEqual(evaluate("1/2"), .5)

    def test_floordivision(self):
        self.assertEqual(evaluate("3//2"), 1)

    def test_modulo(self):
        self.assertEqual(evaluate("7%2"), 1)

    def test_lshift(self):
        self.assertEqual(evaluate("1<<5"), 32)

    def test_rshift(self):
        self.assertEqual(evaluate("128>>5"), 4)

    def test_bitwise_and(self):
        self.assertEqual(evaluate("32 & 64"), 0)

    def test_bitwise_or(self):
        self.assertEqual(evaluate("81 | 82"), 83)

    def test_bitwise_xor(self):
        self.assertEqual(evaluate("54^87"), 97)

    def test_exponentiation(self):
        self.assertEqual(evaluate("2**3"), 8)

    def test_unary_addition(self):
        self.assertEqual(evaluate("+1"), 1)

    def test_unary_subtraction(self):
        self.assertEqual(evaluate("-1"), -1)

    def test_unary_subtraction_multiple(self):
        self.assertEqual(evaluate("--1"), 1)
        self.assertEqual(evaluate("---1"), -1)

    def test_equality(self):
        self.assertEqual(evaluate("2==2"), 1)
        self.assertEqual(evaluate("2!=2"), 0)


class TestOperatorsPriority(TestCase):
    def test_addition_multiplication(self):
        self.assertEqual(evaluate("2+2*2"), 6)

    def test_addition_division(self):
        self.assertEqual(evaluate("2+2/2"), 3)

    def test_addition_exponentiation(self):
        self.assertEqual(evaluate("1+2**3"), 9)

    def test_subtraction_addition(self):
        self.assertEqual(evaluate("1-2+3"), 2)

    def test_subtraction_subtraction(self):
        self.assertEqual(evaluate("1-2-3"), -4)

    def test_subtraction_multiplication(self):
        self.assertEqual(evaluate("2-2*2"), -2)

    def test_subtraction_division(self):
        self.assertEqual(evaluate("2-2/2"), 1)

    def test_subtraction_exponentiation(self):
        self.assertEqual(evaluate("1-2**3"), -7)

    def test_multiplicaion_exponentiation(self):
        self.assertEqual(evaluate("2*10**2"), 200)

    def test_division_exponentiation(self):
        self.assertEqual(evaluate("1/10**2"), 0.01)

    def test_exponentiation_right_associativity(self):
        self.assertEqual(evaluate("2**3**2"), 512)

    def test_exponentiation_unary_subtraction(self):
        self.assertEqual(evaluate("2**-3"), 0.125)

    def test_unary_subtraction_exponentiation(self):
        self.assertEqual(evaluate("-2**2"), -4)


class TestVariables(TestCase):
    def test_get_pi(self):
        self.assertEqual(evaluate("pi"), pi)

    def test_negotate_pi(self):
        self.assertEqual(evaluate("-pi"), -pi)

    def test_expression_with_constant(self):
        self.assertEqual(evaluate("pi+2.0-3"), pi + 2 - 3)
        self.assertEqual(evaluate("2.0+pi-3"), 2 + pi - 3)
        self.assertEqual(evaluate("2.0-3+pi"), 2 - 3 + pi)

    def test_declare_var(self):
        self.assertEqual(evaluate("a=5+5"), 10)

    def test_get_declared_var(self):
        self.assertEqual(evaluate("a"), 10)


class TestFunctions(TestCase):
    def test_funccall(self):
        self.assertEqual(evaluate("rt(25, 2)"), 5)

    def test_nested_funccall(self):
        self.assertEqual(evaluate("rt(rt(625, 2), 2)"), 5)

    def test_expr_in_funccall(self):
        self.assertEqual(evaluate("rt(20+5, 1.0+1.0)"), 5)

    def test_funcdef(self):
        self.assertIsInstance(evaluate("f(x,y)=x*y"), Function)

    def test_def_func_call(self):
        evaluate("f(x,y)=x*y")
        self.assertEqual(evaluate("f(2,5)"), 10)

    def test_def_func_argexpr(self):
        evaluate("f(x,y)=x*y")
        self.assertEqual(evaluate("f(2+5, 3*2)"), 42)


evaluation_tests = TestSuite()
evaluation_tests.addTest(makeSuite(TestNumbers))
evaluation_tests.addTest(makeSuite(TestBasicOperations))
evaluation_tests.addTest(makeSuite(TestOperatorsPriority))
evaluation_tests.addTest(makeSuite(TestVariables))
evaluation_tests.addTest(makeSuite(TestFunctions))
