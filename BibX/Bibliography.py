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

class Publication:

    def __init__(self, DOM):
        self.DOM = DOM

    def get(self, name):
        if name == 'id':
            # Id is an attribute
            return self.DOM.get(name)
        elif name == 'authors':
            # Authors contains child elements
            authors = self.DOM.find('authors')
            # Convert to string
            authorString = ''
            for author in authors:
                authorString += (author.text) + ', '
            return authorString[0:-2]
        else:
            # Remaining are elements
            text = self.DOM.find(name).text
            if text is None:
                text = ''
            return text

    def set(self, name, value):
        if name == 'id':
            # Id is an atribute
            self.DOM.set(name, value)
        elif name == 'authors':
            # Authors contains child elements
            authors = self.DOM.find('authors')
            authors.clear()
            # Value should be a string: a comma=separated list of names
            authorList = value.split(',')
            for author in authorList:
                authorElt = etree.SubElement(authors, 'author')
                authorElt.text = author.strip()
        else:
            self.DOM.find(name).text = value


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
            self.DOM.write(file, pretty_print=True, xml_declaration=True,
                           encoding='utf-8')

    def export(self, xsl, outputFile):
        xslt = etree.parse(xsl)
        transform = etree.XSLT(xslt)
        newDOM = transform(self.DOM)
        with open(outputFile, 'w') as file:
            file.write(str(newDOM))

    def setOwner(self, owner):
        self.DOM.getroot().set('owner', owner)

    def addPublication(self, id, authors, title, type, abstract=None,
                       location=None, school=None, book=None, volume=None,
                       number=None, month=None, year=None, doi=None, area=None,
                       pages=None, url=None, notes=None):
        publication = etree.Element('publication', id=id)
        titleElt = etree.SubElement(publication, 'title')
        titleElt.text = title
        typeElt = etree.SubElement(publication, 'type')
        typeElt.text = type
        authorsElt = etree.SubElement(publication, 'authors')
        for author in authors:
            authorElt = etree.SubElement(authorsElt, 'author')
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
                self.DOM.getroot().remove(publication.DOM)
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
            return Publication(self.DOM.getroot()[0])
        elif index is None:
            # Then return by id
            return Publication(self.DOM.find("publication[@id='"+id+"']"))
        else:
            # Return by index
            return Publication(self.DOM.getroot()[index])

    def __len__(self):
        return len(self.DOM.getroot())
