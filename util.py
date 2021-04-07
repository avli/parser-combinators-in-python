import re
from collections import namedtuple


class ParseError(Exception):
    pass


Failure = namedtuple('Failure', ['expected', 'actual'])
Success = namedtuple('Success', ['data', 'rest'])


def _is_failure(x):
    return isinstance(x, Failure)


def text(match):
    def text_parser(s):
        if s.startswith(match):
            return Success(match, s[len(match):])
        return Failure(expected=f"'{match}'", actual=s)

    return text_parser


def regex(pattern):
    if not isinstance(pattern, re.Pattern):
        pattern = re.compile(pattern)

    def regex_parser(s):
        m = pattern.match(s)
        if m:
            return Success(m.group(0), s[len(m.group(0)):])
        return Failure(expected=pattern.pattern, actual=s)

    return regex_parser


def map(f, parser):
    def map_parser(s):
        result = parser(s)
        if _is_failure(result):
            return result
        return Success(f(result.data), result.rest)
    return map_parser


decimal_re = r'\d+(?:\.\d*)?'

parse_plus = plus = text('+')
parse_decimal = decimal = map(float, regex(decimal_re))


def plus_expr(s):
    left = decimal(s)
    if _is_failure(left):
        return left
    op = plus(left.rest)
    if _is_failure(op):
        return op
    right = decimal(op.rest)
    if _is_failure(right):
        return right
    return Success(left.data + right.data, right.rest)


def repeat(parser):
    def repeat_parser(s):
        buffer, rest, last_failure = [], s, None
        while True:
            result = parser(rest)
            if _is_failure(result):
                last_failure = result
                break
            buffer.append(result.data)
            rest = result.rest
        if len(buffer) == 0:
            return last_failure
        return Success(buffer, rest)
    return repeat_parser


def parse(parser, s):
    result = parser(s)
    if _is_failure(result):
        raise ParseError(f"Parse error. Expected {result.expected}, instead found {result.actual}.")
    return result
