from decimal import *

getcontext().prec = 6 # float calculation precise
op_weight = {op: i for i, op in enumerate("+-*/^")}
op_weight['-'] = op_weight['+']
op_weight['/'] = op_weight['*']


def parse_word(s: str, idx=0):
    """
    parsing words from string s
    :param s: string to be parsed
    :param idx: the starting index number of exception position (like 0-index. 1-index)
    :return: yield words that is parsed
    """

    int_mode = True
    num_val = ""
    for i, ch in enumerate(s):
        # parse operator
        if ch in "+-*/()^":
            if num_val:
                yield Decimal(num_val)
                num_val = ""
                int_mode = True
            yield ch
        # parse dot
        elif ch == '.':
            # validation
            if not int_mode:
                raise ValueError("{} is not a valid digit".format(num_val + '.'))
            # turn int num into float
            else:
                int_mode = False
                num_val += '.'
        elif ch.isdigit():
            num_val += ch
        else:
            raise ValueError("{}:\t'{}' is invalid".format(idx + i, ch))
    if num_val:
        yield Decimal(num_val)


def do_operate(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
    elif op == "^":
        return a ** b


def calc(command: str):
    if not command:
        return None
    val_stack, op_stack = [], []
    for v in parse_word(command):
        if isinstance(v, Decimal):
            val_stack.append(v)
        elif v in op_weight:
            while op_stack and op_stack[-1] != '(' and op_weight[v] <= op_weight[op_stack[-1]]:
                b, a = val_stack.pop(), val_stack.pop()
                val_stack.append(do_operate(a, b, op_stack.pop()))
            op_stack.append(v)
        elif v in "()":
            if v == '(':
                op_stack.append(v)
            else:
                while op_stack and op_stack[-1] != '(':
                    b, a = val_stack.pop(), val_stack.pop()
                    val_stack.append(do_operate(a, b, op_stack.pop()))
                if op_stack:
                    op_stack.pop()
                else:
                    raise ValueError("No corresponding '(' on the left")
    while op_stack:
        b, a = val_stack.pop(), val_stack.pop()
        val_stack.append(do_operate(a, b, op_stack.pop()))
    return val_stack[0]


if __name__ == "__main__":
    print(op_weight)
    print(*parse_word("1.23*23"))
    print(*parse_word("(1.+2/.3)*4-0.1"))
    try:
        print(*parse_word("2^4/2*13.-.23."))
    except Exception as e:
        print(e.args[0])
    print(calc("1+2-1+3-2-2"))
    print(calc("1+2-1+3-(2-2)"))
    try:
        print(calc("2-3)"))
    except Exception as e:
        print(e.args[0])
    print(calc(""))
    print(calc("1*2/3"))
    print(calc("1*2/3."))
    print(calc("2^4/2"))
    print(calc("2^(4/2)"))
    print(calc("0.26*(80*24/10^3)"))
    for d in range(5, 100, 5):
        formulation = "0.{}*9".format(d)
        print(formulation, '=', calc(formulation))

    from time import time

    t1 = time()
    for i in range(100):
        calc("9999^9999")
    print("cost time:", time() - t1, 's')

    print(calc("29/40*9"))

    try:
        calc("2;import os")
    except Exception as e:
        print(e)
