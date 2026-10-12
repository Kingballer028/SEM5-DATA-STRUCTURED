import re

class Stack:
    """A Last-In, First-Out (LIFO) collection."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Cannot remove an item from an empty stack.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise ValueError("Cannot view an empty stack.")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


PRIORITY = {"+": 1, "-": 1, "*": 2, "/": 2, "u+": 3, "u-": 3}
RIGHT_ASSOCIATIVE = {"u+", "u-"}


def tokenize(expression):
    """Split text into numeric values, operators and parentheses."""
    pattern = re.compile(r"\s*(?:(\d+(?:\.\d*)?|\.\d+)|([()+\-*/]))")
    tokens, position = [], 0
    while position < len(expression):
        match = pattern.match(expression, position)
        if not match:
            if expression[position:].strip() == "":
                break
            raise ValueError("Unsupported character near " + repr(expression[position:position+8]))
        number, symbol = match.groups()
        tokens.append(number if number is not None else symbol)
        position = match.end()
    if not tokens:
        raise ValueError("Expression is empty.")
    return tokens


def to_postfix(tokens):
    """Convert infix notation to postfix notation with an operator stack."""
    output, operators = [], Stack()
    previous = None
    for token in tokens:
        is_number = re.fullmatch(r"(?:\d+(?:\.\d*)?|\.\d+)", token) is not None
        if is_number:
            if previous in ("number", ")"):
                raise ValueError("An operator is missing between values.")
            output.append(token)
            previous = "number"
        elif token == "(":
            if previous in ("number", ")"):
                raise ValueError("An operator may be missing before '('.")
            operators.push(token)
            previous = "("
        elif token == ")":
            if previous in (None, "operator", "("):
                raise ValueError("Empty or incomplete parentheses.")
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Closing parenthesis has no matching opening parenthesis.")
            operators.pop()
            previous = ")"
        else:
            if token in ("+", "-") and previous in (None, "operator", "("):
                op = "u+" if token == "+" else "u-"
            else:
                if previous in (None, "operator", "("):
                    raise ValueError("Operator is missing a value before it.")
                op = token
            while not operators.is_empty() and operators.peek() != "(":
                top = operators.peek()
                if (PRIORITY[top] > PRIORITY[op] or
                    (PRIORITY[top] == PRIORITY[op] and op not in RIGHT_ASSOCIATIVE)):
                    output.append(operators.pop())
                else:
                    break
            operators.push(op)
            previous = "operator"
    if previous in (None, "operator", "("):
        raise ValueError("Expression is incomplete.")
    while not operators.is_empty():
        op = operators.pop()
        if op == "(":
            raise ValueError("Opening parenthesis has no matching closing parenthesis.")
        output.append(op)
    return output


def evaluate_postfix(tokens):
    """Calculate postfix tokens using a value stack."""
    values = Stack()
    for token in tokens:
        if token not in PRIORITY:
            values.push(float(token))
        elif token in ("u+", "u-"):
            if values.size() < 1:
                raise ValueError("Unary sign has no value.")
            value = values.pop()
            values.push(value if token == "u+" else -value)
        else:
            if values.size() < 2:
                raise ValueError("Operator does not have two values.")
            right, left = values.pop(), values.pop()
            if token == "+": answer = left + right
            elif token == "-": answer = left - right
            elif token == "*": answer = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                answer = left / right
            values.push(answer)
    if values.size() != 1:
        raise ValueError("Expression is not valid.")
    return values.pop()


def evaluate_expression(expression):
    return evaluate_postfix(to_postfix(tokenize(expression)))


def format_answer(value):
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f"{value:.10g}"


def read_expressions(text):
    """Separator lines of five or more hyphens mark new expressions."""
    sections = re.split(r"(?m)^\s*-{5,}\s*$", text)
    return [section.strip() for section in sections if section.strip()]


def process_files(input_file="input.txt", output_file="output.txt"):
    with open(input_file, "r", encoding="utf-8") as file:
        expressions = read_expressions(file.read())
    if not expressions:
        raise ValueError("No expressions were found in input.txt.")
    results = []
    for index, expression in enumerate(expressions, 1):
        try:
            results.append(format_answer(evaluate_expression(expression)))
        except (ValueError, ZeroDivisionError) as error:
            results.append(f"Expression {index} error: {error}")
    with open(output_file, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n-----\n".join(results) + "\n")


def main():
    try:
        process_files()
        print("Finished. Open output.txt to see the results.")
    except FileNotFoundError:
        print("input.txt was not found. Put it in the same folder as main.py.")
    except (OSError, ValueError) as error:
        print("Problem:", error)


if __name__ == "__main__":
    main()
