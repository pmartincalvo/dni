# History

## 0.2.0 - 2021-10-19

### Added
- Included a new method in the `DNI` class to generate random, valid DNIs.

## 0.1.1 - 2021-10-7

### Fixed 
- Functionality was breaking with DNIs that contained "0" in the number part
  due to an error in a regular expression. The regex has been fixed and DNIs
  with "0" are processed correctly.
