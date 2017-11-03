# BibX
XML-based Personal Bibliography Management

BibX is available as a desktop application using Electron and Photon. A Python API (which is no longer supported) is available in the `bibx-python` branch.

## XSLT
A set of xslt files for transformations to various formats are included in ./app/xml. To date, the following transformations are available:

- Transformation to HTML, sorting by year.
- Transformation to HTML, sorting by publication type.
- Transformation to plain text.
- Transformation to BibTeX.

The citation format roughly follows IEEE style.

## Contributions
Contributions are welcome. Specifically, new or updated xslt files are one way to contribute. The app automatically loads available transformations based on the xslt files in the xml folder, so placing new transformations in the folder will be incorporated into the export menu.
