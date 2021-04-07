import util


def assert_success(data, rest, result):
    assert data == result.data
    assert rest == result.rest


def assert_failure(expected, actual, result):
    assert expected == result.expected
    assert actual == result.actual


def test_parse_integer():
    assert_success(1, '', util.parse_decimal('1'))
    assert_success(2, '', util.parse_decimal('2'))
    assert_success(678, '', util.parse_decimal('678'))
    assert_success(678, 'abc', util.parse_decimal('678abc'))
    assert_failure(util.decimal_re, 'a', util.parse_decimal('a'))
    assert_failure(util.decimal_re, '', util.parse_decimal(''))


def test_parse_plus():
    assert_success('+', '42', util.parse_plus('+42'))
    assert_success('+', '42+42+42', util.parse_plus('+42+42+42'))
    assert_failure("'+'", '1+2+3', util.parse_plus('1+2+3'))


def test_plus_expr():
    assert_success(4, '', util.plus_expr('2+2'))
    assert_success(4, 'abc', util.plus_expr('2+2abc'))
    assert_failure(util.decimal_re, '+4+8', util.plus_expr('+4+8'))


def test_repeat():
    digits = util.regex(r'\d')
    parser = util.repeat(util.map(int, digits))
    assert_success([1, 2, 3], '', parser('123'))
