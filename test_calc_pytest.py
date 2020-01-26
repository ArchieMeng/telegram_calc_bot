from calc import *


def test_parse_words():
    assert tuple(parse_word('1.23*23')) == (
        Decimal("1.23"),
        '*',
        Decimal("23")
    )
    assert tuple(parse_word("(1.+2/.3)*4-0.1")) == (
        "(",
        Decimal("1."),
        "+",
        Decimal("2"),
        "/",
        Decimal(".3"),
        ")",
        "*",
        Decimal("4"),
        "-",
        Decimal("0.1")
    )

def test_errors():
    try:
        print(*parse_word("2^4/2*13.-.23."))
        assert False
    except Exception as e:
        assert e.args[0] == ".23. is not a valid digit"

    try:
        print(calc("2-3)"))
        assert False
    except Exception as e:
        assert e.args[0] == "No corresponding '(' on the left"

    try:
        calc("2;import os")
        assert False
    except Exception as e:
        assert e.args[0] == "{}:\t'{}' is invalid".format(1, ';')


def test_calc_without_power():
    for d in range(5, 100, 5):
        formulation = "0.{}*9".format(d)
        assert calc(formulation) == Decimal("0.{}".format(d)) * Decimal("9")

    assert calc("1+2-1+3-2-2") == eval("1+2-1+3-2-2")
    assert calc("1+2-1+3-2-2") == 1
    assert calc("1+2-1+3-(2-2)") == 5
    assert calc("1+2-1+3-((2-2))") == 5
    assert calc("") == 0
    assert calc("1*2/3") == Decimal("2") / Decimal("3")
    assert calc("1*2/3.") == Decimal("2") / Decimal("3")
    assert calc(".314*4") == Decimal(".314") * Decimal("4")
    assert calc("(1+3)-2") == Decimal("2")
    assert calc("2*(1-3)-2") == Decimal("-6")
    assert calc("2*(22/7)*4+3.1415926") == Decimal("28.2845")
    assert calc("2*(1.5*2+4)+6") == Decimal("20")


def test_calc_with_power():
    assert calc("2^4/2") == 8
    assert calc("2^(4/2)") == 4
    assert calc("2+1^(1+(2*2-1))") == Decimal('3')
    assert calc("2+2^(1+(2*2-1))") == Decimal('18')
    assert calc("0.26*(80*24/10^3)") == Decimal("0.4992")
    assert calc("3*10^5*0.12") == Decimal("36000")
    assert calc("1-2.1*3+5^2*2") == (Decimal('1')
                                     - Decimal('2.1') * Decimal('3')
                                     + Decimal('5')
                                     ** Decimal('2') * Decimal('2'))
    assert calc("0.2^+300") == Decimal("0.2") ** Decimal("+300")
    assert calc("0.2^(+300)") == Decimal("0.2") ** Decimal("+300")
    assert calc("0.2^-300") == Decimal("0.2") ** Decimal("-300")
    assert calc("0.2^(-300)") == Decimal("0.2") ** Decimal("-300")
    assert calc("1+2*999^(-25*4+1)") == (Decimal('1')
                                         + Decimal('2')
                                         * Decimal('999')
                                         ** (Decimal('-25')
                                             * Decimal('4')
                                             + Decimal('1')))
