const {app, Menu, MenuItem} = require('electron').remote
var dialog = require('electron').remote.dialog;
var fs = require('fs');

// Get button elements
var newBibButton = document.getElementById('newBibButton');
var openButton = document.getElementById('openButton');
var saveButton = document.getElementById('saveButton');
var addButton = document.getElementById('addButton');
var removeButton = document.getElementById('removeButton');
var leftButton = document.getElementById('leftButton');
var rightButton = document.getElementById('rightButton');
var exportButton = document.getElementById('exportButton');

// Get other elements
var publications = document.getElementById('publications')
var editpub = document.getElementById('edit-pub');
var publist = document.getElementById('pub-list');
var ownerName = document.getElementById('owner-name');
var filenameFooter = document.getElementById('filename-footer');
var pubNavGroup = document.getElementById('pub-nav-group');
var pubForm = document.getElementById('pub-form');
var exportType = document.getElementById('export-type');

// Get input elements
var pubType = document.getElementById('pub-type')
var pubTitle = document.getElementById('pub-title');
var pubAuthors = document.getElementById('pub-authors');
var pubBook = document.getElementById('pub-book');
var pubSchool = document.getElementById('pub-school');
var pubLocation = document.getElementById('pub-location');
var pubVolume = document.getElementById('pub-volume');
var pubNumber = document.getElementById('pub-number');
var pubPages = document.getElementById('pub-pages');
var pubMonth = document.getElementById('pub-month');
var pubYear = document.getElementById('pub-year');
var pubNotes = document.getElementById('pub-notes');
var pubUrl = document.getElementById('pub-url');
var pubId = document.getElementById('pub-id');
var pubDoi = document.getElementById('pub-doi');
var pubAbstract = document.getElementById('pub-abstract');

// Add button listeners
newBibButton.addEventListener('click', newBib);
openButton.addEventListener('click', openBib);
saveButton.addEventListener('click', saveBib);
addButton.addEventListener('click', addPub);
removeButton.addEventListener('click', removePub);
upButton.addEventListener('click', navUp);
downButton.addEventListener('click', navDown);
exportButton.addEventListener('click', exportBib);

pubType.addEventListener('focusout', updateActivePub);
pubTitle.addEventListener('focusout', updateActivePub);
pubAuthors.addEventListener('focusout', updateActivePub);
pubBook.addEventListener('focusout', updateActivePub);
pubSchool.addEventListener('focusout', updateActivePub);
pubLocation.addEventListener('focusout', updateActivePub);
pubVolume.addEventListener('focusout', updateActivePub);
pubNumber.addEventListener('focusout', updateActivePub);
pubPages.addEventListener('focusout', updateActivePub);
pubMonth.addEventListener('focusout', updateActivePub);
pubYear.addEventListener('focusout', updateActivePub);
pubNotes.addEventListener('focusout', updateActivePub);
pubUrl.addEventListener('focusout', updateActivePub);
pubId.addEventListener('focusout', updateActivePub);
pubDoi.addEventListener('focusout', updateActivePub);
pubAbstract.addEventListener('focusout', updateActivePub);

ownerName.addEventListener('focusin', changeOwner);
ownerName.addEventListener('change', setOwner);
ownerName.addEventListener('focusout', checkOwner);

const template = [
  {
    label: 'File',
    submenu: [
      {label: 'New Bibliography', click() {newBib()}},
      {label: 'Save', click() {saveBib()}},
      {label: 'Save As...', click() {saveAsBib()}},
    ]
  },
  {
    label: 'View',
    submenu: [
      {role: 'resetzoom'},
      {role: 'zoomin'},
      {role: 'zoomout'},
      {type: 'separator'},
      {role: 'togglefullscreen'},
      {type: 'separator'},
      {role: 'toggledevtools'},
    ]
  },
  {
    role: 'window',
    submenu: [
      {role: 'minimize'},
      {role: 'close'}
    ]
  },
  {
    role: 'help',
    submenu: [
      {
        label: 'Learn More',
        click () { require('electron').shell.openExternal('https://electron.atom.io') }
      }
    ]
  }
]

if (process.platform === 'darwin') {
  template.unshift({
    label: app.getName(),
    submenu: [
      {role: 'about'},
      {type: 'separator'},
      {role: 'services', submenu: []},
      {type: 'separator'},
      {role: 'hide'},
      {role: 'hideothers'},
      {role: 'unhide'},
      {type: 'separator'},
      {role: 'quit'}
    ]
  })

  // Edit menu
  template[1].submenu.push(
    {type: 'separator'},
    {
      label: 'Speech',
      submenu: [
        {role: 'startspeaking'},
        {role: 'stopspeaking'}
      ]
    }
  )

  // Window menu
  template[3].submenu = [
    {role: 'close'},
    {role: 'minimize'},
    {role: 'zoom'},
    {type: 'separator'},
    {role: 'front'}
  ]
}

const menu = Menu.buildFromTemplate(template)
Menu.setApplicationMenu(menu)

function openBib() {
  fillExportMenu()
  dialog.showOpenDialog({
    filters: [{ name: 'xml', extensions: ['xml'] }],
    properties: [ 'openFile' ] }, function ( filename ) {
      if (filename==undefined) {
        console.log("No file selected.")
        return;
      }
      // Otherwise, load the file
      loadpubs(filename.toString());
      setVisible();
    }
  );
}

function setVisible() {
  pubNavGroup.style.visibility = 'visible';
  pubForm.style.visibility = 'visible';
}

function setLeftVisible() {
  pubNavGroup.style.visibility = 'visible';
}

function setRightVisible() {
  pubForm.style.visibility = 'visible';
}
function setRightInvisible() {
  pubForm.style.visibility = 'hidden';
}

function loadpubs(xmlFile) {
  // Read file
  fs.readFile(xmlFile, 'utf-8', (err, data) => {
    if(err){
        alert("An error ocurred reading the file :" + err.message);
        return;
    }
    filenameFooter.innerHTML = xmlFile;
    parser = new DOMParser();
    xmlData = parser.parseFromString(data,"text/xml");
    writePubs(xmlData);
  });
}

// Pub node list
var bibxml;
var activePub;
var activePubIndex;

function writePubs(xmlData) {
  bibxml = xmlData;
  // Go through xml dom and write list of pubs
  bibliography = bibxml.getElementsByTagName('bibliography')[0]
  owner = bibliography.getAttribute('owner');
  ownerName.value = owner + "'s Bibliography"
  pubs = bibliography.getElementsByTagName('publication');
  content = '';
  for (var i=0; i<pubs.length; i++) {
    id = pubs[i].id;
    title = pubs[i].getElementsByTagName('title')[0].innerHTML;
    active = '';
    if (i==0) {
      active = ' active';
    }
    content += '<span id="' + id + '" title="' + title;
    content += '" class="nav-group-item' + active + '">';
    content += '<span class="icon icon-doc-text-inv"></span>';
    content += '<span id="inner_' + id + '">' + id;
    content += '</span></span>';
  }
  publist.innerHTML = content;
  // Add event listeners
  for (i=0; i<pubs.length; i++) {
    var pub = pubs[i];
    var id = pubs[i].id;
    elt = document.getElementById(id);
    (function(pub, i) {
      elt.addEventListener('click', function(){
        fillEditPub(pub, i);
      }, false);
    })(pub, i)
  }
  // Fill in first pub
  activePub = pubs[0];
  fillEditPub(pubs[0], 0);
}

function fillEditPub(pub, index) {
  if (bibxml.getElementsByTagName('publication').length==0) {
    return;
  }
  // Inactivate currently selected pub
  document.getElementById(activePub.id).className = 'nav-group-item';
  // Activate new pub
  document.getElementById(pub.id).className = 'nav-group-item active';
  activePub = pub;
  activePubIndex = index;
  // Set form inputs
  pubType.value = pub.getElementsByTagName('type')[0].innerHTML;
  pubTitle.value = pub.getElementsByTagName('title')[0].innerHTML;
  //pubAuthors.value = pub.getElementsByTagName('authors')[0].innerHTML;
  authorElts = pub.getElementsByTagName('authors')[0].children;
  authorList = ''
  for (var i=0; i<authorElts.length; i++) {
    author = authorElts[i].innerHTML;
    authorList += author + ", ";
  }
  pubAuthors.value = authorList.substring(0,authorList.length-2);
  pubBook.value = pub.getElementsByTagName('book')[0].innerHTML;
  pubSchool.value = pub.getElementsByTagName('school')[0].innerHTML;
  pubLocation.value = pub.getElementsByTagName('location')[0].innerHTML;
  pubVolume.value = pub.getElementsByTagName('volume')[0].innerHTML;
  pubNumber.value = pub.getElementsByTagName('number')[0].innerHTML;
  pubPages.value = pub.getElementsByTagName('pages')[0].innerHTML;
  pubMonth.value = pub.getElementsByTagName('month')[0].innerHTML;
  pubYear.value = pub.getElementsByTagName('year')[0].innerHTML;
  pubNotes.value = pub.getElementsByTagName('notes')[0].innerHTML;
  pubUrl.value = pub.getElementsByTagName('url')[0].innerHTML;
  pubId.value = pub.id;
  pubDoi.value = pub.getElementsByTagName('doi')[0].innerHTML;
  pubAbstract.value = pub.getElementsByTagName('abstract')[0].innerHTML;
}

function updateActivePub() {
  pubTag = this.id.substring(4,this.id.length);
  newValue = this.value;
  if (pubTag == 'authors') {
    // Parse author names
    authorList = this.value.split(',');
    authorsNode = activePub.getElementsByTagName('authors')[0];
    authorsNode.innerHTML = '';
    for (i=0; i<authorList.length; i++) {
      authorNode = bibxml.createElement('author');
      authorNode.innerHTML = authorList[i].trim();
      authorsNode.appendChild(authorNode);
    }
  }
  else if (pubTag == 'id') {
    document.getElementById(activePub.id).id = this.value;
    document.getElementById('inner_'+activePub.id).id = 'inner_'+this.value;
    activePub.id = this.value;
    document.getElementById('inner_'+activePub.id).innerHTML = this.value;
  }
  else {
    bibxml.getElementById(activePub.id).getElementsByTagName(pubTag)[0].innerHTML = this.value;
  }
}

function saveBib() {
  if (bibxml==null) {
    return;
  }
  filename = filenameFooter.innerHTML;
  if (filename.length>0) {
    xmlStr = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
    xmlStr += new XMLSerializer().serializeToString(bibxml);
    fs.writeFile(filename, xmlStr, (err) => {
      if (err) {
          alert("An error ocurred writing the file" + err.message);
          console.log(err);
          return;
      }
    });
  }
  else {
    saveAsBib();
  }
}

function saveAsBib() {
  dialog.showSaveDialog({
    filters: [{ name: 'xml', extensions: ['xml'] }],
    properties: [ 'openFile' ] }, function ( filename ) {
      if (filename==undefined) {
        console.log("No file selected.")
        return;
      }
      // Otherwise, save the file
      filenameFooter.innerHTML = filename;
      saveBib();
    }
  );
}

function navUp() {
  if (bibxml==null) {
    return;
  }
  if (activePubIndex>0) {
    fillEditPub(bibliography.getElementsByTagName('publication')[activePubIndex-1], activePubIndex-1)
  }
}
function navDown() {
  if (bibxml==null) {
    return;
  }
  if (activePubIndex+1<bibliography.getElementsByTagName('publication').length) {
    fillEditPub(bibliography.getElementsByTagName('publication')[activePubIndex+1], activePubIndex+1)
  }
}

var newCount = 0;

function addPub() {
  if (bibxml==null) {
    return;
  }
  // Create pub node
  pub = bibxml.createElement('publication');
  // Create children
  pub.appendChild(bibxml.createElement('type'));
  pub.appendChild(bibxml.createElement('title'));
  pub.appendChild(bibxml.createElement('authors'));
  pub.appendChild(bibxml.createElement('book'));
  pub.appendChild(bibxml.createElement('school'));
  pub.appendChild(bibxml.createElement('location'));
  pub.appendChild(bibxml.createElement('volume'));
  pub.appendChild(bibxml.createElement('number'));
  pub.appendChild(bibxml.createElement('pages'));
  pub.appendChild(bibxml.createElement('month'));
  pub.appendChild(bibxml.createElement('year'));
  pub.appendChild(bibxml.createElement('notes'));
  pub.appendChild(bibxml.createElement('url'));
  pub.appendChild(bibxml.createElement('doi'));
  pub.appendChild(bibxml.createElement('abstract'));
  // Fill in values
  pub.getElementsByTagName('type')[0].innerHTML = 'Conference';
  pub.getElementsByTagName('title')[0].innerHTML = 'My Title';
  pub.getElementsByTagName('authors')[0].appendChild(bibxml.createElement('author'));
  pub.getElementsByTagName('authors')[0].children[0].innerHTML = 'My Authors';
  pub.getElementsByTagName('book')[0].innerHTML = '';
  pub.getElementsByTagName('school')[0].innerHTML = '';
  pub.getElementsByTagName('location')[0].innerHTML = '';
  pub.getElementsByTagName('volume')[0].innerHTML = '';
  pub.getElementsByTagName('number')[0].innerHTML = '';
  pub.getElementsByTagName('pages')[0].innerHTML = '';
  pub.getElementsByTagName('month')[0].innerHTML = '';
  pub.getElementsByTagName('year')[0].innerHTML = '';
  pub.getElementsByTagName('notes')[0].innerHTML = '';
  pub.getElementsByTagName('url')[0].innerHTML = '';
  pub.setAttribute('id', 'NewPublication' + newCount++);
  pub.getElementsByTagName('doi')[0].innerHTML = '';
  pub.getElementsByTagName('abstract')[0].innerHTML = '';
  // Insert into bibxml
  firstPub = bibxml.getElementsByTagName('publication')[0];
  bibxml.getElementsByTagName('bibliography')[0].insertBefore(pub, firstPub);
  writePubs(bibxml);
  if (bibxml.getElementsByTagName('publication').length>0) {
    setRightVisible();
  }
}

function removePub() {
  if (bibxml==null) {
    return;
  }
  if (bibxml.getElementsByTagName('publication').length==0) {
    return;
  }
  dialog.showMessageBox({
    type: 'question',
    message: 'Delete ' + activePub.id + '? This cannot be undone.',
    buttons: ['OK', 'Cancel'],
    title: 'Delete Publication?' }, function (response) {
      if (response==0) {
        deletePub(activePub, activePubIndex);
        if (bibxml.getElementsByTagName('publication').length==0) {
          setRightInvisible();
        }
      }
    }
  );
}

function deletePub(pub, index) {
  // Delete from xml
  bibxml.documentElement.removeChild(pub);
  writePubs(bibxml);
}

function newBib() {
  fillExportMenu()
  bibxml = document.implementation.createDocument(null, 'bibliography', null);
  bibxml.documentElement.setAttribute('owner', 'A. Author');
  setLeftVisible();
  setRightInvisible();
  writePubs(bibxml);
}

function changeOwner() {
  owner = bibxml.getElementsByTagName('bibliography')[0].getAttribute('owner');
  ownerName.value = owner;
}

function setOwner() {
  bibxml.getElementsByTagName('bibliography')[0].setAttribute('owner', ownerName.value);
  ownerName.value = ownerName.value + "'s Bibliography";
}

function checkOwner() {
  if (ownerName.value.substring(ownerName.value.length-12, ownerName.value.length)!='Bibliography') {
    ownerName.value = ownerName.value + "'s Bibliography";
  }
}

function exportBib() {
  dialog.showSaveDialog({
    filters: [],
    properties: [ 'openFile' ] }, function ( filename ) {
      if (filename==undefined) {
        console.log("No file selected.")
        return;
      }
      // Otherwise, export
      xsltFilename = './app/xml/' + exportType.value + '.xslt';
      // Read file
      fs.readFile(xsltFilename, 'utf-8', (err, data) => {
        if(err){
          console.log(data)
            alert("An error ocurred reading the file :" + err.message);
            return;
        }
        parser = new DOMParser();
        xsltData = parser.parseFromString(data,"text/xml");
        xsltProcessor = new XSLTProcessor();
        xsltProcessor.importStylesheet(xsltData.documentElement);
        resultDocument = xsltProcessor.transformToDocument(bibxml);
        method = xsltData.getElementsByTagName("output")[0].getAttribute('method')
        var data;
        if (method == 'text') {
          data = resultDocument.documentElement.textContent;
        }
        else {
          data = '<html>' + resultDocument.documentElement.innerHTML + '</html>';
        }
        fs.writeFile(filename, data, (err) => {
          if (err) {
              alert("An error ocurred writing the file" + err.message);
              console.log(err);
              return;
          }
        });
      });
    }
  );
}

function fillExportMenu() {
  while (exportType.options.length > 0) {
    exportType.remove(exportType.options.length - 1);
  }
  // Fill in export options
  var files = fs.readdirSync('./app/xml/')
  for (i=0; i<files.length; i++) {
    if (files[i].length>5) {
      option = files[i].substring(0,files[i].length-5);
      extension = files[i].substring(files[i].length-5,files[i].length);
      if (option.substring(0,2) == 'To' && extension == '.xslt') {
        var opt = document.createElement('option');
        opt.text = option;
        exportType.add(opt, null);
      }
    }
  }
}
