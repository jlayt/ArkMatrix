# LST File Format

LST is the list format originally designed for BASP Harris, and later extended by ArchEd and Stratify. It can be read by most applications, but some don't export to it.

The following file definition is derived from the BASP and Stratify documentation and from inspecting a number of files exported from BASP and Stratify. For Stratify docs see http://www.stratify.org/Download/Stratify_Manual.pdf pages 21-25.

Header of 3 lines.

* Dataset Name
 * Must be a valid DOS filename, i.e. 8 chars long and excluding spaces or . [ ] ? \ / = " , + * : ; < > |

List of Strata records.

Strata records consist of 5 lines:

* First line of Stratum Name and optional Stratum Label
 * Line must not start with whitespace
 * Name consists of 8 chars excluding whitespaces, commas or colons (Stratify uses double colons for Site Code separator in Name)
 * Name and Label must be separated by at least one whitespace or comma
  * Stratify docs say Label must start after column 8, i.e. max name length, usually after 12
 * Label is up to 40 chars long
* Subsequent lines hold Stratum attributes
 * Line must start with whitespace, followed by the Attribute Name, optionally followed by a Strata List
  * Usual whitespace at start is 12 spaces
 * Attribute Name is one of 'above:', 'contemporary with:', 'equal to:' and 'below:'
 * Attribute Name is case insensitive
 * BASP outputs all four attributes even if they are empty
 * Extended only outputs those attributes that are populated
 * Extended adds extra attributes including 'Unit class:'
 * Attribute Name and Strata List are separated by whitespace
 * Strata Lists are comma and/or space separated

If multiple records exist for the same strata, relationship attributes are merged, not overridden.
