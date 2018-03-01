# CSV File Format

ArkMatrix supports two versions of CSV file import/export, simple relationships and tagged relationships. Neither format supports a header row, i.e. every row will be interpreted as data.

## Simple Relationship Format

The simple relationship format consists of two columns representing an Above relationship, i.e. the Stratigraphic Unit in column A is Above the Stratigraphic Unit in column B.

Example:


|-------|-------|
| Unit1 | Unit2 |
| Unit2 | Unit3 |
| Unit2 | Unit4 |
| Unit3 | Unit5 |
| Unit4 | Unit5 |

## Tagged Relationship Format

The tagged relationship format supports more features by allowing relationships to be tagged in a third column, i.e. the tag in column C defines the relationship between the Stratigraphic Units in columns A and B.

File Metadata Tags:
* site
* dataset

Unit Metadata Tags:
* label
* status = allocated | assigned | void
* type = undefined | deposit | fill | cut | masonry | skeleton | timber

Relationship Tags:
* above - unit in column A is above unit in column B
* below - unit in column A is below unit in column B (use discouraged, prefer using above)
* sameas - unit in column A is same-as unit in column B
* contemporary - unit in column A is contemporary-with unit in column B

Aggregation Tags:
* subgroup - unit in column A is a member of subgroup in column B
* group - subgroup in column A is a member of group in column B
* landuse - group in column A is a member of landuse in column B

All Metadata and Aggregation tags are optional. Tags may be included in any order, except the 'site' and 'dataset' tags which if defined should be listed first so they can be used when processing the following units. It is recommended that the tags be written in the order listed above, i.e. File Metadata, Unit Metadata, Relationship, Aggregation.

Other tags may be included in the file, such as 'description' or 'location', but these will be ignored by ArkMatrix.

Example:


|-----------|-----------|--------------|
| MNO12     |           | site         |
| Area A    |           | dataset      |
| Unit1     | assigned  | status       |
| Unit1     | fill      | class        |
| Unit7     | void      | status       |
| Unit1     | Unit2     | above        |
| Unit2     | Unit3     | above        |
| Unit2     | Unit4     | above        |
| Unit3     | Unit5     | above        |
| Unit4     | Unit5     | above        |
| Unit5     | Unit6     | sameas       |
| Unit3     | Unit4     | contemporary |
| Unit1     | Subgroup1 | subgroup     |
| Unit2     | Subgroup2 | subgroup     |
| Unit3     | Subgroup2 | subgroup     |
| Unit4     | Subgroup3 | subgroup     |
| Unit5     | Subgroup3 | subgroup     |
| Unit6     | Subgroup3 | subgroup     |
| Subgroup1 | Group1    | group        |
| Subgroup2 | Group2    | group        |
| Subgroup3 | Group2    | group        |
