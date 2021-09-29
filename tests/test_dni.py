import re

import pytest

import dni


@pytest.fixture
def dni_strings():
    return (
        {
            "valid": "27592354J",
            "without_check_letter": "27592354",
            "with_wrong_check_letter": "27592354X",
            "valid_check_letter_character": "J",
        },
        {
            "valid": "12365487c",
            "without_check_letter": "12365487",
            "with_wrong_check_letter": "12365487h",
            "valid_check_letter_character": "C",
        },
        {
            "valid": "31654234-R",
            "without_check_letter": "31654234",
            "with_wrong_check_letter": "31654234-p",
            "valid_check_letter_character": "R",
        },
        {
            "valid": "45353534_h",
            "without_check_letter": "45353534",
            "with_wrong_check_letter": "45353534_t",
            "valid_check_letter_character": "H",
        },
        {
            "valid": "    12315431 N ",
            "without_check_letter": "12315431",
            "with_wrong_check_letter": "12315431  H",
            "valid_check_letter_character": "N",
        },
    )


@pytest.fixture()
def dni_lookalikes():
    return ["123456789H", "435434-4H", "most probably, not a DNI"]


@pytest.fixture()
def text_with_two_dnis():
    return "Mi DNI no es 12543456-S, es el 65412354-D."


@pytest.fixture()
def text_with_no_dni():
    return "No DNI to find here, no matter how hard you look for it."


def test_is_valid_with_valids_returns_true(dni_strings):
    validation_results = [
        dni.is_valid(dni_string["valid"]) for dni_string in dni_strings
    ]

    all_validations_returned_true = all(validation_results)

    assert all_validations_returned_true


def test_is_valid_with_wrong_check_letter_returns_false(dni_strings):
    validation_results = [
        dni.is_valid(dni_string["with_wrong_check_letter"])
        for dni_string in dni_strings
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_is_valid_without_check_letter_returns_false(dni_strings):
    validation_results = [
        dni.is_valid(dni_string["without_check_letter"])
        for dni_string in dni_strings
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_is_valid_with_not_a_dni_returns_false(dni_lookalikes):
    validation_results = [
        dni.is_valid(lookalike) for lookalike in dni_lookalikes
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_issues_with_valids_returns_none(dni_strings):
    list_of_issues = [
        dni.issues(dni_string["valid"]) for dni_string in dni_strings
    ]

    all_issues_returned_none = all([issue is None for issue in list_of_issues])

    assert all_issues_returned_none


def test_issues_with_wrong_check_letter_returns_wrong_check_letter_report(
    dni_strings
):
    list_of_issues = [
        dni.issues(dni_string["with_wrong_check_letter"])
        for dni_string in dni_strings
    ]
    valid_check_letters = [
        dni_string["valid_check_letter_character"]
        for dni_string in dni_strings
    ]

    issues_reports_are_as_expected = all(
        [
            issues_report
            == {
                "issues": [
                    {
                        "type": "Wrong check_letter.",
                        "details": {
                            "correct_check_letter": valid_check_letter
                        },
                    }
                ]
            }
            for issues_report, valid_check_letter in zip(
                list_of_issues, valid_check_letters
            )
        ]
    )

    assert issues_reports_are_as_expected


def test_issues_without_check_letter_returns_wrong_check_letter_report(
    dni_strings
):
    list_of_issues = [
        dni.issues(dni_string["without_check_letter"])
        for dni_string in dni_strings
    ]
    valid_check_letters = [
        dni_string["valid_check_letter_character"]
        for dni_string in dni_strings
    ]

    issues_reports_are_as_expected = all(
        [
            issues_report
            == {
                "issues": [
                    {
                        "type": "Missing check_letter.",
                        "details": {
                            "correct_check_letter": valid_check_letter
                        },
                    }
                ]
            }
            for issues_report, valid_check_letter in zip(
                list_of_issues, valid_check_letters
            )
        ]
    )

    assert issues_reports_are_as_expected


def test_issues_without_8_numbers_returns_cant_find_number_report(
    dni_lookalikes
):
    list_of_issues = [dni.issues(lookalike) for lookalike in dni_lookalikes]

    issues_reports_are_as_expected = all(
        [
            issues_report
            == {"issues": [{"type": "Can't find DNI number in string."}]}
            for issues_report in list_of_issues
        ]
    )

    assert issues_reports_are_as_expected


def test_check_letter_is_valid_with_valids_returns_true(dni_strings):
    validation_results = [
        dni.check_letter_is_valid(dni_string["valid"])
        for dni_string in dni_strings
    ]

    all_validations_returned_true = all(validation_results)

    assert all_validations_returned_true


def test_check_letter_is_valid_with_wrongs_returns_false(dni_strings):
    validation_results = [
        dni.check_letter_is_valid(dni_string["wrong_check_letter"])
        for dni_string in dni_strings
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_check_letter_is_valid_without_check_letter_raises_exception(
    dni_strings
):
    for dni_string in dni_strings:
        with pytest.raises(ValueError):
            dni.check_letter_is_valid(dni_string["without_check_letter"])


def test_has_check_letter_with_valids_returns_true(dni_strings):
    validation_results = [
        dni.has_check_letter(dni_string["valid"]) for dni_string in dni_strings
    ]

    all_validations_returned_true = all(validation_results)

    assert all_validations_returned_true


def test_has_check_letter_with_invalids_returns_false(dni_strings):
    validation_results = [
        dni.has_check_letter(dni_string["without_check_letter"])
        for dni_string in dni_strings
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_add_or_fix_check_letter_with_valids_returns_without_change(
    dni_strings
):
    fixed_dnis = [
        dni.add_or_fix_check_letter(dni_string["valid"])
        for dni_string in dni_strings
    ]

    regular_dnis = [dni.DNI(dni_string["valid"]) for dni_string in dni_strings]

    both_are_equal = all(
        [
            fixed_dni == regular_dni
            for fixed_dni, regular_dni in zip(fixed_dnis, regular_dnis)
        ]
    )

    assert both_are_equal


def test_add_or_fix_check_letter_with_missing_returns_fixed(dni_strings):
    fixed_dnis = [
        dni.add_or_fix_check_letter(dni_string["without_check_letter"])
        for dni_string in dni_strings
    ]
    valid_check_letters = [
        dni_string["valid_check_letter_character"]
        for dni_string in dni_strings
    ]

    all_have_the_right_check_letter = all(
        [
            fixed_dni.check_letter == valid_check_letter
            for fixed_dni, valid_check_letter in zip(
                fixed_dnis, valid_check_letters
            )
        ]
    )

    assert all_have_the_right_check_letter


def test_add_or_fix_check_letter_with_wrong_returns_fixed(self):
    fixed_dnis = [
        dni.add_or_fix_check_letter(dni_string["wrong_check_letter"])
        for dni_string in dni_strings
    ]
    valid_check_letters = [
        dni_string["valid_check_letter_character"]
        for dni_string in dni_strings
    ]

    all_have_the_right_check_letter = all(
        [
            fixed_dni.check_letter == valid_check_letter
            for fixed_dni, valid_check_letter in zip(
                fixed_dnis, valid_check_letters
            )
        ]
    )

    assert all_have_the_right_check_letter


def test_compute_check_letter_with_valids_returns_same_character(dni_strings):
    numbers = [
        dni_string["without_check_letter"] for dni_string in dni_strings
    ]
    valid_check_letter_characters = [
        dni_string["valid_check_letter_character"]
        for dni_string in dni_strings
    ]

    computed_check_letter_is_valid = [
        dni.compute_check_letter(number)
        == valid_check_letter_character.upper()
        for number, valid_check_letter_character in zip(
            numbers, valid_check_letter_characters
        )
    ]

    assert all(computed_check_letter_is_valid)


def test_add_check_letter_with_valids_returns_same_dni(dni_strings):
    numbers = [
        dni_string["without_check_letter"] for dni_string in dni_strings
    ]
    valid_dni = [dni_string["valid"] for dni_string in dni_strings]

    computed_check_letter_is_valid = [
        dni.add_check_letter(number) == valid_dni.upper()
        for number, valid_dni in zip(numbers, valid_dni)
    ]

    assert all(computed_check_letter_is_valid)


def test_contains_dni_with_a_dni_returns_true(text_with_two_dnis):
    text_contains_dni = dni.contains_dni(text_with_two_dnis)

    assert text_contains_dni


def test_contains_dni_without_a_dni_returns_false(text_with_no_dni):
    text_contains_no_dni = not dni.contains_dni(text_with_no_dni)

    assert text_contains_no_dni


def test_extract_dnis_with_two_dnis_returns_two_dnis(text_with_two_dnis):
    extracted_dnis = dni.extract_dnis(text_with_two_dnis)

    assert False  # TODO use DNI class here when implemented


def test_extract_dnis_without_a_dni_returns_none(text_with_two_dnis):
    assert dni.extract_dnis(text_with_no_dni) == None


def test_extract_number_from_string_that_contains_it_extracts_succesfully(
    dni_strings
):
    numbers = [
        dni._extract_exactly_one_dni_number_from_string(dni_string["valid"])
        for dni_string in dni_strings
    ]

    all_numbers_have_8_letters = all([len(number) == 8 for number in numbers])

    assert all_numbers_have_8_letters


def test_extract_number_with_multiple_numbers_raises_exception(
    text_with_two_dnis
):
    with pytest.raises(dni.MultipleMatchesException):
        dni._extract_exactly_one_dni_number_from_string(text_with_two_dnis)


def test_extract_number_with_no_number_raises_exception(text_with_no_dni):
    with pytest.raises(dni.NoNumberFoundException):
        dni._extract_exactly_one_dni_number_from_string(text_with_no_dni)


def test_extract_numbers_with_multiple_numbers_returns_multiple_numbers(
    text_with_two_dnis
):
    numbers = dni._extract_multiple_dni_numbers_from_string(text_with_two_dnis)

    assert len(numbers) == 2


def test_extract_numbers_with_one_number_returns_one_number(dni_strings):
    numbers = dni._extract_multiple_dni_numbers_from_string(
        dni_strings[0]["valid"]
    )

    assert len(numbers) == 1


def test_extract_numbers_with_no_number_raises_exception(text_with_no_dni):
    with pytest.raises(dni.NoNumberFoundException):
        dni._extract_multiple_dni_numbers_from_string(text_with_no_dni)


def test_contains_number_and_check_letter_on_valid_dni_returns_true(
    dni_strings
):

    contain_numbers_and_check_letters = [
        dni._contains_one_dni_number_and_check_letter(dni_string["valid"])
        for dni_string in dni_strings
    ]

    all_are_true = all(contain_numbers_and_check_letters)

    assert all_are_true


def test_contains_number_and_check_letter_on_invalid_return_false(
    dni_lookalikes
):

    contain_numbers_and_check_letters = [
        dni._contains_one_dni_number_and_check_letter(lookalike)
        for lookalike in dni_lookalikes
    ]

    all_are_false = not all(contain_numbers_and_check_letters)

    assert all_are_false


def test_extract_check_letter_on_valid_returns_them(dni_strings):
    check_letters = [
        dni._extract_exactly_one_check_letter_from_string(dni_string["valid"])
        for dni_string in dni_strings
    ]

    all_are_valid_letters = [
        letter in dni.UPPER_AND_LOWER_CASE_CHECK_LETTERS
        for letter in check_letters
    ]
    all_are_one_char_long = [len(letter) == 1 for letter in check_letters]

    assert all_are_valid_letters and all_are_one_char_long


def test_extract_check_letter_on_invalid_raises_exception(dni_lookalikes):
    for lookalike in dni_lookalikes:
        with pytest.raises(
            (
                dni.NoNumberFoundException,
                dni.MissingCheckDigitException,
                dni.MultipleMatchesException,
            )
        ):
            dni._extract_exactly_one_check_letter_from_string(lookalike)


def test_remove_clutter_from_clutterless_string_returns_identical_string():
    cluterless_dni_string = "27592354J"

    processed_string = dni._remove_clutter_from_potential_dni_string(
        cluterless_dni_string
    )

    assert cluterless_dni_string == processed_string


def test_remove_clutter_from_cluttered_string_returns_clean():
    cluttered_dni_strng = "---!!!2.7.5.9.2.3.5.4.      J???"

    processed_string = dni._remove_clutter_from_potential_dni_string(
        cluttered_dni_strng
    )

    assert processed_string == "27592354J"


class TestDNI:
    def test_instantiate_dni_with_valids_works(self, dni_strings):
        dni_instances = [
            dni.DNI(dni_string["valid"]) for dni_string in dni_strings
        ]

        all_objects_are_dni = all(
            [isinstance(instance, dni.DNI) for instance in dni_instances]
        )

        assert all_objects_are_dni

    def test_instantiate_dni_without_check_letters_raises_error(
        self, dni_strings
    ):
        for dni_string in dni_strings:
            with pytest.raises(dni.MissingCheckDigitException):
                dni.DNI(dni_string["without_check_letter"])

    def test_instantiate_dni_with_wrong_check_letters_raises_error(
        self, dni_strings
    ):
        for dni_string in dni_strings:
            with pytest.raises(dni.InvalidCheckDigitException):
                dni.DNI(dni_string["with_wrong_check_letter"])

    def test_instantiate_dni_without_check_letters_with_fix_issues_works(
        self, dni_strings
    ):
        dni_instances = [
            dni.DNI(dni_string["without_check_letter"], fix_issues=True)
            for dni_string in dni_strings
        ]

        all_objects_are_dni = all(
            [isinstance(instance, dni.DNI) for instance in dni_instances]
        )

        assert all_objects_are_dni

    def test_instantiate_dni_with_not_a_dni_raises_value_error(
        self, dni_lookalikes
    ):
        for lookalike in dni_lookalikes:
            with pytest.raises(
                (
                    dni.NoNumberFoundException,
                    dni.MissingCheckDigitException,
                    dni.InvalidCheckDigitException,
                )
            ):
                dni.DNI(lookalike)

    def test_dni_returns_components_correctly(self, dni_strings):
        dni_instances = [
            dni.DNI(dni_string["valid"], fix_issues=True)
            for dni_string in dni_strings
        ]

        all_numbers_are_correct = all(
            [
                re.match(dni.REGEX_FOR_8_DIGIT_NUMBER, a_dni.number)
                for a_dni in dni_instances
            ]
        )

        all_check_letter_are_correct = all(
            [
                re.match(
                    dni.REGEX_FOR_UPPER_OR_LOWER_CHECK_LETTERS,
                    a_dni.check_letter,
                )
                for a_dni in dni_instances
            ]
        )

        assert all_numbers_are_correct and all_check_letter_are_correct

    def test_several_format_combinations_output_as_expected(self):
        a_dni = dni.DNI("27592354J")

        assert (
            (a_dni.format(lower=True) == "27592354j")
            and (a_dni.format(upper=True) == "27592354J")
            and (a_dni.format(lower=True, separator="$") == "27592354$j")
        )

    def test_equality_works(self):
        assert dni.DNI("27592354J") == dni.DNI("27592354J")

    def test_inequality_works(self):
        assert dni.DNI("27592354J") != dni.DNI("12365487c")
