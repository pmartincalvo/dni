from collections import namedtuple

DNIExceptionDetails = namedtuple(
    "DNIExceptionDetails",
    field_names=[
        "message",
        "string",
        "number",
        "invalid_check_letter",
        "valid_check_letter",
    ],
)
DNIExceptionDetails.__new__.__defaults__ = (None,) * len(
    DNIExceptionDetails._fields
)  # Default None values, required for campatibility with Python < 3.7.


class DNIException(Exception):
    """
    Shared behaviour for custom defined exceptions in the DNI package.
    """

    description = None

    def __init__(self, message):
        """
        Init base class.
        """
        super().__init__(message)
        self.details_to_render = None

    def render_as_dict(self) -> dict:
        """
        Generate a dictionary indicating the exception description and a
        flexible details section.

        :return: the dictionary with the specific details of the raised
        exception.
        """
        return {"type": self.description, "details": self.details_to_render}


class NoNumberFoundException(DNIException):
    """
    No DNI number was found in the string.
    """

    description = "missing_dni_number"

    def __init__(self, exception_details: DNIExceptionDetails):
        self.details = exception_details
        self.message = exception_details.message
        if self.message is None:
            self.message = (
                f"Could not find a DNI number in: '{exception_details.string}'"
            )
        self.details_to_render = {
            "message": self.message,
            "string": self.details.string,
        }

        super().__init__(self.message)


class MissingCheckLetterException(DNIException):
    """
    No check letter was found in the string.
    """

    description = "missing_check_letter"

    def __init__(self, exception_details: DNIExceptionDetails):
        self.details = exception_details
        self.message = exception_details.message
        if self.message is None:
            self.message = (
                f"Could not find the check letter corresponding to number"
                f" '{self.details.number}'."
            )

        super().__init__(self.message)

        self.details_to_render = {
            "message": self.message,
            "string": self.details.string,
            "number": self.details.number,
        }


class InvalidCheckLetterException(DNIException):
    """
    The check letter does not match with the number.
    """

    description = "invalid_check_letter"

    def __init__(self, exception_details: DNIExceptionDetails):
        self.details = exception_details
        self.message = self.details.message
        if self.message is None:
            self.message = (
                f"Found check letter '{self.details.invalid_check_letter}' is not the"
                f" valid check letter for found number '{self.details.number}'."
            )

        self.details_to_render = {
            "message": self.details.message,
            "string": self.details.string,
            "found_number": self.details.number,
            "invalid_check_letter": self.details.invalid_check_letter,
            "valid_check_letter": self.details.valid_check_letter,
        }

        super().__init__(self.message)


class MultipleMatchesException(Exception):
    """
    Expected only one occurrence, but found multiple.
    """
