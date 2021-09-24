import re

from .exceptions import (
    MultipleMatchesException,
    InvalidCheckDigitException,
    MissingCheckDigitException,
    NoNumberFoundException,
)


def compute_check_digit(dni_number: str) -> str:
    """
    Given a DNI number, obtain the correct check digit.
    :param dni_number: a valid dni number.
    :return: the check digit for the number as an uppercase, single character
    string.
    """
    return "TRWAGMYFPDXBNJZSQVHLCKE"[int(dni_number) % 23]


def _extract_one_dni_number_from_string_that_contains_it(
    string_that_contains_dni_number: str
) -> str:
    """
    Extracts a number with exactly 8 digits from a string. Raises an exception
    if the string does not contain such a number or contains more than one.
    :param string_that_contains_dni_number: the string that contains the
    number.
    :return: the number in string form.
    """
    results = re.findall(
        "[^1-9]*([1-9]{8})[^1-9]*", string_that_contains_dni_number
    )
    if not results:
        raise NoNumberFoundException()
    if len(results) > 1:
        raise MultipleMatchesException()

    return results.pop()
