
Importer.loadQtBinding("qt.core");
Importer.loadQtBinding( "qt.gui" );
Importer.loadQtBinding( "qt.uitools" );

const lang = QLocale.system().name();
var translator = new QTranslator();
translator.load("HamsiManagerInTheAmarok_"+lang, Amarok.Info.scriptPath()+"/languages");
QCoreApplication.installTranslator(translator);

function translate(context,st){
    return QCoreApplication.translate(context,st);
}

function OrganizeWithHamsiManager(){
    var fileName = Amarok.Playlist.filenames()[Amarok.Playlist.activeIndex()];
    if (fileName == "") {
        Amarok.alert(translate("HamsiManagerInTheAmarok", "Please select a file in playlist."));
    }
    else {
        try
        {
            var sets = new QSettings(QDir.homePath().toString()+"/.HamsiApps/universalSettings.ini",QSettings.IniFormat);
            var HamsiManagerPath = sets.value("HamsiManagerPath").toString();
            var mySets = new QSettings(QDir.homePath().toString()+"/.HamsiApps/HamsiManager/mySettings.ini",QSettings.IniFormat);
            var directoryInfo = new QFileInfo(fileName);
            var directoryPath = directoryInfo.dir().path();
            mySets.setValue("lastDirectory", directoryPath);
            mySets.setValue("tableType", "2");
            var params = new Array();
            params[0] = HamsiManagerPath;
            var HamsiManagerInTheAmarok = new QProcess(Amarok);
            HamsiManagerInTheAmarok.start("python", params);
        }
        catch(err)
        {
            Amarok.alert(translate("HamsiManagerInTheAmarok", "Please once run Hamsi Manager.Hamsi Manager if is not installed on your system, please download from http://hamsiapps.com/HamsiManager and install it."));
        }
    }
}

if ( Amarok.Window.addToolsMenu("HamsiManagerInTheAmarokId", translate("HamsiManagerInTheAmarok", "Organize With Hamsi Manager"), Amarok.Info.scriptPath() + "/M.png") ){
        var HamsiManagerInTheAmarokButton = Amarok.Window.ToolsMenu.HamsiManagerInTheAmarokId;
        HamsiManagerInTheAmarokButton['triggered()'].connect(OrganizeWithHamsiManager);
    } else {
        Amarok.debug( translate("HamsiManagerInTheAmarok", "This Menu is already exist") );
    }

function Clear() {
    HamsiManagerInTheAmarok.terminate();
}