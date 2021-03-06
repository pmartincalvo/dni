UPPERCASE_CHECK_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
LOWERCASE_CHECK_LETTERS = UPPERCASE_CHECK_LETTERS.lower()
UPPER_AND_LOWER_CASE_CHECK_LETTERS = (
    UPPERCASE_CHECK_LETTERS + LOWERCASE_CHECK_LETTERS
)
REGEX_FOR_UPPER_OR_LOWER_CHECK_LETTERS = (
    f"(?<![{UPPER_AND_LOWER_CASE_CHECK_LETTERS}]{{1}})"
    f"([{UPPER_AND_LOWER_CASE_CHECK_LETTERS}]{{1}})"
    f"(?![{UPPER_AND_LOWER_CASE_CHECK_LETTERS}]{{1}})"
)
REGEX_FOR_8_DIGIT_NUMBER = "(?<![0-9]{1})([0-9]{8})(?![0-9]{1})"
MAX_ALLOWED_SEP_CHARS = 3
REGEX_FOR_FULL_DNI_WITH_POSSIBLE_CLUTTER = (
    f"{REGEX_FOR_8_DIGIT_NUMBER}.{{0,{MAX_ALLOWED_SEP_CHARS}}}"
    f"{REGEX_FOR_UPPER_OR_LOWER_CHECK_LETTERS}"
)
REGEX_FOR_NOT_A_DNI_CHAR = f"[^0-9{UPPER_AND_LOWER_CASE_CHECK_LETTERS}]"
NUMBER_CHARACTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
