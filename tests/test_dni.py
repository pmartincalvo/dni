import pytest

import dni


@pytest.fixture
def dni_strings():
    return [
        {
            "valid": "27592354J",
            "without_checksum": "27592354",
            "with_wrong_checksum": "27592354X",
            "valid_checksum_character": "J",
        },
        {
            "valid": "12365487c",
            "without_checksum": "12365487",
            "with_wrong_checksum": "12365487h",
            "valid_checksum_character": "C",
        },
        {
            "valid": "31654234-R",
            "without_checksum": "31654234",
            "with_wrong_checksum": "31654234-p",
            "valid_checksum_character": "R",
        },
        {
            "valid": "45353534_h",
            "without_checksum": "45353534",
            "with_wrong_checksum": "45353534_t",
            "valid_checksum_character": "H",
        },
        {
            "valid": "    12315431 N ",
            "without_checksum": "12315431",
            "with_wrong_checksum": "12315431  H",
            "valid_checksum_character": "N",
        },
    ]


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


def test_is_valid_with_wrong_checksum_returns_false(dni_strings):
    validation_results = [
        dni.is_valid(dni_string["with_wrong_checksum"])
        for dni_string in dni_strings
    ]

    all_validations_returned_false = not any(validation_results)

    assert all_validations_returned_false


def test_is_valid_without_checksum_returns_false(dni_strings):
    validation_results = [
        dni.is_valid(dni_string["without_checksum"])
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


def test_issues_with_wrong_checksum_returns_wrong_checksum_report(dni_strings):
    list_of_issues = [
        dni.issues(dni_string["with_wrong_checksum"])
        for dni_string in dni_strings
    ]
    valid_checksums = [
        dni_string["valid_checksum_character"] for dni_string in dni_strings
    ]

    issues_reports_are_as_expected = all(
        [
            issues_report
            == {
                "issues": [
                    {
                        "type": "Wrong checksum.",
                        "details": {"correct_checksum": valid_checksum},
                    }
                ]
            }
            for issues_report, valid_checksum in zip(
                list_of_issues, valid_checksums
            )
        ]
    )

    assert issues_reports_are_as_expected


def test_issues_without_checksum_returns_wrong_checksum_report(dni_strings):
    list_of_issues = [
        dni.issues(dni_string["without_checksum"])
        for dni_string in dni_strings
    ]
    valid_checksums = [
        dni_string["valid_checksum_character"] for dni_string in dni_strings
    ]

    issues_reports_are_as_expected = all(
        [
            issues_report
            == {
                "issues": [
                    {
                        "type": "Missing checksum.",
                        "details": {"correct_checksum": valid_checksum},
                    }
                ]
            }
            for issues_report, valid_checksum in zip(
                list_of_issues, valid_checksums
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


def test_compute_checksum_with_valids_returns_same_character(dni_strings):
    numbers = [dni_string["without_checksum"] for dni_string in dni_strings]
    valid_checksum_characters = [
        dni_string["valid_checksum_character"] for dni_string in dni_strings
    ]

    computed_checksum_is_valid = [
        dni.compute_checksum(number) == valid_checksum_character.upper()
        for number, valid_checksum_character in zip(
            numbers, valid_checksum_characters
        )
    ]

    assert all(computed_checksum_is_valid)


def test_add_checksum_with_valids_returns_same_dni():
    numbers = [dni_string["without_checksum"] for dni_string in dni_strings]
    valid_dni = [dni_string["valid"] for dni_string in dni_strings]

    computed_checksum_is_valid = [
        dni.add_checksum(number) == valid_dni.upper()
        for number, valid_dni in zip(numbers, valid_dni)
    ]

    assert all(computed_checksum_is_valid)


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


class TestDNI:
    def test_instantiate_dni_with_valids_works(self):
        assert False

    def test_instantiate_dni_without_checksums_raises_error(self):
        assert False

    def test_instantiate_dni_without_checksums_with_fix_issues_works(self):
        assert False

    def test_instantiate_dni_with_not_a_dni_raises_value_error(self):
        assert False

    def test_dni_returns_components_correctly(self):
        assert False

    def test_several_format_combinations_output_as_expected(self):
        assert False

    def test_equality_works(self):
        assert False

    def test_inequality_works(self):
        assert False

    def test_checksum_is_valid_with_valids_returns_true(self):
        assert False

    def test_checksum_is_valid_with_wrongs_returns_false(self):
        assert False

    def test_has_checksum_with_valids_returns_true(self):
        assert False

    def test_has_checksum_with_invalids_returns_false(self):
        assert False

    def test_add_or_fix_checksum_with_valids_returns_without_change(self):
        assert False

    def test_add_or_fix_checksum_with_missing_returns_fixed(self):
        assert False

    def test_add_or_fix_checksum_with_wrong_returns_fied(self):
        assert False
