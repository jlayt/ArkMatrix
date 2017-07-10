# ARK Matrix

A tool for creating and manipulating Harris Matrices.
Part of the Archaeological Recording Kit by L-P : Archaeology
<http://ark.lparchaeology.com>

## Features

The following features are currently supported by the command line tool and library:

*   Import from LST (BASP, Stratify, ArchEd) and CSV files
*   Export to CSV, GML, GraphML, GraphViz/Dot, GXL, TGF
*   Same-As reduction
*   Matrix validation
*   Matrix reduction
*   Automatic Subgroup and Group matrix generation

The following features are not currently supported:
*   Contemporary With relationships are preserved but otherwise not used

A GUI application for data entry and graph drawing is planned.

## Installation

Currently ARK Matrix must be manually installed and run from the command line.

*   Install Python if not already installed
*   Install NetworkX 'pip install networkx'
*   Download the source code from <https://github.com/lparchaeology/ArkMatrix/archive/master.zip>

## Usage

ArkMatrix is run from the command line.

*   Run 'python arkmatrix.py --help' to see the available options
*   ArkMatrix will guess the file formats from the file suffixes
*   The matrix will only be reduced if you set the --reduce or -r flag and the matrix is valid
*   The subgroup and group matrices will only be generated if you set the --group or -g flag and the matrix is valid.

To generate a graphical version of smaller matrices, install yEd <https://www.yworks.com/products/yed>.

*   Run 'python arkmatrix.py -r -s mysite.csv mysite.gml'
*   Open mysite.gml in yEd
*   Choose Layout > Hierarchical and click OK

## CSV Format

The simple CSV format consists of two columns representing a stratigraphic relationship between two contexts, the first column being above, the second column being below. If column 1 is left empty, then the previous value in column 2 is used as the above value (see <https://github.com/lparchaeology/ArkMatrix/blob/master/test/csv_simple.csv> for an example).

The advanced format consists of 3 columns, with the third column describing the stratigraphic relationship between the first two columns. The valid relationships are:

*   above - context in column 1 is above context in column 2
*   below - context in column 1 is below context in column 2 (converted to above)
*   sameas - context in column 1 is same as context in column 2
*   contemporary - context in column 1 is contemporary with context in column 2
*   subgroup - context in column 1 is in subgroup in column 2
*   group - subgroup in column 1 is in group in column 2
*   site - column 1 holds the site code
*   dataset - column 1 holds the dataset name
*   status - context in column 1 has the status in column 2, either allocated, assigned, or void
*   type - context in column 1 has the class in column 2, either undefined, deposit, fill, cut, masonry, skeleton or timber

See <https://github.com/lparchaeology/ArkMatrix/blob/master/test/csv_format.csv> for an example.
