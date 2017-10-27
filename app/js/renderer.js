var dialog = require('electron').remote.dialog;
var fs = require('fs');

// Get button elements
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
openButton.addEventListener('click', openBib);
saveButton.addEventListener('click', saveBib);
addButton.addEventListener('click', addPub);
removeButton.addEventListener('click', removePub);
upButton.addEventListener('click', navUp);
downButton.addEventListener('click', navDown);
//exportButton.addEventListener('click', exportBib);

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

function openBib() {
  dialog.showOpenDialog({
    filters: [{ name: 'xml', extensions: ['xml'] }],
    properties: [ 'openFile' ] }, function ( filename ) {
      if (filename==undefined) {
        console.log("No file selected.")
        return;
      }
      // Otherwise, load the file
      loadpubs(filename.toString());
    }
  );
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
  ownerName.innerHTML = owner + "'s Bibliography"
  pubs = bibliography.getElementsByTagName('publication');
  content = '';
  for (var i=0; i<pubs.length; i++) {
    id = pubs[i].id;
    title = pubs[i].getElementsByTagName('title')[0].innerHTML;
    active = '';
    if (i==0) {
      active = ' active';
    }
    content += '<span id="' + id + '" class="nav-group-item' + active + '">';
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
    console.log(activePub);
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
  filename = filenameFooter.innerHTML;
  if (filename.length>0) {
    fs.writeFile(filename, new XMLSerializer().serializeToString(bibxml), (err) => {
      if (err) {
          alert("An error ocurred writing the file" + err.message);
          console.log(err);
          return;
      }
    });
  }
}

function navUp() {
  if (activePubIndex>0) {
    fillEditPub(bibliography.getElementsByTagName('publication')[activePubIndex-1], activePubIndex-1)
  }
}
function navDown() {
  if (activePubIndex+1<bibliography.getElementsByTagName('publication').length) {
    fillEditPub(bibliography.getElementsByTagName('publication')[activePubIndex+1], activePubIndex+1)
  }
}

var newCount = 0;

function addPub() {
  // Create pub node
  pub = activePub.cloneNode(true);
  pub.getElementsByTagName('type')[0].innerHTML = 'Conference';
  pub.getElementsByTagName('title')[0].innerHTML = 'My Title';
  pub.getElementsByTagName('authors')[0] = pub.getElementsByTagName('authors')[0].children[0];
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
  pub.id = 'NewPublication' + newCount++;
  pub.getElementsByTagName('doi')[0].innerHTML = '';
  pub.getElementsByTagName('abstract')[0].innerHTML = '';
  // Insert into bibxml
  firstPub = bibxml.getElementsByTagName('publication')[0]
  bibxml.getElementsByTagName('bibliography')[0].insertBefore(pub, firstPub);
  writePubs(bibxml);
}

function removePub() {
  dialog.showMessageBox({
    type: 'question',
    message: 'Delete ' + activePub.id + '? This cannot be undone.',
    buttons: ['OK', 'Cancel'],
    title: 'Delete Publication?' }, function () {
      deletePub(activePub, activePubIndex);
    }
  );
}

function deletePub(pub, index) {
  // Delete from xml
  bibxml.documentElement.removeChild(pub);
  writePubs(bibxml);
}
