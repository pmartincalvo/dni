# dni
Simple DNI class and operations.


Check if a string is a valid DNI. Get details on possible errors:
```python
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

>>> # Get objects with issue details.
>>> dni.issues("27592354")
{
    "issues":[
        {
            "type": "Missing check letter.",
            "details": {
                "correct_check_letter": "J"
            }
        }
    ]
}
```

Get the check letter character for a DNI number:

```python
>> > import dni
>> > dni.compute_check_letter("27592354")
"J"

>> > dni.add_check_letter("27592354")
"27592354J"
```

Avoid primitive obsession with the DNI class. Get the components of the DNI, format it in different ways, check for equality.

```python
>>> some_dni = dni.DNI("27592354J")
>>> some_dni.number
"27592354"
>>> some_dni.check_letter
"J"

>>>some_dni.format(upper=True, separator="-")
"27592354-J"
>>>some_dni.format(lower=True, separator="+++")
"27592354+++j"
>>>str(some_dni)
"27592354J"

>>> dni.DNI("27592354J") == dni.DNI("27592354-j")
True
```

Spot and solve missing or wrong check letter issues.
```python
>>> dni.check_letter_is_valid("27592354X")
False

>>> dni.has_check_letter("27592354")
False

>>> dni.add_or_fix_check_letter("27592354").format()
"27592354J"

>>> dni.add_or_fix_check_letter("27592354X").format()
"27592354J"

>>> DNI("27592354", fix_issues=True).format()
"27592354J"
```


Find one or more DNIs in text.

```python
>> > dni.text_contains_dni("El señor Forges, con DNI 12345678Z, sactamente.")
True

>> > dni.extract_dnis_from_text("Mi DNI no es 12543456-S, es el 65412354-D.")

```