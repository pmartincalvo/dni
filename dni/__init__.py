from typing import List

import re

from .constants import (
    UPPERCASE_CHECK_LETTERS,
    LOWERCASE_CHECK_LETTERS,
    REGEX_FOR_8_DIGIT_NUMBER,
    REGEX_FOR_UPPER_OR_LOWER_CHECK_LETTERS,
    UPPER_AND_LOWER_CASE_CHECK_LETTERS,
    REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER,
    REGEX_FOR_NOT_A_DNI_CHAR,
)
from .exceptions import (
    MultipleMatchesException,
    InvalidCheckDigitException,
    MissingCheckDigitException,
    NoNumberFoundException,
)

from .utils import store_exception, get_last_catched_exception


class DNI:
    def __init__(self, potentiaL_dni_string: str, fix_issues: bool = False):
        try:
            _look_for_issues_in_potential_dni_string(potentiaL_dni_string)
            self._dni = _remove_clutter_from_potential_dni_string(
                potentiaL_dni_string
            ).upper()
        except (
            MissingCheckDigitException,
            InvalidCheckDigitException,
        ) as check_letter_issue:
            store_exception(check_letter_issue)
            if not fix_issues:
                raise check_letter_issue
            number = self._dni = _extract_exactly_one_dni_number_from_string(
                potentiaL_dni_string
            )
            valid_check_letter = compute_check_letter(potentiaL_dni_string)
            self._dni = number + valid_check_letter.upper()

    @property
    def number(self):
        return self._dni[:8]

    @property
    def check_letter(self):
        return self._dni[-1]


def _look_for_issues_in_potential_dni_string(potential_dni_string: str):
    has_8_letter_number = _contains_exactly_one_dni_number(
        potential_dni_string
    )
    if not has_8_letter_number:
        raise NoNumberFoundException(
            f"Could not find a potential DNI number in string: {potential_dni_string}"
        )

    has_check_letter_character = _contains_one_dni_number_and_check_letter(potential_dni_string)
    if not has_check_letter_character:
        raise MissingCheckDigitException(
            f"String does not contain the check letter character: {potential_dni_string}"
        )

    check_letter_character = _extract_exactly_one_check_letter_from_string(potential_dni_string)
    check_letter_character_is_valid = (
        check_letter_character
        == compute_check_letter(
            _extract_exactly_one_dni_number_from_string(potential_dni_string)
        )
    )

    if not check_letter_character_is_valid:
        raise InvalidCheckDigitException(
            f"Check letter in string does not correspond to number: {check_letter_character}"
        )


def compute_check_letter(dni_number: str) -> str:
    """
    Given a DNI number, obtain the correct check letter.
    :param dni_number: a valid dni number.
    :return: the check letter for the number as an uppercase, single character
    string.
    """
    return UPPERCASE_CHECK_LETTERS[int(dni_number) % 23]


def _contains_one_dni_number_and_check_letter(a_string: str) -> bool:
    """
    Check if a string contains exactly one 8 letter number and a check letter.
    The validity of the check letter is not checked.
    :param a_string: the string that could contain a number and a check letter.
    :return: True if so, False otherwise.
    """
    if not _contains_exactly_one_dni_number(a_string):
        return False

    has_check_letter_character = re.findall(
        REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER, a_string
    )
    if not has_check_letter_character:
        return False

    return True


def _extract_exactly_one_check_letter_from_string(a_string: str) -> str:
    """
    Extracts the check letter out of string that could be a DNI. Will raise an
    exception if the string does not represnt a DNI.
    :param a_string: the string that contains the check letter.
    :return: the check letter found in the string.
    """
    if not _contains_one_dni_number_and_check_letter(a_string):
        _look_for_issues_in_potential_dni_string(a_string)

    return re.findall(REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER, a_string)[0][1]
    # Get first result and get second capture group,
    # which is the one for the check letter


def _contains_exactly_one_dni_number(a_string: str) -> bool:
    """
    Checks if a string contains exactly one 8 letter number.
    :param a_string: the string that could contain a number.
    :return: True if so, False otherwise.
    """
    try:
        _extract_exactly_one_dni_number_from_string(a_string)
        return True
    except (NoNumberFoundException, MultipleMatchesException) as e:
        store_exception(e)
        return False


def _extract_exactly_one_dni_number_from_string(
    string_that_contains_dni_number: str
) -> str:
    """
    Extracts a number with exactly 8 letters from a string. Raises an exception
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
    Extracts all occurences of 8 letter numbers in the string. Raises an
    exception if the string does not contain such a number or contains more
    than one.
    :param string_that_contains_dni_numbers: the string that contains some
    nubmers.
    :return: a list with the found numbers.
    """

    results = re.findall(
        REGEX_FOR_8_DIGIT_NUMBER, string_that_contains_dni_numbers
    )  # TODO CONTINUE HERE substitute that regex for this, that solves the issue
    if not results:
        raise NoNumberFoundException()

    return results


def _remove_clutter_from_potential_dni_string(a_string: str) -> str:
    """
    Removes all characters that are not part of the valid characters for a DNI
    from a string.
    :param a_string: the string to remove the characters from.
    :return: the same string, without any character that is not a valid DNI
    character.
    """
    string_without_clutter = re.sub(REGEX_FOR_NOT_A_DNI_CHAR, "", a_string)

    return string_without_clutter
