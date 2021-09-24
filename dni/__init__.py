from typing import List

import re

from .constants import UPPERCASE_CHECK_DIGITS, REGEX_FOR_8_DIGIT_NUMBER
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
    return UPPERCASE_CHECK_DIGITS[int(dni_number) % 23]


def _extract_one_dni_number_from_string(
    string_that_contains_dni_number: str
) -> str:
    """
    Extracts a number with exactly 8 digits from a string. Raises an exception
    if the string does not contain such a number or contains more than one.
    :param string_that_contains_dni_number: the string that contains the
    number.
    :return: the number in string form.
    """
    results = _extract_multiple_dni_numbers_from_string(string_that_contains_dni_number)
    if not results:
        raise NoNumberFoundException()
    if len(results) > 1:
        raise MultipleMatchesException()

    return results.pop()


def _extract_multiple_dni_numbers_from_string(
    string_that_contains_dni_numbers: str
) -> List[str]:
    """
    Extracts all occurences of 8 digit numbers in the string. Raises an
    exception if the string does not contain such a number or contains more
    than one.
    :param string_that_contains_dni_numbers: the string that contains some
    nubmers.
    :return: a list with the found numbers.
    """

    results = re.findall(
        REGEX_FOR_8_DIGIT_NUMBER, string_that_contains_dni_numbers
    )
    if not results:
        raise NoNumberFoundException()

    return results
