# BibX
XML-based Personal Bibliography Management

## Schema
The schema for bibliography collections is ./Schema/Bibliography.xsd.

## Bibliographies
Bibliography files are stored in the ./Bibliographies directory. An example file, ./Bibliographies/Example.xml, is included.

## XSLT
A set of XSLT files for transformations to various formats are incldued in ./XSLT. To date, the following transformations are available:

- Transformation to HTML, sorting by year.
- Transformation to HTML, sorting by publication type.
- Transformation to plain text.

The citation format roughly follows IEEE style. Support for other formats is forthcoming.

## Python
A set of Python modules will be made available for editing a bibliography XML file and performing the included XSL transformations.
