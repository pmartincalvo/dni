class NoNumberFoundException(Exception):
    """
    No DNI number was found in the string.
    """


class MissingCheckLetterException(Exception):
    """
    No check letter was found in the string.
    """


class InvalidCheckLetterException(Exception):
    """
    The check letter does not match with the number.
    """


class MultipleMatchesException(Exception):
    """
    Expected only one occurrence, but found multiple.
    """
