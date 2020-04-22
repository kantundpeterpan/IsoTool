# IsoTool
Isotopologue and mass spectrum calculator

## Dependencies
all dependencies are available via pip
- numpy
- pandas
- scipy
- IsoSpecPy
- gooey

## Installation
### Linux
pip wheel TBD

conda TBD

For the time being Linux users need to clone the rep and install dependencies manually.

### Windows
Windows users can either clone the repository or use a Release which comes bundled with Winpython
containing all necessary packages. Unzip and launch via `isotool_win.bat`.

## Usage
### Isotope definitions
#### Terrestrial
IsoTool comes with a .csv-file containing the terrestrial abundances of known elements 
(`data/isotopes_terrestrial.csv`), retrieved from the [National Institute of Standards
and Technology](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl).

#### Custom Isotope definitions
It is possible to define custom isotopes, e.g. for isotopoic labeling experiments. The
definitions have to be stored in a csv-file similar to the terrestrial isotope definitions.

```csv
element_symbol,mass_number,atomic_mass,abundance,
C,12,12.0000000000000,0.01
C,13,13.0033548350723,0.99
X,..,................,....
```
These files can easily be edited in any spreadsheet or text editor.

### Molecule
The Molecule file contains the elemental composition of the chemical species of interest.
```
element,n
C,54
X,20
..,..
```
Elements appearing in the molecule file need to have their isotopes defined in the
Isotope file used for the calculations.

## Usage
