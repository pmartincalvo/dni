def compute_checksum(dni_number: str) -> str:
    """
    Given a DNI number, obtain the correct checksum.
    :param dni_number: a valid dni number.
    :return: the checksum for the number as an uppercase, single character
    string.
    """
    return "TRWAGMYFPDXBNJZSQVHLCKE"[int(dni_number) % 23]
