# dni

<p align="center">
<a href="https://github.com/pmartincalvo/dni/actions"><img alt="Actions Status" src="https://github.com/pmartincalvo/dni/workflows/latest/badge.svg"></a>
<a href="https://dni.readthedocs.io/en/stable/?badge=stable"><img alt="Documentation Status" src="https://readthedocs.org/projects/dni/badge/?version=stable"></a>
<a href="https://github.com/pmartincalvo/dni/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://pypi.org/project/dni/"><img alt="PyPI" src="https://img.shields.io/pypi/v/dni"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Simple DNI class and operations to make your life easier with Spanish Ids.

Release: 0.2.0

```python
>>> import dni

>>> dni.is_valid("27592354J")
True

>>> # Not a DNI
>>> dni.is_valid("ABC123XYZ")
False

>>> dni.compute_check_letter("27592354")
"J"

>>> some_dni = dni.DNI("27592354J")
>>> some_dni.number
"27592354"
>>> some_dni.check_letter
"J"

>>> some_dni.format(case="upper", separator="-")
"27592354-J"

>>> dni.DNI("27592354J") == dni.DNI("27592354-j")
True

>>> dni.text_contains_dni("El señor Forges, con DNI 12345678Z, sactamente.")
True

>>> dni.extract_dnis_from_text("Mi DNI no es 12543456-S, es el 65412354-D.")
[DNI('12543456S'), DNI('65412354D')]

>>> dni.DNI.random()
DNI("02448431N")
```

## Install

```shell
$ pip install dni`
```

## Features

- Applies for Spanish DNI IDs.
- Check validity of DNIs.
- Get check letter for a DNI number.
- Avoid primitive obsession with the DNI class. Get the components of the DNI, 
  format it in different ways, check for equality.
- Find and extract multiple DNIs from text.
- Get detailed exceptions when a string has issues.
- Generate random, valid DNIs.


## Docs

- For an extensive compilation of usage examples, check the
  [quickstart](https://dni.readthedocs.io/en/0.2.0/quickstart.html) 
  in the docs.
- You can also check the full [API reference](https://dni.readthedocs.io/en/0.2.0/api_reference.html).

## Misc

- If you spot a bug or want to request a feature, feel free to open an issue in
  this repository.
