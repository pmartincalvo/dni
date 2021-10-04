from typing import List

import re

from ._version import __version__
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
    InvalidCheckLetterException,
    MissingCheckLetterException,
    NoNumberFoundException,
    DNIExceptionDetails,
)

__all__ = [
    "DNI",
    "is_valid",
    "has_check_letter",
    "compute_check_letter",
    "add_or_fix_check_letter",
    "text_contains_dni",
    "extract_dnis_from_text",
    "MissingCheckLetterException",
    "InvalidCheckLetterException",
    "NoNumberFoundException",
]


class DNI:
    """
    A DNI.

    :param potentiaL_dni_string: the string that may contain a DNI.
    :param fix_issues: whether to fix check letter issues if found.
    """

    def __init__(self, potentiaL_dni_string: str, fix_issues: bool = False):
        try:
            _search_and_raise_issues_with_potential_dni_string(
                potentiaL_dni_string
            )
            self._dni = _remove_clutter_from_potential_dni_string(
                potentiaL_dni_string
            ).upper()
        except (MissingCheckLetterException, InvalidCheckLetterException):
            if not fix_issues:
                _search_and_raise_issues_with_potential_dni_string(
                    potentiaL_dni_string
                )  # Call it again but let it raise this time
            number = self._dni = _extract_exactly_one_dni_number_from_string(
                potentiaL_dni_string
            )
            valid_check_letter = compute_check_letter(number)
            self._dni = number + valid_check_letter.upper()

    @property
    def number(self) -> str:
        """
        Get the number part of the DNI.

        :return: the number.
        """
        return self._dni[:8]

    @property
    def check_letter(self) -> str:
        """
        Get the check letter of the DNI.

        :return: the check letter.
        """
        return self._dni[-1]

    def __eq__(self, other) -> bool:
        """
        Check equality by comparing to another DNI instance. If a string is
        passed, an attempt will be made to turn it into a DNI to execute the
        comparison.

        :param other: a DNI instance, or a string that could be a DNI.
        :return: True if equal, False otherwise.
        """
        is_a_dni_object = isinstance(other, DNI)
        is_a_string = isinstance(other, str)
        if not (is_a_dni_object or is_a_string):
            return False

        if is_a_string:
            try:
                other = DNI(other)
            except (
                MissingCheckLetterException,
                InvalidCheckLetterException,
                NoNumberFoundException,
            ):
                return False

        numbers_are_identical = self.number == other.number
        check_letters_are_identical = self.check_letter == other.check_letter

        both_are_same_dni = (
            numbers_are_identical and check_letters_are_identical
        )

        return both_are_same_dni

    def __str__(self):
        return self.format()

    def __repr__(self):
        return f"DNI('{self.format()}')"

    def format(self, case: str = "upper", separator: str = "") -> str:
        """
        Get a string representation of the DNI, with some formatting options.

        :param case: whether to put the check letter in upper or lower case.
        :param separator: an option seperator string to put between the number
         and the check letter.
        :return: a string with the DNI, formatted as defined.
        """
        if case not in ("upper", "lower"):
            raise ValueError(
                f"Case must be either 'upper' or 'lower', not {case}"
            )

        if case == "upper":
            return self.number + separator + self.check_letter.upper()

        return self.number + separator + self.check_letter.lower()


def is_valid(potential_dni_string: str) -> bool:
    """
    Check if a string contains a valid DNI.

    :param potential_dni_string: the string that may contain a DNI.
    :return: True if so, False otherwise.
    """

    try:
        DNI(potential_dni_string)
        return True
    except (
        NoNumberFoundException,
        MissingCheckLetterException,
        InvalidCheckLetterException,
    ):
        return False


def check_letter_is_valid(potential_dni_string: str) -> bool:
    """
    Check if the check letter of a DNI string is valid. Will raise an exception
    if the string is not a complete DNI.

    :param potential_dni_string: the string that may contain a DNI.
    :return: True if so, False otherwise.
    """

    try:
        _search_and_raise_issues_with_potential_dni_string(
            potential_dni_string
        )
        return True
    except InvalidCheckLetterException:
        return False


def has_check_letter(potential_dni_string: str) -> bool:
    """
    Check if the DNI string has a check letter. Will raise an exception if the
    string does not, at least, match a DNI number. Does not check the validity
    of the check letter if one is found.

    :param potential_dni_string: the string that may contain a DNI.
    :return: True if so, False otherwise.
    """

    try:
        _search_and_raise_issues_with_potential_dni_string(
            potential_dni_string
        )
        return True
    except MissingCheckLetterException:
        return False
    except InvalidCheckLetterException:
        return True


def compute_check_letter(dni_number: str) -> str:
    """
    Given a DNI number, obtain the correct check letter.

    :param dni_number: a valid dni number.
    :return: the check letter for the number as an uppercase, single character
     string.
    """
    return UPPERCASE_CHECK_LETTERS[int(dni_number) % 23]


def add_or_fix_check_letter(dni_or_number_string: str) -> str:
    """
    Add the right letter to a DNI number, or replace the existing one if it is
    not valid. DNIs without issues will return unchanged.

    :param dni_or_number_string: the string that contains a complete DNI or a
     DNI number without the check letter.
    :return: the DNI number with the valid check letter.
    """
    try:
        _search_and_raise_issues_with_potential_dni_string(
            dni_or_number_string
        )
        return dni_or_number_string  # If no exception, nothing to change
    except (MissingCheckLetterException, InvalidCheckLetterException):
        return DNI(dni_or_number_string, fix_issues=True).format()


def text_contains_dni(text: str) -> bool:
    """
    Check if a text contains or more DNI occurrences.

    :param text: a text that may contain some or no DNI-valid substrings.
    :return: True if so, False otherwise.
    """
    dni_matching_strings = re.findall(
        REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER, text
    )

    if dni_matching_strings:
        return True

    return False


def extract_dnis_from_text(text: str) -> List[DNI]:
    """
    Find DNI-valid substrings in a text and generate DNI instances from them.

    :param text: a text that may contain some or no DNI-valid substrings.
    :return: a list with the found DNIs as instances of the DNI class.
    """

    dni_matching_strings = re.findall(
        REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER, text
    )

    found_dnis = [
        DNI(number + check_letter)
        for number, check_letter in dni_matching_strings
    ]

    return found_dnis


def _search_and_raise_issues_with_potential_dni_string(
    potential_dni_string: str
) -> None:
    """
    Parse a string to see if it contains a DNI. If not, raise an exception
    specifying why the string is not a valid DNI.

    :param potential_dni_string: the string that may contain a DNI.
    :return: None
    """
    has_8_letter_number = _contains_exactly_one_dni_number(
        potential_dni_string
    )
    if not has_8_letter_number:
        raise NoNumberFoundException(
            DNIExceptionDetails(string=potential_dni_string)
        )

    number = _extract_exactly_one_dni_number_from_string(potential_dni_string)

    has_check_letter_character = _contains_one_dni_number_and_check_letter(
        potential_dni_string
    )
    if not has_check_letter_character:
        raise MissingCheckLetterException(
            DNIExceptionDetails(string=potential_dni_string, number=number)
        )

    found_check_letter_character = _extract_exactly_one_check_letter_from_string(
        potential_dni_string
    ).upper()

    valid_check_letter = compute_check_letter(number)
    check_letter_character_is_valid = (
        found_check_letter_character == valid_check_letter
    )

    if not check_letter_character_is_valid:
        raise InvalidCheckLetterException(
            DNIExceptionDetails(
                string=potential_dni_string,
                number=number,
                invalid_check_letter=found_check_letter_character,
                valid_check_letter=valid_check_letter,
            )
        )


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
        _search_and_raise_issues_with_potential_dni_string(a_string)

    return re.findall(REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER, a_string)[0][1]
    # Get first result and get second capture group, which is the one for the
    # check letter.


def _contains_exactly_one_dni_number(a_string: str) -> bool:
    """
    Checks if a string contains exactly one 8 letter number.

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
        raise NoNumberFoundException(
            DNIExceptionDetails(string=string_that_contains_dni_number)
        )
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
     numbers.
    :return: a list with the found numbers.
    """

    results = re.findall(
        REGEX_FOR_8_DIGIT_NUMBER, string_that_contains_dni_numbers
    )
    if not results:
        raise NoNumberFoundException(
            DNIExceptionDetails(string=string_that_contains_dni_numbers)
        )

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
