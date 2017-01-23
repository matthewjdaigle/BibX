# Bibliography class. It is a database of publications.
# It is based on an XML file format. Exporting to other
# formats is done with XLS transformations.

# Imports
from lxml import etree

####################################

def indent(elem, level=0):
    i = '\n' + '\t' * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '\t'
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

####################################

class Bibliography:

    def __init__(self, owner=None, filename=None):
        if filename is None:
            # Create empty DOM with bibliography root
            bibliography = etree.Element('bibliography')
            if owner is not None:
                bibliography.set('owner', owner)
            self.DOM = etree.ElementTree(bibliography)
        else:
            # Open and validate xml
            if not self.validateFile(filename):
                print(filename, "does not validate!")
                raise RuntimeError('Bibliography file is not valid.')

            # Set DOM
            self.DOM = etree.parse(filename)

    @staticmethod
    def validateFile(xmlFilename):
        xsd = '../Schema/Bibliography.xsd'
        # Open schema file
        with open(xsd, 'r') as f:
            schemaRoot = etree.XML(f.read())
        schema = etree.XMLSchema(schemaRoot)
        xmlParser = etree.XMLParser(schema=schema)
        try:
            with open(xmlFilename, 'r') as f:
                etree.fromstring(f.read(), xmlParser)
            return True
        except etree.XMLSchemaError:
            print(xmlParser.error_log)
            return False
        except etree.XMLSyntaxError:
            print(xmlParser.error_log)
            return False

    def print(self):
        print(etree.tounicode(self.DOM, pretty_print=True))

    def export(self, xsl, outputFile):
        xslt = etree.parse(xsl)
        transform = etree.XSLT(xslt)
        newDOM = transform(self.DOM)
        with open(outputFile, 'w') as file:
            #newDOM.write(file, pretty_print=True)
            file.write(str(newDOM))

    def addPublication(self, id, authors, title, type, abstract=None, location=None, school=None, book=None, volume=None,
                       number=None, month=None, year=None, doi=None, area=None, pages=None, url=None):
        publication = etree.Element('publication', id=id)
        titleElt = etree.SubElement(publication, 'title')
        titleElt.text = title
        typeElt = etree.SubElement(publication, 'type')
        typeElt.text = type
        authorsElt = etree.SubElement(publication,'authors')
        for author in authors:
            authorElt = etree.SubElement(authorsElt,'author')
            authorElt.text = author
        # Add optional elements
        if abstract is not None:
            abstractElt = etree.SubElement(publication, 'abstract')
            abstractElt.text = abstract
        if location is not None:
            locationElt = etree.SubElement(publication, 'location')
            locationElt.text = location
        if school is not None:
            schoolElt = etree.SubElement(publication, 'school')
            schoolElt.text = school
        if book is not None:
            bookElt = etree.SubElement(publication, 'book')
            bookElt.text = book
        if volume is not None:
            volumeElt = etree.SubElement(publication, 'volume')
            volumeElt.text = volume
        if number is not None:
            numberElt = etree.SubElement(publication, 'number')
            numberElt.text = number
        if month is not None:
            monthElt = etree.SubElement(publication, 'month')
            monthElt.text = month
        if year is not None:
            yearElt = etree.SubElement(publication, 'year')
            yearElt.text = year
        if doi is not None:
            doiElt = etree.SubElement(publication, 'doi')
            doiElt.text = doi
        if area is not None:
            areaElt = etree.SubElement(publication, 'area')
            areaElt.text = area
        if pages is not None:
            pagesElt = etree.SubElement(publication, 'pages')
            pagesElt.text = pages
        if url is not None:
            urlElt = etree.SubElement(publication, 'url')
            urlElt.text = url
        # Add publication to bibliography
        self.DOM.getroot().insert(0, publication)


def test():
    # Create empty bibliography
    bib = Bibliography(owner='F. Author')
    # Add a publication
    bib.addPublication(id='Author2015Paper', title='New Paper Title', authors=['F. Author', 'S. Author', 'T. Author'], type='Conference',
                    abstract='This is the abstract.', location='City, USA', book='Proceedings of the Fancy Conference',
                    month='April', year='2015')
    bib.addPublication(id='Author2016Paper', title='New Paper Title', authors=['S. Author', 'F. Author'], type='Journal',
                    abstract='This is the abstract.', book='Journal of Papers', pages='100-110', volume='3', number='10',
                    month='April', year='2016')
    bib.addPublication(id='Author2017Paper', title='Another Paper Title', authors=['F. Author'], type='Conference',
                    abstract='This is the abstract.', location='City, USA', book='Proceedings of the Fancy Conference',
                    month='April', year='2017')
    bib.print()


    # Read in bibliography file
    print('Reading in Example.xml...')
    bib = Bibliography(filename='../Bibliographies/Example.xml')

    # Test transformations
    print('Transforming to HTML, organized by year...')
    bib.export('../XSLT/bibliographyToHTMLByYear.xslt','../Test/BibByYear.html')
    print('Transforming to HTML, organized by type...')
    bib.export('../XSLT/bibliographyToHTMLByType.xslt','../Test/BibByType.html')
    print('Transforming to plain text...')
    bib.export('../XSLT/bibliographyToPlainText.xslt','../Test/Bib.txt')
    print('Transforming to BibTeX...')
    bib.export('../XSLT/bibliographyToBib.xslt','../Test/Bib.bib')

    # Next steps:
    # Python base code (Bibliography module)
    #   Need add/remove/get publication
    #   Need to be able to create an empty bibliography
    #   Need to be able to open bib file, save file, save updates
    #   Need soem sort of print for checking content (maybe plan text can do that?)
    #   Anything else in the bib base that is needed?
    # Python GUI (allowing editing of xml files and export functionality)



if __name__ == '__main__':
    test()
