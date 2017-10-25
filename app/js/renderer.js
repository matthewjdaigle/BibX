var dialog = require('electron').remote.dialog;
var fs = require('fs');

// Get various elements
var openButton = document.getElementById('openButton');
var publications = document.getElementById('publications')
var editpub = document.getElementById('edit-pub');
var publist = document.getElementById('pub-list');
var ownerName = document.getElementById('owner-name');
var filenameFooter = document.getElementById('filename-footer');

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
var pubAbstract = document.getElementById('pub-abstract');

openButton.addEventListener('click', openBib);

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
    content += id;
    content += '</span>';
  }
  publist.innerHTML = content;
  // Add event listeners
  for (var i=0; i<pubs.length; i++) {
    var pub = pubs[i];
    var id = pubs[i].id;
    elt = document.getElementById(id);
    (function(pub) {
      elt.addEventListener('click', function(){
        fillEditPub(pub);
      }, false);
    })(pub)
  }
  // Fill in first pub
  activePub = pubs[0];
  fillEditPub(pubs[0]);
}

function fillEditPub(pub) {
  // Inactivate currently selected pub
  document.getElementById(activePub.id).className = 'nav-group-item';
  // Activate new pub
  document.getElementById(pub.id).className = 'nav-group-item active';
  activePub = pub;
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
  pubAbstract.value = pub.getElementsByTagName('abstract')[0].innerHTML;
}

function updateActivePub() {
  pubTag = this.id.substring(4,this.id.length);
  bibxml.getElementById(activePub.id).getElementsByTagName(pubTag)[0].innerHTML = this.value;
}
