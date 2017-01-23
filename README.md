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
- Transformation to BibTeX.

The citation format roughly follows IEEE style. Support for other formats is forthcoming.

## Python
Python code is available for creating bibliographies, reading in and validation bibliography files, and performing the available transformations. This code will be extended with additional functionality, and a GUI added for managing bibliography files.
