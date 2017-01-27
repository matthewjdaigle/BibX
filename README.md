# BibX
XML-based Personal Bibliography Management

## Schema
The schema for a bibliography is ./Schema/Bibliography.xsd.

## Bibliographies
Bibliography files are stored in the ./Bibliographies directory. An example file, ./Bibliographies/Example.xml, is included.

## XSLT
A set of XSLT files for transformations to various formats are incldued in ./XSLT. To date, the following transformations are available:

- Transformation to HTML, sorting by year.
- Transformation to HTML, sorting by publication type.
- Transformation to plain text.
- Transformation to BibTeX.

The citation format roughly follows IEEE style. Support for other formats is forthcoming.

## Python Framework & GUI
A Python framework is available for creating bibliographies, reading and validating bibliography files, adding/removing publications, and performing the available transformations. A Python GUI is built on top of this framework implementing all the available functionality.
