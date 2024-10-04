from PyQt5.Qt import QTranslator, QLocale, QLibraryInfo
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui, uic
from PyQt5.QtWebEngineWidgets import *
import webbrowser, requests, json, os, sys
path = os.path.dirname(os.path.realpath(__file__))
class Ui(QMainWindow):
    link ='http://http.cat/200'
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(path+'/main.ui', self)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("about:blank"))
        self.browser.urlChanged.connect(self.getimg)
        self.gridimg.addWidget(self.browser,0,0)
        self.setWindowIcon(QtGui.QIcon(path+'/resources/icon.ico'))
        self.searchbutton.clicked.connect(self.search)
        self.viewerlink.clicked.connect(self.openLink)
        self.searchbutton.setIcon(QtGui.QIcon(path+'/resources/search.gif'))
        
        #Показать
        self.showMaximized()

    def getimg(self):
        query = QUrl(self.link)
        if query.scheme() == '':
            query.setScheme('http')
        self.browser.setUrl(query)
    def search(self):       #Поиск
        try:
            req = 'https://api.nasa.gov/planetary/apod?api_key=523p5hPYHGzafYGLCkqa54kKMTV2vbP0XcPxkcLm&thumbs=True&date='+ self.searchline.text()
            response = requests.get(req)
            json_file = json.loads(response.text)
            title = 'Название: '+ json_file['title']+'\n\n--\n\n' if ('title' in json_file) else 'Название недоступно' + '\n\n--\n\n'
            copyright ='Правообладатель: '+ json_file['copyright'] + '\n\n--\n\n' if('copyright' in json_file) else 'Имя правообладателя недоступно' + '\n\n--\n\n'
            explanation = 'Описание: '+ json_file['explanation']
            date = json_file['date'] + '\n\n--\n\n  '
            descriptionvar = title + copyright + date + explanation
            self.description.clear()
            self.description.setPlainText(descriptionvar)
            if json_file['media_type'] == 'video':
                linkvideo = json_file['url'] if('youtube' in json_file['url']) else 'https:'+ json_file['url']
                self.link = linkvideo
            else:
                lnkinsimg = json_file['hdurl'] if ('hdurl' in json_file) else json_file['url'] 
                self.link = lnkinsimg
            self.browser.setUrl(QUrl(self.link))
        except BaseException as message:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка")
            msg.setText('Произошла ошибка')
            msg.setWindowIcon(QtGui.QIcon(path+'/resources/icon.ico'))
            msg.setDetailedText(str(message))
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()


    def openLink(self):
        webbrowser.open_new_tab(self.link)

app = QApplication(sys.argv)
window = Ui()
translator = QTranslator(app)
translator.load(path+'/qtbase_ru.qm')
app.installTranslator(translator)
window.search()
app.exec_()