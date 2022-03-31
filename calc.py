from decimal import *
from fractions import Fraction

getcontext().prec = 6 # float calculation precise
op_weight = {op: i for i, op in enumerate("+-*/^")}  # the larger, the higher in priority
op_weight['-'] = op_weight['+']
op_weight['/'] = op_weight['*']
op_weight['pos'] = op_weight['neg'] = max(op_weight.values()) + 1
unary_operators = {
    '-': "neg",
    '+': "pos",
}


def f2d(n):
    """
    Fraction to Decimal convertion
    :param n: a Number
    :return: Decimal
    """
    if isinstance(n, Fraction):
        return Decimal(n.numerator) / Decimal(n.denominator)
    else:
        return Decimal(n)


def parse_word(s: str, idx: int = 0):
    """
    parsing words from string s
    :param s: string to be parsed
    :param idx: the starting index number of exception position (like 0-index. 1-index)
    :return: yield words that is parsed
    """

    int_mode = True  # reading int
    num_val = ""  # the value of parsed number
    value_parsed = False  # whether a number is parsed or not
    operator_val = ""
    for i, ch in enumerate(s):
        # parse operator
        if any(op.startswith(operator_val + ch) for op in op_weight):  # prefix match
            if value_parsed:
                if num_val:
                    yield Decimal(num_val)
                num_val = ""
                value_parsed = False
                int_mode = True
                yield ch

            else:  # parsing unary or other long operators
                if ch in unary_operators:
                    yield unary_operators[ch]
                else:
                    yield ch
        elif ch in '()':
            if value_parsed:
                if num_val:
                    yield Fraction(num_val)
                num_val = ""
                if ch == '(':
                    value_parsed = False
                int_mode = True
            yield ch
        # parse dot
        elif ch == '.':
            # validation
            if not int_mode:
                raise ValueError("{} is not a valid digit".format(num_val + '.'))
            # turn int number into float
            else:
                int_mode = False
                num_val += '.'
        elif ch.isdigit():
            value_parsed = True
            num_val += ch
        else:
            raise ValueError("{}:\t'{}' is invalid".format(idx + i, ch))
    if num_val:
        yield Decimal(num_val)


def do_operate(op, a, b):
    # operation between Decimal and Fraction is not allowed
    if type(a) != type(b):
        a, b = Fraction(a), Fraction(b)

    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        a, b = Fraction(a), Fraction(b)
        return Fraction(a, b)
    elif op == "^":
        return a ** b
    elif op == "pos":
        return a
    elif op == "neg":
        return -a
    else:
        raise ValueError("operator '{}' not found".format(op))


def calc(command: str):
    if not command:
        return 0
    val_stack, op_stack = [], []
    for v in parse_word(command):
        if isinstance(v, (Decimal, Fraction)):
            val_stack.append(v)
        elif v in op_weight:  # v is an operator
            while (op_stack
                   and op_stack[-1] != '('
                   and op_weight[v] <= op_weight[op_stack[-1]]):

                if op_stack[-1] in unary_operators.values():
                    a, b = val_stack.pop(), 0
                else:
                    b, a = val_stack.pop(), val_stack.pop()
                val_stack.append(do_operate(op_stack.pop(), a, b))
            op_stack.append(v)
        elif v in "()":
            if v == '(':
                op_stack.append(v)
            else:
                while op_stack and op_stack[-1] != '(':
                    if op_stack[-1] in unary_operators.values():
                        a, b = val_stack.pop(), 0
                    else:
                        b, a = val_stack.pop(), val_stack.pop()
                    val_stack.append(do_operate(op_stack.pop(), a, b))
                if op_stack:
                    op_stack.pop()
                else:
                    raise ValueError("No corresponding '(' on the left")
    while op_stack:
        if op_stack[-1] in unary_operators.values():
            a, b = val_stack.pop(), 0
        else:
            b, a = val_stack.pop(), val_stack.pop()
        val_stack.append(do_operate(op_stack.pop(), a, b))
    ans = val_stack[0]
    return f2d(ans)


if __name__ == "__main__":
    print(op_weight)
    from time import time

    t1 = time()
    for i in range(100):
        calc("9999^9999")
    print("cost time:", time() - t1, 's')