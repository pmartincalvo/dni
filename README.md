# dni
Simple DNI class and operations to make your life easier with Spanish Ids.

Release: 0.1.0

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


## Docs

- For an extensive compilation of usage examples, check the
  [quickstart](https://dni.readthedocs.io/en/0.1.0/quickstart.html) 
  in the docs.
- You can also check the full [API reference](https://dni.readthedocs.io/en/0.1.0/api_reference.html).

## Misc

- If you spot a bug or want to request a feature, feel free to open an issue in
  this repository.
