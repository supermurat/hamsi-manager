#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, stat
import os
reload(sys)
sys.setdefaultencoding("utf-8")

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *






myHttp = QHttp()
myHttp.setHost("mopened.com")
print myHttp.post("ForMyProjects/MailList.php", "name=murat")

op = QUrlOperator("http://doc.trolltech.com")
op.get("qhttp.html")

print myHttp.readAll()





def addToMailList(self):
    from urllib import unquote, quote
    self.myHttp = MHttp()
    self.myHttp.setHost("mopened.com")
    header = MHttpRequestHeader("POST", "/ForMyProjects/MailList.php")
    header.setValue("Host","mopened.com")
    header.setContentType("application/x-www-form-urlencoded")
    self.myHttp.request(header, 
        u"mail=" + unquote(str(self.leEMail.text())) + 
        u"&message=" + unquote(str(MApplication.translate("Install", "%s added to mail list."))))
    self.connect(self.myHttp,SIGNAL("done(bool)"), self.addedToMailList)
    
def addedToMailList(self, _message):
    import Dialogs
    Dialogs.show(self.myHttp.readAll())



#
#
#QNetworkAccessManager *manager = new QNetworkAccessManager;
#connect(manager, SIGNAL(finished(QNetworkReply*)),
#        this, SLOT(replyFinished(QNetworkReply*)));
#// Define replyFinished slot to handle the reply.
#
#...
#
#QNetworkRequest request;
#QUrl tmpUrl;
#request.setUrl(QUrl("http://localhost/test.php";));
#request.setHeader(QNetworkRequest::ContentTypeHeader,
#                  "application/x-www-form-urlencoded");
#
#tmpUrl.addQueryItem("field1", "value1");
#tmpUrl.addQueryItem("field2", "value2");
#...
#
#QNetworkReply *reply = manager->post(request, tmpUrl.encodedQuery());
#
#
#QString poststr; 
#//login olmak için gereken post string'i 
#    poststr.append("LoggingOn=1&Sicil="); 
#    poststr.append(OgrNo); 
#    poststr.append("&Sifre="); 
#    poststr.append(Sifre); 
#    poststr.append("&Ara=Listele&AnketOnay=0&Donem="); 
#    poststr.append(Donem.toString()); 
#    //yukarıda post-string oluşturuluyor, 
#    QNetworkRequest qnreq(urlNot); 
#    //bu satırla urlNot değişkenindeki url ile bir ağ isteği oluşturuyoruz 
#    qnreply=qnam->post(qnreq,poststr.toUtf8()); 
#    //yukarıda post işlemi gerçekleştiriliyor 
#connect(qnreply,SIGNAL(downloadProgress(qint64,qint64)),this,SIGNAL(sinyal( qint64,qint64))); 
#    //bu satırda progress bar'a html'in indirme işlemini göndertti
#



sys.exit()

print os.path.isfile("/usr/bin/OrganizasyonizM")

import re
_stringFull = "Org \"/retertre\" aniza \"/syon\" izM"
pattern = re.compile(unicode("\"/.*\""))
#_stringFull = re.sub(pattern,unicode(_replaceStrings[filterNo]), unicode(_stringFull))
#_stringFull.replace(_stringLink, "<a href='%s' target='_blank'>%s</a>" % (_stringLink, _stringLink))

m = re.search("\"/.*(?:[a-zA-Z])\"", _stringFull)

print dir(m)
print m.group()

#import InputOutputs
#print InputOutputs.checkExtension("murat.de.mir", "")

sys.exit()

print os.stat("/home/mxd/.HamsiApps/HamsiManager/logs.txt")[stat.ST_SIZE]/1024




print os.sep

sys.exit()
#print sys.getfilesystemencoding().lower()
#print sys.getdefaultencoding().lower()
#print "dffffffgsdfgdf"
#sys.exit()
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

print KMessageBox.questionYesNoCancel(None, 
                            "jjjjjjjjjjjjjjjjjjjjjjjjjjjjj", 
                            "kkkkkkkkkkkkkkkkkkkkkkkkk")


sys.exit()

for x in KMimeType.mimeType(u"text/plain").patterns():
    print x
print "-------"
for x in KMimeType.mimeType(u"text/plain").parentMimeTypes():
    print x
print "-------"
c, y = KMimeType.findByFileContent(u"/home/mxd/Belgeler/Ekran Görüntüleri/1.png")
print c
print c.is_(u"text/plain")
c.userSpecifiedIconName()
for x in c.parentMimeTypes():
    print x
print "-------"
filePath=u"/home/mxd/Belgeler/Ekran Görüntüleri/1.png"
c, y = KMimeType.findByPath(filePath)
print c
print c.comment(KUrl(filePath))
print c.iconName(KUrl(filePath))
print c.is_(u"text/plain")
c.userSpecifiedIconName()
for x in c.patterns():
    print x
print KMimeType.iconNameForUrl(KUrl(filePath))
print "-------"
    
sys.exit()

from encodings import aliases
for k, v in aliases.aliases.iteritems():
    try:
        print "code :" + v + "---" + str(["�"]) + "---"
    except:pass

sys.exit()






#>>> unicode('\x80abc', errors='replace')
#u'\ufffdabc'
#>>> unicode('\x80abc', errors='ignore')
#u'abc'









#                testing PyKDE4
#                from PyQt4.QtCore import QFile
#                a = QFile.copy(_oldPath, _newPath)
#                Dialogs.show("", a)
                        
#                        answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"),
#                                str(translate("InputOutputs", "'%s' : there already exists a folder with the same name.<br>'%s' Add this directory contents to the current directory?<br>"+
#                                              "İf source files already exist in the destination directory,<br>source files will be overwritten to destination files.")) % (Organizer.showWithIncorrectChars(_newPath), Organizer.showWithIncorrectChars(_newPath)), 
#                                translate("InputOutputs", "&Yes"), 
#                                translate("InputOutputs", "&No"))
#                        if answer==translate("InputOutputs", "&Yes"):
#                            appendingDirectories.append(getDirName(_newPath))
#                            return getDirName(_newPath)



#    def moveToDir(_oldPath,_newPath):
#        _oldPath, _newPath = str(_oldPath), str(_newPath)
#        try:
#            makeDirs(getDirName(_newPath))
#            isChange=True
#            appendingDirectories.append(getDirName(_newPath))
#        except OSError ,(error):
#            if str(error)[:10]=="[Errno 13]":
#                isChange=False
#                Dialogs.show(translate("InputOutputs", "Access Denied"),
#                        str(translate("InputOutputs", "'%s' : you do not have the necessary permissions to create this folder.<br>Please check your access controls and retry.")) % (Organizer.showWithIncorrectChars(getDirName(_newPath))))
#            else:
#                isChange = True
#                if isDir(getDirName(_newPath)):   
#                    isChange=False
#                    isAllowed=False
#                    for dizin in appendingDirectories:
#                        if getDirName(_newPath)==dizin:
#                            isAllowed=True
#                    if isAllowed==False: 
#                        answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"), 
#                                str(translate("InputOutputs", "'%s' : there already exists a folder with the same name.<br>Add your files to the current folder?")) % (Organizer.showWithIncorrectChars(getDirName(_newPath))), 
#                                translate("InputOutputs", "&Yes"), 
#                                translate("InputOutputs", "&No"))
#                        if answer==translate("InputOutputs", "&Yes"):
#                            appendingDirectories.append(getDirName(_newPath))
#                            isChange=True
#                    else:
#                        isChange=True
#        if isChange==True:
#            moveOrChange(_oldPath,_newPath)
#            return True
#        return False






yazimiz = "Şyyyyyyyyyyyyy"
import re
pattern = re.compile(u"ş", re.I | re.U)
yazimiz = re.sub(pattern,"kkk", yazimiz)
print yazimiz
print u"ş".upper()
print u"Ş".lower()


sys.exit()
import select
import subprocess
class MPlayer(object):
    """ A class to access a slave mplayer process
    you may want to use command(name, args*) directly
    or call populate() to access functions (and minimal doc).

    Exemples:
        mp.command('loadfile', '/desktop/funny.mp3')
        mp.command('pause')
        mp.command('quit')

    Note:
        After a .populate() call, you can access an higher level interface:
            mp.loadfile('/desktop/funny.mp3')
            mp.pause()
            mp.quit()

        Beyond syntax, advantages are:
            - completion
            - minimal documentation
            - minimal return type parsing
    """

    exe_name = 'mplayer' if os.sep == '/' else 'mplayer.exe'

    def __init__(self):
        self._mplayer = subprocess.Popen(
                [self.exe_name, '-slave', '-quiet', '-idle'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=-1)
        self._readlines()

    def _readlines(self):
        ret = []
        while any(select.select([self._mplayer.stdout.fileno()], [], [], 0.6)):
            ret.append( self._mplayer.stdout.readline() )
        return ret

    def command(self, name, *args):
        """ Very basic interface [see populate()]
        Sends command 'name' to process, with given args
        """
        cmd = '%s%s%s\n'%(name,
                ' ' if args else '',
                ' '.join(repr(a) for a in args)
                )
        self._mplayer.stdin.write(cmd)
        if name == 'quit':
            return
        return self._readlines()

    @classmethod
    def populate(kls):
        """ Populates this class by introspecting mplayer executable """
        mplayer = subprocess.Popen([kls.exe_name, '-input', 'cmdlist'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        def args_pprint(txt):
            lc = txt.lower()
            if lc[0] == '[':
                return '%s=None'%lc[1:-1]
            return lc

        while True:
            line = mplayer.stdout.readline()
            if not line:
                break
            if line[0].isupper():
                continue
            args = line.split()
            cmd_name = args.pop(0)
            arguments = ', '.join([args_pprint(a) for a in args])
            func_str = '''def _populated_fn(self, *args):
            """%(doc)s"""
            if not (%(minargc)d <= len(args) <= %(argc)d):
                raise TypeError('%(name)s takes %(argc)d arguments (%%d given)'%%len(args))
            ret = self.command('%(name)s', *args)
            if not ret:
                return None
            if ret[0].startswith('ANS'):
                val = ret[0].split('=', 1)[1].rstrip()
                try:
                    return eval(val)
                except:
                    return val
            return ret'''%dict(
                    doc = '%s(%s)'%(cmd_name, arguments),
                    minargc = len([a for a in args if a[0] != '[']),
                    argc = len(args),
                    name = cmd_name,
                    )
            exec(func_str)

            setattr(MPlayer, cmd_name, _populated_fn)


    
#MPlayer.populate()
#mp = MPlayer()
#import readline
#readline.parse_and_bind('tab: complete')
#import rlcompleter
#mp.command('loadfile', '/home/mxd/Belgeler/Mp3 Dene/Pinar Aylin - Sebebini Sorma.mp3')
##mp.command('pause')
##mp.command('quit')









#import sys
#import os
#sys.path.insert(0,sys.path[1]+"/eyeD3")
#import eyeD3
#
#
#tag = eyeD3.Tag()
#tag.link("/home/mxd/Belgeler/Mp3 Dene/Yeni Dizin/tty.üçç")
#tag.update(0x24)

#muzik = eyeD3.Mp3AudioFile("/home/mxd/Belgeler/Mp3 Dene/Yeni Dizin/tty.üçç")





#import sys, traceback
#import os
#if sys.path[0]=="":
#    sys.path.insert(0, sys.path[1])
#sys.path.insert(0,sys.path[0]+"/AramaMotorlari")
#
#from os import listdir,path,mkdir,removedirs,makedirs, rmdir, remove
#listem = [".directory", "(a:[-a-z0-9])"]
#dizim = [".directory", "ahmetdirm*", "yokkkartık"]
#gelen = "akrepmd@.directry.com"
#

#
#
#from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ReleaseFilter, TrackFilter
#from musicbrainz2 import webservice, model, utils
#
#
#
#
#
#for result in Query().getTracks(TrackFilter(query="Kimdi")):
#    print result.track.artist.name
#    for bilgi in result.track.releases:
#        print bilgi.title















import re
def makerelib():
    lib = {}
    lib["email"] = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)",re.IGNORECASE)
    lib["postcode"] = re.compile("[a-z]{1,2}\d{1,2}[a-z]?\s*\d[a-z]{2}",re.IGNORECASE)
    lib["zipcode"] = re.compile("\d{5}(?:[-\s]\d{4})?")
    lib["ukdate"] = re.compile("[0123]?\d[-/\s\.](?:[01]\d|[a-z]{3,})[-/\s\.](?:\d{2})?\d{2}",re.IGNORECASE)
    lib["time"] = re.compile("\d{1,2}:\d{1,2}(?:\s*[aApP]\.?[mM]\.?)?")
    lib["fullurl"] = re.compile("https?://[-a-z0-9\.]{4,}(?::\d+)?/[^#?]+(?:#\S+)?",re.IGNORECASE)
    lib["visacard"] = re.compile("4\d{3}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}")
    lib["mastercard"] = re.compile("5[1-5]\d{2}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}")
    lib["phone"] = re.compile("0[-\d\s]{10,}")
    lib["ninumber"] = re.compile("[a-z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[a-z]",re.IGNORECASE)
    lib["isbn"] = re.compile("(?:[\d]-?){9}[\dxX]")
    for x, kriter in enumerate(listem):
        lib[str(x)] = re.compile(kriter)
    return lib

tests = makerelib()










#print vars()
#print locals()
#print globals()











#def sanatcininAlbumleri(_sanatciId):
#    """Belirtilen sanatçı IDsinin tüm albümlerini geri döndürür.
#    Dönenler[x][0]:Id               Dönenler[x][1]:Başlık
#    Dönenler[x][2]:Asin             Dönenler[x][3]:Text
#    Dönenler[x][4]:Tarz"""
#    donenler = []
#    q = Query()
#    inc = webservice.ArtistIncludes(releases=(model.Release.TYPE_OFFICIAL, model.Release.TYPE_ALBUM),tags=True)
#    artist = q.getArtistById(_sanatciId, inc)
#    for release in artist.getReleases():
#        donenler.append([release.id, release.title, release.asin, (release.textLanguage, '/', release.textScript), release.types])
#    return donenler
#
##print sanatcininAlbumleri("http://musicbrainz.org/artist/4ec2451d-ed0c-4273-b683-4c1312df25fd")
##print sanatcininAlbumleri("http://musicbrainz.org/artist/a6a70a9c-a17a-46cd-8a12-ba3fe69f1036")
##print sanatcininAlbumleri("http://musicbrainz.org/artist/a066220a-cc79-45e7-9f31-4c7d1613c2b4")
#a="http://musicbrainz.org/artist/4ec2451d-ed0c-4273-b683-4c1312df25fd"
#b="http://musicbrainz.org/artist/a6a70a9c-a17a-46cd-8a12-ba3fe69f1036"
#c="http://musicbrainz.org/artist/a066220a-cc79-45e7-9f31-4c7d1613c2b4"
#
#
#things = 0
#for test in tests.keys():
#    matches = tests[test].findall(gelen)
#    if matches:
#        print "Matched",test,"with",matches
#        things += 1
#if not things: print "nothing"









#print vars()
#print locals()
#print globals()




#for name in dir():
#    if str(str(name).strip())[0]!="{":
#        exec("print "+str(name))

#donenler = []
#q = Query()
#inc = webservice.ArtistIncludes(releases=(model.Release.TYPE_ALBUM, model.Release.TYPE_OFFICIAL))
#artist = q.getArtistById(b, inc)
#for release in artist.getReleases():
#    donenler.append([release.id, release.title, release.asin, (release.textLanguage, '/', release.textScript), release.types])
#print donenler


#

#print 
#from musicbrainz2.webservice import Query, ArtistFilter, ReleaseFilter, WebServiceError, TrackFilter
#
#try:
#    print 2/0
#except:
#    cla, hata, trbk = sys.exc_info()
#    hata_ismi = cla.__name__
#    try:
#        excArgs = hata.__dict__["args"]
#    except KeyError:
#        excArgs = "<no args>"
#    hata_detayi = traceback.format_tb(trbk, 5)
#    hata_detaylari = str(hata_ismi)+"----"+str(hata)+"----"+str(excArgs)+"----"+str(hata_detayi[0])
#
#    print hata_detaylari
#    print "......................................"










#q = Query()
#f = TrackFilter(query="kuzu kuzu")
#releases = q.getTracks(f)
#for bilgi in releases:
#    print "score        :", bilgi.score
#    print "Artist Name  :", bilgi.track.artist.name
#    print "Id        :", bilgi.track.id





#import os, sys
#if sys.path[0]=="":
#    sys.path.insert(0, sys.path[1])
#sys.path.insert(0,sys.path[0]+"/AramaMotorlari")
#
#from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ReleaseFilter, TrackFilter
#from musicbrainz2 import webservice, model, utils
#
#q = Query()
#inc = webservice.ArtistIncludes(tags=True)
#artist = q.getArtistById("d138302b-4f57-4d1d-83e3-47f95cb51774", inc)
#print artist.id, artist.name, artist.sortName


#donenler=[]
#q = Query()
#inc = webservice.ArtistIncludes(releases=(model.Release.TYPE_OFFICIAL, model.Release.TYPE_ALBUM))
#artist = q.getArtistById("d138302b-4f57-4d1d-83e3-47f95cb51774", inc)
#for release in artist.getReleases():
#    donenler.append([release.title, release.types])
#print donenler




#q = Query()
#f = ReleaseFilter(query="karma", releaseTypes=ReleaseFilter.Album)
#releases = q.getReleases(f)
#for bilgi in releases:
##    print "score        :", bilgi.score
#    print "Artist Name  :", bilgi.release.artist.name
#    print "Id        :", bilgi.release.id
#    print "Title     :", bilgi.release.title
##    print "ASIN      :", bilgi.release.asin
##    print "Text      :", bilgi.release.textLanguage, '/', bilgi.release.textScript
#    print "Types     :", bilgi.release.types
##    for track in bilgi.release.tracks:
##        print "  Id        :", track.id
##        print "  Title     :", track.title
##        print "  Duration  :", track.duration
#    print "-----------------"










#def sarkilari(_albumid):
#    import sys
#    import logging
#    import musicbrainz2.webservice as ws
#    import musicbrainz2.utils as u
#    q = ws.Query()
#    try:
#        inc = ws.ReleaseIncludes(artist=True, releaseEvents=True, labels=True,
#                discs=True, tracks=True)
#        release = q.getReleaseById(_albumid, inc)
#    except ws.WebServiceError, e:
#        print 'Error:', e
#        sys.exit(1)
#    print "Id          :", release.id
#    print "Title       :", release.title
#    print "ASIN        :", release.asin
#    print "Lang/Script :", release.textLanguage, '/', release.textScript
#
#    if release.artist:
#        print
#        print "Artist:"
#        print "  Id        :", release.artist.id
#        print "  Name      :", release.artist.name
#        print "  SortName  :", release.artist.sortName
#
#    if len(release.releaseEvents) > 0:
#        print
#        print "Released (earliest: %s):" % release.getEarliestReleaseDate()
#
#    for event in release.releaseEvents:
#        print "  %s %s" % (u.getCountryName(event.country), event.date),
#
#        if event.catalogNumber:
#            print '#' + event.catalogNumber,
#
#        if event.barcode:
#            print 'EAN=' + event.barcode,
#
#        if event.label:
#            print '(' + event.label.name + ')',
#
#        print
#
#
#    if len(release.discs) > 0:
#        print
#        print "Discs:"
#
#    for disc in release.discs:
#        print "  DiscId: %s (%d sectors)" % (disc.id, disc.sectors)
#
#
#    if len(release.tracks) > 0:
#        print
#        print "Tracks:"
#
#    for track in release.tracks:
#        print "  Id        :", track.id
#        print "  Title     :", track.title
#        print "  Duration  :", track.duration
#        print
#
#
#def albumleri(_artistid):
#    import musicbrainz2.webservice as ws
#    import musicbrainz2.model as m
#    try:
#        inc = ws.ArtistIncludes(
#            releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM),
#            tags=True)
#        artist = q.getArtistById(_artistid, inc)
#    except ws.WebServiceError, e:
#        print 'Error:', e
#        sys.exit(1)
#    print "Id         :", artist.id
#    print "Name       :", artist.name
#    print "SortName   :", artist.sortName
#    print "UniqueName :", artist.getUniqueName()
#    print "Type       :", artist.type
#    print "BeginDate  :", artist.beginDate
#    print "EndDate    :", artist.endDate
#    print "Tags       :", ', '.join(t.value for t in artist.tags)
#    print
#
#    if len(artist.getReleases()) == 0:
#        print "No releases found."
#    else:
#        print "Releases:"
#
#    for release in artist.getReleases():
#        print
#        print "Id        :", release.id
#        print "Title     :", release.title
#        print "ASIN      :", release.asin
#        print "Text      :", release.textLanguage, '/', release.textScript
#        print "Types     :", release.types
#        sarkilari(release.id)
#
#
#
#for result in artistResults:
#    artist = result.artist
#    print "Score     :", result.score
#    print "Id        :", artist.id
#    print "Name      :", artist.name
#    print "Sort Name :", artist.sortName
#    print "Şarkıları :"
#    albumleri(artist.id)



























#
#import sys
#import os
#reload(sys)
#sys.setdefaultencoding("utf-8")
#
#file = "/home/mxd/Belgeler/Mp3 Dene/Heyy - Unuttum1.mp3"
#import sys
#
#from PyQt4.QtGui import QApplication, QMainWindow, QDirModel, QColumnView
#from PyQt4.QtGui import QFrame
#from PyQt4.QtCore import SIGNAL
#from PyKDE4.phonon import Phonon
#
#class MainWindow(QMainWindow):
#
#    m_model = QDirModel()
#
#    def __init__(self):
#        QMainWindow.__init__(self)
#        self.m_fileView = QColumnView(self)
#        self.m_media = None
#
#        self.setCentralWidget(self.m_fileView)
#        self.m_fileView.setModel(self.m_model)
#        self.m_fileView.setFrameStyle(QFrame.NoFrame)
#
#        self.connect(self.m_fileView,
#            SIGNAL("updatePreviewWidget(const QModelIndex &)"), self.play)
#
#    def play(self, index):
#        self.delayedInit()
#        #self.m_media.setCurrentSource(self.m_model.filePath(index))
#        self.m_media.setCurrentSource(
#            Phonon.MediaSource(self.m_model.filePath(index)))
#        self.m_media.play()
#
#    def delayedInit(self):
#        if not self.m_media:
#            self.m_media = Phonon.MediaObject()
#            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
#            Phonon.createPath(self.m_media, audioOutput)
#
#def main():
#    app = QApplication(sys.argv)
#    QApplication.setApplicationName("Phonon Tutorial 2 (Python)")
#    mw = MainWindow()
#    mw.show()
#    sys.exit(app.exec_())
#
#if __name__ == '__main__':
#    main()
