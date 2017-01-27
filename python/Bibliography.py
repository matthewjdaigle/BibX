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

    def __init__(self, filename=None, owner=None,):
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
            with open(xmlFilename, 'rb') as f:
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

    def write(self, filename):
        with open(filename, 'wb') as file:
            self.DOM.write(file, pretty_print=True, xml_declaration=True, encoding='utf-8')

    def export(self, xsl, outputFile):
        xslt = etree.parse(xsl)
        transform = etree.XSLT(xslt)
        newDOM = transform(self.DOM)
        with open(outputFile, 'w') as file:
            file.write(str(newDOM))

    def setOwner(self, owner):
        self.DOM.getroot().set('owner',owner)

    def addPublication(self, id, authors, title, type, abstract=None, location=None, school=None, book=None, volume=None,
                       number=None, month=None, year=None, doi=None, area=None, pages=None, url=None, notes=None):
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
        abstractElt = etree.SubElement(publication, 'abstract')
        if abstract is not None:
            abstractElt.text = abstract
        locationElt = etree.SubElement(publication, 'location')
        if location is not None:
            locationElt.text = location
        schoolElt = etree.SubElement(publication, 'school')
        if school is not None:
            schoolElt.text = school
        bookElt = etree.SubElement(publication, 'book')
        if book is not None:
            bookElt.text = book
        volumeElt = etree.SubElement(publication, 'volume')
        if volume is not None:
            volumeElt.text = volume
        numberElt = etree.SubElement(publication, 'number')
        if number is not None:
            numberElt.text = number
        monthElt = etree.SubElement(publication, 'month')
        if month is not None:
            monthElt.text = month
        yearElt = etree.SubElement(publication, 'year')
        if year is not None:
            yearElt.text = year
        doiElt = etree.SubElement(publication, 'doi')
        if doi is not None:
            doiElt.text = doi
        areaElt = etree.SubElement(publication, 'area')
        if area is not None:
            areaElt.text = area
        pagesElt = etree.SubElement(publication, 'pages')
        if pages is not None:
            pagesElt.text = pages
        urlElt = etree.SubElement(publication, 'url')
        if url is not None:
            urlElt.text = url
        notesElt = etree.SubElement(publication, 'notes')
        if notes is not None:
            notesElt.text = notes
        # Add publication to bibliography
        self.DOM.getroot().insert(0, publication)

    def removePublication(self, id=None, index=None):
        if id is None and index is None:
            raise RuntimeError('id or index must be specified')
        elif index is None:
            # Find element with given id
            publication = self.getPublication(id)
            if publication is not None:
                self.DOM.getroot().remove(publication)
            else:
                raise RuntimeError('Publication '+id+' does not exist')
        else:
            # Remove by index
            publication = self.DOM.getroot()[index]
            self.DOM.getroot().remove(publication)

    def getOwner(self):
        return self.DOM.getroot().get('owner')

    def getPublication(self, id=None, index=None):
        if id is None and index is None:
            # If no id or index is given, return first one
            return self.DOM.getroot()[0]
        elif index is None:
            # Then return by id
            return self.DOM.find("publication[@id='"+id+"']")
        else:
            # Return by index
            return self.DOM.getroot()[index]

    def __len__(self):
        return len(self.DOM.getroot())



####################################

def test():
    # Create empty bibliography
    bib = Bibliography(owner='F. Author')
    print('Owner is',bib.getOwner())
    
    # Add some publications
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
    print('This bibliograph has', len(bib),'publications.')

    # Get publications
    publication = bib.getPublication()
    print(etree.tounicode(publication, pretty_print=True))
    publication = bib.getPublication('Author2016Paper')
    print(etree.tounicode(publication, pretty_print=True))
    publication = bib.getPublication(id='Author2016Paper')
    print(etree.tounicode(publication, pretty_print=True))
    publication = bib.getPublication(index=2)
    print(etree.tounicode(publication, pretty_print=True))
    
    # Remove a publication, by id
    bib.removePublication('Author2017Paper')
    bib.print()
    # Remove a publication, by index
    bib.removePublication(index=0)
    bib.print()

    # Change owner
    bib.setOwner('T. Author')
    bib.print()
    bib.setOwner('F. Author')
    bib.print()

    # Write bibliography to file
    bib.write('../Test/test.xml')
    
    # Validate the result
    isValid = bib.validateFile('../Test/test.xml')
    print('Is test.xml valid?', isValid)

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

####################################

if __name__ == '__main__':
    test()
