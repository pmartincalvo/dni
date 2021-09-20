def compute_checksum(dni_number: str) -> str:
    return "TRWAGMYFPDXBNJZSQVHLCKE"[int(dni_number) % 23]

def add_checksum(dni_number: str) -> str:
    return dni_number+compute_checksum(dni_number)
