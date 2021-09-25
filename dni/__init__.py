from typing import List

import re

from .constants import (
    UPPERCASE_CHECK_DIGITS,
    LOWERCASE_CHECK_DIGITS,
    REGEX_FOR_8_DIGIT_NUMBER,
    REGEX_FOR_UPPER_OR_LOWER_CHECK_DIGIT,
)
from .exceptions import (
    MultipleMatchesException,
    InvalidCheckDigitException,
    MissingCheckDigitException,
    NoNumberFoundException,
)


class DNI:
    def __init__(self, potentiaL_dni_string: str, fix_issues: bool = False):
        try:
            self._look_for_issues_in_potential_dni_string(potentiaL_dni_string)
            self._dni = potentiaL_dni_string.upper()
        except (
            MissingCheckDigitException,
            InvalidCheckDigitException,
        ) as check_digit_issue:
            if not fix_issues:
                raise check_digit_issue
            number = self._dni = _extract_exactly_one_dni_number_from_string(
                potentiaL_dni_string
            )
            valid_check_digit = compute_check_digit(potentiaL_dni_string)
            self._dni = potentiaL_dni_string.upper()

    @property
    def number(self):
        return self._dni[:8]

    @property
    def check_digit(self):
        return self._dni[-1]

    def _look_for_issues_in_potential_dni_string(
        self, potential_dni_string: str
    ):
        has_8_digit_number = _contains_exactly_one_dni_number(
            potential_dni_string
        )
        if not has_8_digit_number:
            raise NoNumberFoundException(
                f"Could not find a potential DNI number in string: {potential_dni_string}"
            )

        has_check_digit_character = re.match(
            f"{REGEX_FOR_8_DIGIT_NUMBER}.*([{UPPERCASE_CHECK_DIGITS+LOWERCASE_CHECK_DIGITS}]{{1}})[a-zA-Z]*",
            potential_dni_string,
        )
        if not has_check_digit_character:
            raise MissingCheckDigitException(
                f"String does not contain the check digit character: {potential_dni_string}"
            )

        check_digit_character = has_check_digit_character.group(2).upper()
        check_digit_character_is_valid = (
            check_digit_character
            == compute_check_digit(
                _extract_exactly_one_dni_number_from_string(
                    potential_dni_string
                )
            )
        )

        if not check_digit_character_is_valid:
            raise InvalidCheckDigitException(
                f"Check digit in string does not correspond to number: {check_digit_character}"
            )


def compute_check_digit(dni_number: str) -> str:
    """
    Given a DNI number, obtain the correct check digit.
    :param dni_number: a valid dni number.
    :return: the check digit for the number as an uppercase, single character
    string.
    """
    return UPPERCASE_CHECK_DIGITS[int(dni_number) % 23]


def _contains_exactly_one_dni_number(a_string: str) -> bool:
    """
    Checks if a string contains exactly one 8 digit number.
    :param a_string: the string that could contain a number.
    :return: True if so, False otherwise.
    """
    try:
        _extract_exactly_one_dni_number_from_string(a_string)
        return True
    except (NoNumberFoundException, MultipleMatchesException):
        return False


def _extract_exactly_one_dni_number_from_string(
    string_that_contains_dni_number: str
) -> str:
    """
    Extracts a number with exactly 8 digits from a string. Raises an exception
    if the string does not contain such a number or contains more than one.
    :param string_that_contains_dni_number: the string that contains the
    number.
    :return: the number in string form.
    """
    results = _extract_multiple_dni_numbers_from_string(
        string_that_contains_dni_number
    )
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
