# Bibliography Manager with GUI
#
# Matthew Daigle, October 2014

# Imports
import os
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Bibliography import Bibliography
from configparser import ConfigParser


class BibliographyManager(tkinter.Tk):

    def __init__(self):
        # Open config file
        parser = ConfigParser()
        parser.read('../BibX.config')
        self.configuration = dict()
        for section in parser.sections():
            for name, value in parser.items(section):
                self.configuration[name] = value

        # Create Bibliography object
        if 'file' not in self.configuration:
            self.configuration['file'] = 'Example.xml'
        self.filename = '../Bibliographies/' + self.configuration['file']
        self.bib = Bibliography(filename=self.filename)

        # Initialize some member variables
        self.labelVariables = dict()
        self.labels = dict()
        self.entryVariables = dict()
        self.entries = dict()
        self.publicationIndex = 0

        # Create/Initialize GUI
        tkinter.Tk.__init__(self)
        self.initialize()

    def initialize(self):
        # Create grid
        self.grid()

        # Basic config
        fgColor = '#EEEEEE'
        bgColor = '#555555'
        self.config(bg=bgColor)

        # Create profile image
        if tkinter.TkVersion < 8.6:
            photo = tkinter.PhotoImage(file='B.gif')
        else:
            photo = tkinter.PhotoImage(file='B.png')
        self.profileImageLabel = tkinter.Label(self, image=photo,
                                               anchor='center', bg=bgColor,
                                               height=100)
        self.profileImageLabel.image = photo
        self.profileImageLabel.grid(column=0, row=0, rowspan=4)

        # Create empty labels
        emptyLabel1 = tkinter.Label(self, bg=bgColor, height=1)
        emptyLabel1.grid(column=1, row=0)
        emptyLabel2 = tkinter.Label(self, bg=bgColor, height=2)
        emptyLabel2.grid(column=1, row=3)

        # Create owner entry
        self.ownerVariable = tkinter.StringVar()
        self.setOwner()
        self.ownerLabel = tkinter.Entry(self, textvariable=self.ownerVariable,
                                        bg=bgColor, fg=fgColor, width=95,
                                        font='Arial 11 bold', relief='flat')
        self.ownerLabel.bind('<Return>', self.onEnterOwner)
        self.ownerLabel.grid(column=1, row=1, columnspan=2)

        # Create fileName label
        self.fileNameVariable = tkinter.StringVar()
        self.fileNameVariable.set(self.filename)
        self.fileNameLabel = tkinter.Label(self,
                                           textvariable=self.fileNameVariable,
                                           anchor='nw', bg=bgColor, fg=fgColor,
                                           width=95, font='Arial 10 bold')
        self.fileNameLabel.bind('<Double-Button-1>', self.open)
        self.fileNameLabel.grid(column=1, row=2, columnspan=2)

        # Create publication number label
        self.publicationNumberVariable = tkinter.StringVar()
        self.publicationNumberLabel = tkinter.Label(self,
                                                    textvariable=self.publicationNumberVariable,
                                                    anchor='center',
                                                    font='Arial 10 bold',
                                                    bg=bgColor, fg=fgColor)
        self.publicationNumberLabel.grid(column=0, row=4)

        # Create previous/next buttons
        self.previousButton = tkinter.Button(self, text='Previous',
                                             command=self.onPreviousButtonClick,
                                             bg=bgColor, fg=fgColor,
                                             font='Arial 10 bold', bd=5,
                                             relief='ridge',
                                             activeforeground=bgColor,
                                             activebackground=fgColor)
        self.previousButton.grid(column=1, row=4, sticky='EW')
        self.nextButton = tkinter.Button(self, text='Next',
                                         command=self.onNextButtonClick,
                                         bg=bgColor, fg=fgColor,
                                         font='Arial 10 bold', bd=5,
                                         relief='ridge',
                                         activeforeground=bgColor,
                                         activebackground=fgColor)
        self.nextButton.grid(column=2, row=4, sticky='EW')
        currentRow = 6

        # Create text fields and load with values for first publication
        fields = ['type', 'title', 'authors', 'book', 'school', 'location',
                  'volume', 'number', 'pages', 'month', 'year', 'notes',
                  'area', 'url', 'id', 'abstract']
        for index, field in enumerate(fields):
            # Create label
            self.labelVariables[field] = tkinter.StringVar()
            self.labelVariables[field].set(field.capitalize())
            self.labels[field] = tkinter.Label(self,
                                               textvariable=self.labelVariables[field],
                                               anchor='nw',
                                               font='Arial 10 bold',
                                               bg=bgColor, fg=fgColor)
            self.labels[field].grid(column=0, row=index + currentRow,
                                    sticky='EW')
            # Create entry variable
            self.entryVariables[field] = tkinter.StringVar()
            if field == 'abstract':
                # Create Text object
                self.entries[field] = tkinter.Text(self, width=100, height=20,
                                                   wrap='word',
                                                   font='Arial 10',
                                                   relief='flat')
                self.labels[field].config(height=20)
            else:
                # Create entry GUI object
                self.entries[field] = tkinter.Entry(self,
                                                    textvariable=self.entryVariables[field],
                                                    width=100, font='Arial 10',
                                                    relief='flat')
            # Set grid location
            self.entries[field].grid(column=1, row=index + currentRow,
                                     columnspan=2, sticky='EW')

        # Create menu bar
        menuBar = tkinter.Menu(self, bg='black', fg='white')

        # Create pulldown menu for File
        fileMenu = tkinter.Menu(menuBar, tearoff=0, bg='black', fg='white',
                                activebackground=bgColor,
                                activeforeground=fgColor)
        fileMenu.add_command(label='New', command=self.new)
        fileMenu.add_command(label='Open...', command=self.open)
        fileMenu.add_command(label='Save', command=self.save)
        fileMenu.add_command(label='Save As...', command=self.saveAs)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.quit)
        menuBar.add_cascade(label='File', menu=fileMenu)

        # Create pulldown menu for Publication
        pubMenu = tkinter.Menu(menuBar, tearoff=0, bg='black', fg='white',
                               activebackground=bgColor,
                               activeforeground=fgColor)
        pubMenu.add_command(label='New...', command=self.addNewPublication)
        pubMenu.add_command(label='Delete', command=self.deletePublication)
        menuBar.add_cascade(label='Publication', menu=pubMenu)

        # Create pulldown menu for Export
        exportMenu = tkinter.Menu(menuBar, tearoff=0, bg='black', fg='white',
                                  activebackground=bgColor,
                                  activeforeground=fgColor)
        # Get list of available xslts
        for file in os.listdir('../XSLT/'):
            if file.endswith('.xslt'):
                filename = '../XSLT/' + file
                exportMenu.add_command(
                    label=file[0:-5],
                    command=lambda filename=filename: self.export(filename))
        exportMenu.add_separator()
        exportMenu.add_command(label='Custom...', command=self.exportCustom)
        menuBar.add_cascade(label='Export', menu=exportMenu)

        # display the menu
        self.config(menu=menuBar)

        # Add initial values
        self.setPublicationValues()

        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.update()
        self.geometry(self.geometry())
        self.entries['title'].selection_range(0, tkinter.END)

    def setOwner(self):
        self.ownerVariable.set(self.bib.getOwner() + "'s Bibliography")

    def onEnterOwner(self, event=[]):
        # Get new value entered and set it for the bib
        newText = self.ownerVariable.get()
        if newText.find("'s Bibliography") > 0:
            newName = newText[0:-15]
        else:
            newName = newText
        # Update with new name
        self.bib.setOwner(newName)
        self.setOwner()

    def setFileName(self, fileName):
        self.fileName = fileName
        self.fileNameVariable.set(self.fileName)

    def new(self):
        self.bib = Bibliography(owner='Owner Name')
        self.addNewPublication()
        self.setOwner()

    def open(self, event=[]):
        fileName = tkinter.filedialog.askopenfilename(
            title='Open Bibliography', defaultextension='.xml',
            filetypes=[('XML', '.xml')])
        if fileName:
            self.bib = Bibliography(fileName)
            self.publicationIndex = 0
            self.setPublicationValues()
            self.setOwner()
            self.setFileName(fileName)

    def save(self):
        ok = self.updatePublicationValues()
        if ok:
            self.bib.write(self.filename)

    def saveAs(self):
        ok = self.updatePublicationValues()
        if ok:
            file = tkinter.filedialog.asksaveasfile(
                title='Save Bibliography As...', defaultextension='.xml',
                filetypes=[('XML', '.xml')])
            self.bib.write(file.name)
            self.setFileName(file.name)

    def addNewPublication(self):
        self.bib.addPublication(id='Insert Unique Identifier Here',
                                authors=['Insert Authors Here'],
                                title='Insert Title Here', type='Conference')
        self.publicationIndex = 0
        self.setPublicationValues()

    def deletePublication(self):
        if tkinter.messagebox.askyesno('Verify Delete Publication',
                                       'Are you sure you want to delete this publication?'):
            self.bib.removePublication(index=self.publicationIndex)
            self.setPublicationValues()

    def setPublicationValues(self):
        # Get first publication
        publication = self.bib.getPublication(index=self.publicationIndex)
        self.publicationNumberVariable.set(
            str(self.publicationIndex + 1) + '/' + str(len(self.bib)))

        # Set up simple fields
        fields = ['id', 'type', 'title', 'book', 'school', 'location',
                  'volume', 'number', 'pages', 'month', 'year', 'notes',
                  'area', 'url', 'authors']
        for field in fields:
            text = publication.get(field)
            self.entryVariables[field].set(text)

        # Set up abstract
        self.entries['abstract'].delete('1.0', tkinter.END)
        text = publication.get('abstract')
        self.entries['abstract'].insert(tkinter.INSERT, text)

        # Configure buttons
        if self.publicationIndex == 0:
            self.previousButton.config(state='disabled')
        else:
            self.previousButton.config(state='normal')
        if self.publicationIndex == len(self.bib) - 1:
            self.nextButton.config(state='disabled')
        else:
            self.nextButton.config(state='normal')

    def updatePublicationValues(self, event=[]):
        # Check that type is one of the accepted values
        type = self.entryVariables['type'].get()
        if type != 'Conference' and type != 'Journal' and type != 'Unrefereed' and type != 'Dissertation' and type != 'Technical Report':
            tkinter.messagebox.showerror('Publication Error', 'Incorrect publication type specified!\nAccepted values are Journal, Conference, Unrefereed, Technical Report, and Dissertation.')
            return False

        # Get publication
        publication = self.bib.getPublication(index=self.publicationIndex)

        # Update values
        fields = ['id', 'type', 'title', 'book', 'school', 'location',
                  'volume', 'number', 'pages', 'month', 'year', 'notes',
                  'area', 'url', 'authors']
        for field in fields:
            publication.set(field, self.entryVariables[field].get())

        # Update abstract
        newAbstract = self.entries['abstract'].get('1.0', tkinter.END)
        newAbstract = newAbstract[0:-1]
        publication.set('abstract', newAbstract)

        # Return success
        return True

    def onPreviousButtonClick(self):
        # self.previousButton.focus_set()
        ok = self.updatePublicationValues()
        if ok:
            if self.publicationIndex > 0:
                self.publicationIndex -= 1
            self.setPublicationValues()

    def onNextButtonClick(self):
        # self.nextButton.focus_set()
        ok = self.updatePublicationValues()
        if ok:
            if self.publicationIndex < len(self.bib) - 1:
                self.publicationIndex += 1
            self.setPublicationValues()

    def export(self, filename):
        # Open up a prompt for file to export as
        outputFile = tkinter.filedialog.asksaveasfile(title='Save Output As...')
        if outputFile is not None:
            # Perform export
            self.bib.export(filename, outputFile.name)

    def exportCustom(self):
        # Open up a prompt for xls/xlst files
        filename = tkinter.filedialog.askopenfilename(
            title='Open XSL Transformation', defaultextension='.xslt',
            filetypes=[('XSLT', '.xsl*')])
        if filename != '':
            self.export(filename)


if __name__ == "__main__":
    app = BibliographyManager()
    app.title('BibX')
    app.mainloop()
