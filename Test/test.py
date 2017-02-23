import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from BibX import Bibliography
from lxml import etree


if __name__ == '__main__':
    # Create empty bibliography
    bib = Bibliography(owner='F. Author')
    print('Owner is', bib.getOwner())

    # Add some publications
    bib.addPublication(id='Author2015Paper', title='New Paper Title',
                       authors=['F. Author', 'S. Author', 'T. Author'],
                       type='Conference', abstract='This is the abstract.',
                       location='City, USA',
                       book='Proceedings of the Fancy Conference',
                       month='April', year='2015')
    bib.addPublication(id='Author2016Paper', title='New Paper Title',
                       authors=['S. Author', 'F. Author'], type='Journal',
                       abstract='This is the abstract.',
                       book='Journal of Papers', pages='100-110', volume='3',
                       number='10',
                       month='April', year='2016')
    bib.addPublication(id='Author2017Paper', title='Another Paper Title',
                       authors=['F. Author'], type='Conference',
                       abstract='This is the abstract.', location='City, USA',
                       book='Proceedings of the Fancy Conference',
                       month='April', year='2017')
    bib.print()
    print('This bibliography has', len(bib), 'publications.')

    # Get publications
    publication = bib.getPublication()
    print(etree.tounicode(publication.DOM, pretty_print=True))
    publication = bib.getPublication('Author2016Paper')
    print(etree.tounicode(publication.DOM, pretty_print=True))
    publication = bib.getPublication(id='Author2016Paper')
    print(etree.tounicode(publication.DOM, pretty_print=True))
    publication = bib.getPublication(index=2)
    print(etree.tounicode(publication.DOM, pretty_print=True))

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
    isValid = bib.validateFile('test.xml')
    print('Is test.xml valid?', isValid)

    # Read in bibliography file
    print('Reading in Example.xml...')
    bib = Bibliography(filename='example.xml')

    # Test transformations
    print('Transforming to HTML, organized by year...')
    bib.export('../XSLT/To HTML By Year.xslt', 'BibByYear.html')
    print('Transforming to HTML, organized by type...')
    bib.export('../XSLT/to HTML By Type.xslt', 'BibByType.html')
    print('Transforming to plain text...')
    bib.export('../XSLT/To Plain Text.xslt', 'Bib.txt')
    print('Transforming to BibTeX...')
    bib.export('../XSLT/to BibTeX.xslt', 'Bib.bib')
