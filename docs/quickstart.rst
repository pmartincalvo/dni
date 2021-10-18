Quickstart
===============

Here you can find how to install and use ``dni``.

Install
----------------

::

    $ pip install dni


Typical usage
----------------

Check if a string is/contains a valid DNI.

::

    >>> import dni

    >>> dni.is_valid("27592354J")
    True
    >>> dni.is_valid("27592354-J")
    True
    >>> dni.is_valid("   27592354-J")
    True


    >>> # Wrong check digit character. Should be 'J'.
    >>> dni.is_valid("27592354Y")
    False

    >>> # Missing check digit character. Should be 'J'.
    >>> dni.is_valid("27592354")
    False

    >>> # Not a DNI.
    >>> dni.is_valid("ABC123XYZ")
    False


Get the check letter character for a DNI number:

::

    >>> dni.compute_check_letter("27592354")
    "J"


Avoid primitive obsession with the DNI class. Get the components of the DNI, format it in different ways, check for equality.

::

    >>> some_dni = dni.DNI("27592354J")
    >>> some_dni.number
    "27592354"
    >>> some_dni.check_letter
    "J"

    >>> some_dni.format(case="upper", separator="-")
    "27592354-J"
    >>> some_dni.format(case="lower", separator="+++")
    "27592354+++j"
    >>> str(some_dni)
    "27592354J"

    >>> dni.DNI("27592354J") == dni.DNI("27592354-j")
    True


Spot and solve missing or wrong check letter issues.


::

    >>> dni.check_letter_is_valid("27592354X")
    False

    >>> dni.has_check_letter("27592354")
    False

    >>> dni.add_or_fix_check_letter("27592354").format()
    "27592354J"

    >>> dni.add_or_fix_check_letter("27592354X").format()
    "27592354J"

    >>> dni.DNI("27592354", fix_issues=True).format()
    "27592354J"

Find one or more DNIs in text.

::

    >>> dni.text_contains_dni("El señor Forges, con DNI 12345678Z, sactamente.")
    True

    >>> dni.extract_dnis_from_text("Mi DNI no es 12543456-S, es el 65412354-D.")
    [DNI('12543456S'), DNI('65412354D')]



Get details when things go wrong.

::

    >>> try:
    >>>     dni.DNI("27592354-?")
    >>> except dni.MissingCheckLetterException as exc:
    >>>     print(exc.render_as_dict())
    {
        'type': 'missing_check_letter',
        'details': {
            'message': "Could not find the check letter corresponding to number '27592354'.",
            'string': '27592354-?',
            'number': '27592354'
        }
    }

Generate one or multiple random, valid DNIs:

::

    >>> dni.DNI.random()
    DNI('12543456S')

    >>> dni.DNI.random(quantity=3)
    [DNI('12543456S'), DNI('65412354D'), DNI('71290112W')]
