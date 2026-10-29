 

import inspect
import math


def exponentiation(base, exponent):
     
    return math.pow(base, exponent)


def square_root(number, _=None):
     
    if number < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(number)


def logarithm(number, base=math.e):
     
    if number <= 0:
        raise ValueError("Cannot calculate the logarithm of a non-positive number.")
    if base is not None:
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1.")
        return math.log(number, base)
    return math.log(number)


class Calculator:
     

    def __init__(self):
         
        self.operations = {}
        self.init()

    def init(self):
         
        self.operations = {
            '+': self._add,
            '-': self._subtract,
            '*': self._multiply,
            '/': self._divide,
        }

    @staticmethod
    def _add(a, b):
        return a + b

    @staticmethod
    def _subtract(a, b):
        return a - b

    @staticmethod
    def _multiply(a, b):
        return a * b

    @staticmethod
    def _divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    def add_operation(self, operation_symbol, operation_function):
         
        self.operations[operation_symbol] = operation_function

    def calculate(self, first_number, operation_symbol, second_number=None):
         
         
        if operation_symbol not in self.operations:
            error_message = (
                f"Error: Invalid operation symbol '{operation_symbol}'. "
                f"Available operations: {', '.join(self.operations.keys())}"
            )
            print(error_message)
            raise ValueError(error_message)

         
        if not isinstance(first_number, (int, float)) or isinstance(first_number, bool):
            error_message = (
                f"Error: Invalid input '{first_number}'. "
                f"The first input must be a valid number (int or float)."
            )
            print(error_message)
            raise TypeError(error_message)

        operation_function = self.operations[operation_symbol]

         
        try:
            sig = inspect.signature(operation_function)
            min_required = sum(
                1 for p in sig.parameters.values()
                if p.default == inspect.Parameter.empty
                and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            )
        except (ValueError, TypeError):
            min_required = 2

        # Check second_number requirements and validity
        if min_required > 1:
            if second_number is None:
                error_message = f"Error: Operation '{operation_symbol}' requires a second number."
                print(error_message)
                raise ValueError(error_message)

            if not isinstance(second_number, (int, float)) or isinstance(second_number, bool):
                error_message = (
                    f"Error: Invalid input '{second_number}'. "
                    f"The second input must be a valid number (int or float)."
                )
                print(error_message)
                raise TypeError(error_message)
        else:
            # If second_number is provided for an optional/unary operation, ensure it is a number
            if second_number is not None and (
                not isinstance(second_number, (int, float)) or isinstance(second_number, bool)
            ):
                error_message = (
                    f"Error: Invalid input '{second_number}'. "
                    f"The second input must be a valid number (int or float)."
                )
                print(error_message)
                raise TypeError(error_message)

        # Execute the operation
        try:
            if second_number is not None:
                try:
                    result = operation_function(first_number, second_number)
                except TypeError:
                    result = operation_function(first_number)
            else:
                result = operation_function(first_number)
            return result
        except Exception as e:
            error_message = f"Error during calculation: {e}"
            print(error_message)
            raise


def parse_input_number(user_input):
     
    user_input = user_input.strip()
    try:
        val = float(user_input)
        if val.is_integer():
            return int(val)
        return val
    except ValueError:
        return user_input


def main():
     
    calc = Calculator()

    # Register advanced operations
    calc.add_operation('^', exponentiation)
    calc.add_operation('**', exponentiation)
    calc.add_operation('sqrt', square_root)
    calc.add_operation('log', logarithm)

    print("=" * 50)
    print("Welcome to the Python Calculator!")
    print("Available operations:")
    print("  Basic:    +, -, *, /")
    print("  Advanced: ^ or ** (exponentiation), sqrt (square root), log (logarithm)")
    print("Type 'exit' or 'quit' at any prompt to terminate.")
    print("=" * 50)

    while True:
        try:
             
            raw_num1 = input("\nEnter first number: ").strip()
            if raw_num1.lower() in ('exit', 'quit', 'q'):
                print("Exiting calculator. Goodbye!")
                break
            num1 = parse_input_number(raw_num1)

             
            symbol = input("Enter operation symbol (+, -, *, /, ^, **, sqrt, log): ").strip()
            if symbol.lower() in ('exit', 'quit', 'q'):
                print("Exiting calculator. Goodbye!")
                break

             
            num2 = None
            if symbol in ('sqrt', '√'):
                 
                pass
            elif symbol == 'log':
                raw_num2 = input("Enter base for log (press Enter for natural log base e): ").strip()
                if raw_num2.lower() in ('exit', 'quit', 'q'):
                    print("Exiting calculator. Goodbye!")
                    break
                if raw_num2 != "":
                    num2 = parse_input_number(raw_num2)
            else:
                raw_num2 = input("Enter second number: ").strip()
                if raw_num2.lower() in ('exit', 'quit', 'q'):
                    print("Exiting calculator. Goodbye!")
                    break
                num2 = parse_input_number(raw_num2)

             
            result = calc.calculate(num1, symbol, num2)
            print(f"Result: {result}")

        except Exception as e:
             
            print(f"[Operation failed: {type(e).__name__}]")

         
        choice = input("\nDo you want to perform another calculation? (yes/no): ").strip().lower()
        if choice in ('no', 'n', 'exit', 'quit', 'q'):
            print("Exiting calculator. Goodbye!")
            break


if __name__ == '__main__':
    main()
