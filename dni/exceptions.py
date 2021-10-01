class DNIException(Exception):
    def __init__(self, *args, **kwargs):
        pass

    def render_as_dict(self):
        return {"type": self.description, "details": self.details}


class NoNumberFoundException(DNIException):
    """
    No DNI number was found in the string.
    """

    description = "missing_dni_number"

    def __init__(self, message: str = None, string: str = None):
        if message is None:
            message = f"Could not find a DNI number in: '{string}'"

        super().__init__(message)
        self.message = message
        self.string = string
        self.details = {"message": message, "string": string}


class MissingCheckLetterException(DNIException):
    """
    No check letter was found in the string.
    """

    description = "missing_check_letter"

    def __init__(
        self, message: str = None, string: str = None, number: str = None
    ):
        if message is None:
            message = (
                f"Could not find the check letter corresponding to number"
                f" '{number}'."
            )

        super().__init__(message)
        self.message = message
        self.string = string
        self.number = number
        self.details = {"message": message, "string": string, "number": number}


class InvalidCheckLetterException(DNIException):
    """
    The check letter does not match with the number.
    """

    description = "invalid_check_letter"

    def __init__(
        self,
        message: str = None,
        string: str = None,
        number: str = None,
        invalid_check_letter: str = None,
        valid_check_letter: str = None,
    ):
        if message is None:
            message = (
                f"Found check letter '{invalid_check_letter}' is not the"
                f" valid check letter for found number '{number}'."
            )

        super().__init__(message)
        self.message = message
        self.string = string
        self.number = number
        self.invalid_check_letter = invalid_check_letter
        self.details = {
            "message": message,
            "string": string,
            "found_number": number,
            "invalid_check_letter": invalid_check_letter,
            "valid_check_letter": valid_check_letter,
        }


class MultipleMatchesException(Exception):
    """
    Expected only one occurrence, but found multiple.
    """
