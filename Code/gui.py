'''
Created on 8.3.2018

@author: MJwork
'''
import sys 
from PyQt5.Qt import QPushButton, QFileDialog, QGraphicsRectItem ,\
    QGraphicsSimpleTextItem, QComboBox, QAction, QSpinBox, QLinearGradient,\
    QColor, QBrush, QMessageBox, QGraphicsLineItem, \
    QGraphicsPolygonItem
from PyQt5 import QtWidgets, QtCore, QtGui
from ominaisuudet import Ominaisuudet
from tallennin import Tallennin
from laskin import Laskin
from lataaja import Lataaja

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self):
        '''Asetetaan muuttujille alkuarvoja ohjelman suorittamiseksi'''
        super().__init__()
        self.title = "Lujuusanalysaattori"
        self.left = 200
        self.top = 200
        self.width = 1300   
        self.height = 700
        self.palkin_default_pituus = 5
        self.square_size = 10
        self.ikkuna()
        self.button_height = 75
        self.button_width = 150
        self.button_separation = 25
        self.x = 0 
        self.y = 0
        self.palkin_leveys = 700
        self.palkin_korkeus = 75 
        self.palkin_keskipiste = 650
        self.palkin_paatypiste = 1000
        self.yksikko_arvo = 0
        self.voima = 20
        self.maks_jannitys = "-"
        self.asteikko_teksti = QGraphicsSimpleTextItem()
        
        '''Lisää QGraphicsScenen ruudukon piirtämistä varten'''
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, -20, self.width - 200, self.height - 100)
               
        '''Suoritetaan lukuisia metodeja, jolla ohjelma "alustetaan"'''
        self.aloita_simulaatio()
        self.simulaatioikkuna() 
        self.simulaatio_nappi()
        self.materiaali_valikko()
        self.uusi_palkki_nappi()
        self.lisaa_tuki_nappi()
        self.lisaa_ulkoinen_voima_nappi()
        self.poista_ulkoinen_voima_nappi()
        self.vaihda_tuki_nappi()
        
        Ominaisuudet.alkuarvot(self)
        self.lisaa_palkki()
        self.palkin_pituus_valikko()
        self.yksikko_pituus()
        self.asteikko()
        self.lisaa_asteikko_arvo()
        self.asteikko_teksti.hide()
        self.tulos_teksti()
        self.lisaa_seina_tuki()
        self.lisaa_tuki_alhaalta()
        self.ulkoinen_voima_valikko()
        self.ulkoinen_voima_nuoli_alatuki()
        self.ulkoinen_voima_nuoli_seinatuki()
        Ominaisuudet.alkuarvot(self)
        '''Asetetaan tietyille napeille tietty näkyvyys'''
        self.lisaa_tuki.setEnabled(False)
        self.simuloi.setEnabled(False) 
        self.show()

    def ikkuna(self):
        '''Tekee ohjelman pääikkunan'''
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Lujuusanalysaattori')
        self.horizontal = QtWidgets.QHBoxLayout() 
        
        '''Luo menubarin'''
        self.uusiAction = QAction("Uusi simulaatio", self)
        self.uusiAction.setStatusTip("Luo uusi rakenne")
        self.uusiAction.triggered.connect(self.uusi_rakenne)
        self.uusiAction.setEnabled(True)
        self.uusiAction.setShortcut("Ctrl+N")
        
        self.tallennaAction = QAction("Tallenna simulaatio", self)
        self.tallennaAction.setStatusTip("Tallenna simulaatio")
        self.tallennaAction.triggered.connect(self.tallenna_rakenne)
        self.tallennaAction.setEnabled(False)
        self.tallennaAction.setShortcut("Ctrl+S")
        
        self.avaaAction = QAction("Lataa simulaatio", self)
        self.avaaAction.setStatusTip("Lataa simulaatio tiedostosta")
        self.avaaAction.triggered.connect(self.lataa_tallennettu_rakenne)
        self.avaaAction.setShortcut("Ctrl+O")
        
        self.exitAction = QAction("Exit", self)
        self.exitAction.setToolTip("Lopeta ohjelma")
        self.exitAction.triggered.connect(self.close_application)
        self.exitAction.setShortcut("Ctrl+E")
        self.statusBar()
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        aboutMenu = mainMenu.addMenu('&About')
        fileMenu.addAction(self.uusiAction)
        fileMenu.addAction(self.avaaAction)
        fileMenu.addAction(self.tallennaAction)
        fileMenu.addAction(self.exitAction)
    
    def tallenna_rakenne(self):
        '''Hoitaa rakenteen tallentamisen'''
        tallennus = Tallennin.tallenin(self)
        if tallennus == True:
            '''Kerrotaan käyttäjälle, että tallennus onnistui''' 
            msgBox = QMessageBox()
            msgBox.setText("Tallennus onnistui!")
            msgBox.setWindowTitle("Onnistunut Tallennus")
            msgBox.setMinimumWidth(50)
            msgBox.addButton(QPushButton('OK'), QMessageBox.NoRole)
            msgBox.exec_()
            
    def lataa_tallennettu_rakenne(self):
        '''Metodi avaa QFileDialog ikkunan, josta käyttäjä valitsee tiedoston, jossa aiemmin tallennettu rakenne sijaitsee. Vain .txt -tiedostot 
        ovat ladattavissa '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        tiedosto, _ = QFileDialog.getOpenFileName(self,"Valitse tiedosto", "","txt Files (*.txt)", options=options)
        lataus = Lataaja.lataaja(self, tiedosto)
        if lataus == False:
            return
        
        if lataus == True:
            self.uusi_rakenne()
            Lataaja.lataaja(self, tiedosto)
            tuen_tyyppi = Ominaisuudet.palauta_tuen_tyyppi(self)
            '''Jos tuki on seinästä, piirretään sitä vastaava grafiikka'''
            if tuen_tyyppi == 0: 
                self.nayta_seina_tuki()
                self.gradient_seina_tuki()
                
            '''Jos tuki on alhaalta, piirretään sitä vastaava grafiikka'''
            if tuen_tyyppi == 1: 
                self.nayta_tuki_alhaalta()
                self.gradient_alatuki()    
            
            if tuen_tyyppi != 2: 
                self.vaihda_tuki.show()
                self.lisaa_tuki.hide()            
            '''Jos ulkoinen voima on asetettu, piirretään se'''
            ulkoinen_voima = int(Ominaisuudet.onko_ulkoinen_voima_asetettu(self))
            if ulkoinen_voima == 1:
                self.nayta_ulkoinen_voima() 
            
            self.nayta_palkki()
            Laskin.laskin(self)
            self.paivita_tulos_teksti()
            self.tulos.show()
            self.sp.setValue(float(Ominaisuudet.palauta_palkin_pituus(self)))
            self.uusiAction.setEnabled(True)
            self.simuloi.setEnabled(True)
            
            '''Kerrotaan käyttäjälle, että kaikki onnistui''' 
            msgBox = QMessageBox()
            msgBox.setText("Lataus onnistui!")
            msgBox.setWindowTitle("Onnistunut lataus")
            msgBox.addButton(QPushButton('OK'), QMessageBox.NoRole)
            msgBox.exec_()
        
    def aloita_simulaatio(self):
        '''Aloittaa simulaation'''
        self.setCentralWidget(QtWidgets.QWidget()) 
        self.horizontal = QtWidgets.QHBoxLayout() 
        self.centralWidget().setLayout(self.horizontal)
        
    def simulaatioikkuna(self):
        '''lisää view näyttämistä varten'''
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
     
    def uusi_palkki_nappi(self):
        '''Luo Uusi palkki -napin'''
        self.uusi_palkki = QPushButton('Uusi palkki')
        self.uusi_palkki.setToolTip("Lisää uusi palkki")
        self.uusi_palkki.move(0, 0)
        self.uusi_palkki.resize(self.button_width, self.button_height)
        self.uusi_palkki.font = QtGui.QFont()
        self.uusi_palkki.font.setPointSize(12)
        self.uusi_palkki.setFont(self.uusi_palkki.font)
        self.uusi_palkki.setEnabled(True)
        self.scene.addWidget(self.uusi_palkki)
        self.uusi_palkki.clicked.connect(self.nayta_palkki)  
        
    def nayta_palkki(self):
        '''Näyttää kaikki palkkiin liittyvät komponentit sekä asettaa uusi palkki -napin toimimattomaksi'''
        self.rect.show()
        self.palkin_pituus.show()
        self.sp.show()
        self.yksikko.show()
        self.asteikko_teksti.show()
        self.line.show()
        self.nuoli_1.show()
        self.nuoli_2.show()
        self.uusi_palkki.setEnabled(False)
        self.lisaa_tuki.setEnabled(True)
        self.materiaali_valinta.setEnabled(True)
        
    
    def lisaa_palkki(self):
        '''lisää palkin'''
        self.rect = QGraphicsRectItem(300, 200, self.palkin_leveys, self.palkin_korkeus)
        self.rect.setBrush(QBrush(4))
        self.scene.addItem(self.rect)
        self.rect.hide()
        self.lisaa_tuki.setEnabled(True)
        
        '''Aina kun on uusi palkki luotu, voidaan aloittaa simulaatio alusta'''
        self.uusiAction.setEnabled(True)
    
    def lisaa_tuki_nappi(self):
        '''Luo Lisää tuki -napin'''
        self.lisaa_tuki = QPushButton("Lisää tuki")
        self.lisaa_tuki.setToolTip("Lisää tuki")
        self.lisaa_tuki.move(0, self.button_height + self.button_separation)
        self.lisaa_tuki.resize(self.button_width, self.button_height)
        self.lisaa_tuki.font = QtGui.QFont()
        self.lisaa_tuki.font.setPointSize(12)
        self.lisaa_tuki.setFont(self.lisaa_tuki.font)
        self.lisaa_tuki.setEnabled(False)
        self.lisaa_tuki.clicked.connect(self.valitse_tuki)
        self.scene.addWidget(self.lisaa_tuki)
        
    def vaihda_tuki_nappi(self):
        '''Luo vaihda tuki -napin'''
        self.vaihda_tuki = QPushButton("Vaihda tuki")
        self.vaihda_tuki.setToolTip("Vaihda tuki")
        self.vaihda_tuki.move(0, self.button_height + self.button_separation)
        self.vaihda_tuki.resize(self.button_width, self.button_height)
        self.vaihda_tuki.setFont(self.lisaa_tuki.font)
        self.vaihda_tuki.clicked.connect(self.valitse_tuki)
        self.scene.addWidget(self.vaihda_tuki)
        self.vaihda_tuki.hide()
        
    def valitse_tuki(self):        
        '''Tuen valinta.
        Jos tuki on seinästä (tyyppi = 0), kysytään halutaanko vaihtaa.
        Jos haluaa muutetaan tuen grafiikka ja arvo'''
        
        if Ominaisuudet.palauta_tuen_tyyppi(self) == 0:
            msgBox = QMessageBox()
            msgBox.setText("Haluatko vaihtaa tuen tyyppiä?")
            msgBox.addButton(QPushButton('En'), QMessageBox.NoRole)
            msgBox.addButton(QPushButton('Kyllä'), QMessageBox.YesRole)
            vastaus = msgBox.exec_()
            self.rect.setBrush(QBrush(4))
            
            if vastaus == 1:
                self.viiva_1.hide()
                self.viiva_2.hide()
                self.viiva_3.hide()
                self.viiva_4.hide()
                self.nayta_tuki_alhaalta()
                
                if int(Ominaisuudet.onko_ulkoinen_voima_asetettu(self)) == 1:
                    self.viiva.hide()
                    self.nuoli_3.hide()
                    self.viiva_5.show()
                    self.nuoli_6.show()
                
                Ominaisuudet.tuki(self, 1)
            return
        
        '''Jos tuki on alhaalta (tyyppi = 1), kysytään halutaanko vaihtaa.
        Jos haluaa muutetaan tuen grafiikka ja arvo'''    
        if Ominaisuudet.palauta_tuen_tyyppi(self) == 1:
            msgBox = QMessageBox()
            msgBox.setText("Haluatko vaihtaa tuen tyyppiä?")
            msgBox.addButton(QPushButton('Kyllä'), QMessageBox.YesRole)
            msgBox.addButton(QPushButton('En'), QMessageBox.NoRole)
            vastaus = msgBox.exec_()
            self.rect.setBrush(QBrush(4))
            
            if vastaus == 0:
                Ominaisuudet.tuki(self, 0) 
                self.nuoli_4.hide()
                self.nuoli_5.hide()
                self.nayta_seina_tuki()
                
                if int(Ominaisuudet.onko_ulkoinen_voima_asetettu(self)) == 1:
                    self.viiva.show()
                    self.nuoli_3.show()
                    self.viiva_5.hide()
                    self.nuoli_6.hide()
                
            if vastaus == 1:
                pass
        
        '''Jos tukea ei ole (tyyppi = 2). Tuen tyypin valinta'''   
        if Ominaisuudet.palauta_tuen_tyyppi(self) == 2:
            msgBox = QMessageBox()
            msgBox.setText("Valitse tuen tyyppi")
            msgBox.addButton(QPushButton('Seinätuki'), QMessageBox.YesRole)
            msgBox.addButton(QPushButton('Tuki alhaalta'), QMessageBox.NoRole)
            vastaus = msgBox.exec_()
            self.vaihda_tuki.show()
            self.lisaa_tuki.hide()
            
            if vastaus == 0:
                self.nayta_seina_tuki()
                Ominaisuudet.tuki(self, 0)
                
            if vastaus == 1:
                self.nayta_tuki_alhaalta() 
                Ominaisuudet.tuki(self, 1)
                
        '''Joka tapauksessa asetetaan ulkoisen voiman lisääminen mahdolliseksi
        sekä maalataan palkki normaaliksi'''
        self.lisaa_ulkoinen_voima.setEnabled(True)
        self.simuloi.setEnabled(True)
        
    
    def nayta_seina_tuki(self):
        '''Näytetään seinätukea kuvaavat grafiikat'''
        self.viiva_1.show()
        self.viiva_2.show()
        self.viiva_3.show()
        self.viiva_4.show()
        
    def nayta_tuki_alhaalta(self):
        '''Näytetään alatukea kuvaavat grafiikat'''
        self.nuoli_4.show()
        self.nuoli_5.show()
        
    def paivita_tuen_tyyppi(self, tyyppi):
        '''Päivittää tuen tyypin arvon Ominaisuudet luokassa'''
        Ominaisuudet.tuki(self, tyyppi)
        
    def lisaa_seina_tuki(self):
        '''Piirtää seinätukea kuvaavat viivat sekä asettaa self.tuen_tyyppi arvoksi 
        Asettaa SIMULOI-napin painettavaksi'''
        viiva = QtGui.QPen(QtCore.Qt.black, 2)
        viiva.setStyle(QtCore.Qt.SolidLine)
        self.viiva_1 = QGraphicsLineItem(QtCore.QLineF(300, 202, 275, 225))
        self.viiva_2 = QGraphicsLineItem(QtCore.QLineF(300, 222, 275, 245))
        self.viiva_3 = QGraphicsLineItem(QtCore.QLineF(300, 242, 275, 265))
        self.viiva_4 = QGraphicsLineItem(QtCore.QLineF(300, 262, 275, 285))
          
        self.scene.addItem(self.viiva_1)
        self.scene.addItem(self.viiva_2)
        self.scene.addItem(self.viiva_3)
        self.scene.addItem(self.viiva_4)
        self.viiva_1.hide()
        self.viiva_2.hide()
        self.viiva_3.hide()
        self.viiva_4.hide()
        tyyppi = 0
        Ominaisuudet.tuki(self, tyyppi)
        self.simuloi.setEnabled(True)
        
    def lisaa_tuki_alhaalta(self):
        '''Piirtää alhaalta tukemista kuvaavat grafiikat
        sekä asettaa self.tuen_tyyppi arvoksi 1'''
        leveys = 15 #nuolen leveus pikseleissä
        korkeus = 30 #nuuolen korkeus pikseleissä
        
        '''Nuolen kärkien koordinaatit'''
        nuoli_piste_1 = QtCore.QPointF(305, 275)
        nuoli_piste_2 = QtCore.QPointF(305 - leveys, 275 + korkeus)
        nuoli_piste_3 = QtCore.QPointF(305 + leveys, 275 + korkeus)
        
        nuoli_piste_4 = QtCore.QPointF(995, 275)
        nuoli_piste_5 = QtCore.QPointF(995 - leveys, 275 + korkeus)
        nuoli_piste_6 = QtCore.QPointF(995 + leveys, 275 + korkeus)
        
        '''Luodaan nuolia kuvaavat QPolygonF oliot'''
        self.nuoli_4  = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_piste_1, nuoli_piste_2, nuoli_piste_3]))
        self.nuoli_5 = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_piste_4, nuoli_piste_5, nuoli_piste_6]))
        self.nuoli_brush = QtGui.QBrush(1)
        self.nuoli_pencil = QtGui.QPen(QtCore.Qt.black, 2)
        self.nuoli_pencil.setStyle(QtCore.Qt.SolidLine)
        
        '''Lisätään nuolet sceneen'''
        self.scene.addItem(self.nuoli_4)
        self.scene.addItem(self.nuoli_5)
        self.nuoli_4.hide()
        self.nuoli_5.hide()
        
        tyyppi = 1
        Ominaisuudet.tuki(self, tyyppi)
        self.simuloi.setEnabled(True) 
        
    def lisaa_ulkoinen_voima_nappi(self):
        '''Luo Lisää ulkoinen voima -napin'''
        self.lisaa_ulkoinen_voima = QPushButton("Lisää ulkoinen voima")
        self.lisaa_ulkoinen_voima.setToolTip("Lisää ulkoinen voima")
        self.lisaa_ulkoinen_voima.move(0, 2 * self.button_height + 2 * self.button_separation) 
        self.lisaa_ulkoinen_voima.resize(self.button_width, self.button_height)
        self.lisaa_ulkoinen_voima.font = QtGui.QFont()
        self.lisaa_ulkoinen_voima.font.setPointSize(8)
        self.lisaa_ulkoinen_voima.setFont(self.lisaa_ulkoinen_voima.font)
        self.lisaa_ulkoinen_voima.clicked.connect(self.nayta_ulkoinen_voima)
        self.lisaa_ulkoinen_voima.clicked.connect(self.nollaa_gradientti)
        self.lisaa_ulkoinen_voima.setEnabled(False)
        self.scene.addWidget(self.lisaa_ulkoinen_voima)
    
    def poista_ulkoinen_voima_nappi(self):
        '''Luo poista ulkoinen voima -napin'''
        self.poista_ulkoinen_voima = QPushButton("Poista ulkoinen voima")
        self.poista_ulkoinen_voima.setToolTip("Poista ulkoinen voima")
        self.poista_ulkoinen_voima.move(0, 2 * self.button_height + 2 * self.button_separation) 
        self.poista_ulkoinen_voima.resize(self.button_width, self.button_height)
        self.poista_ulkoinen_voima.setFont(self.lisaa_ulkoinen_voima.font)
        self.poista_ulkoinen_voima.clicked.connect(self.piilota_ulkoinen_voima)
        self.poista_ulkoinen_voima.clicked.connect(self.nollaa_gradientti)
        self.scene.addWidget(self.poista_ulkoinen_voima)
        self.poista_ulkoinen_voima.hide()
    
    def piilota_ulkoinen_voima(self):
        '''Piilotaa kaiken ulkoiseen voimaan liittyvän'''
        self.sp_voima.hide()
        self.yksikko_voima.hide()
        self.ulkoinen_voima.hide()
        self.lisaa_ulkoinen_voima.show()
        self.lisaa_ulkoinen_voima.setEnabled(True) 
        self.viiva.hide() 
        self.nuoli_3.hide()
        self.viiva_5.hide()
        self.nuoli_6.hide()
        self.poista_ulkoinen_voima.hide()
        self.lisaa_ulkoinen_voima.show()
        self.tulos.hide()
       
        Ominaisuudet.ulkoinen_voima(self, 0)
        
    def nayta_ulkoinen_voima(self):
        '''Näytetään ulkoinen voima riippuen tuen tyypistä'''
        self.sp_voima.show()
        self.yksikko_voima.show()
        self.ulkoinen_voima.show()
        self.lisaa_ulkoinen_voima.hide()
        self.poista_ulkoinen_voima.show()
        
        if int(Ominaisuudet.palauta_tuen_tyyppi(self)) == 0:
            self.viiva.show() 
            self.nuoli_3.show()
        
        if int(Ominaisuudet.palauta_tuen_tyyppi(self)) == 1:
            self.viiva_5.show()
            self.nuoli_6.show()
        
        Ominaisuudet.ulkoinen_voima(self, 1)
        
    def ulkoinen_voima_valikko(self):
        '''Luo voiman suuruus -tekstin'''
        self.ulkoinen_voima = QGraphicsSimpleTextItem("Voiman suuruus")
        self.ulkoinen_voima.setPos(600, 5)
        self.ulkoinen_voima.font = QtGui.QFont()
        self.ulkoinen_voima.font.setPointSize(12)
        self.ulkoinen_voima.setFont(self.ulkoinen_voima.font)
        self.lisaa_ulkoinen_voima.setEnabled(False)
        self.scene.addItem(self.ulkoinen_voima)
        self.ulkoinen_voima.hide()
        
        '''Luo voiman arvon QSpinBoxin'''
        self.sp_voima = QSpinBox()
        self.sp_voima.move(750, 5)
        self.sp_voima.setRange(0, 10000)
        self.sp_voima.setSingleStep(1)
        self.sp_voima.setMinimumHeight(30)
        self.sp_voima.setValue(int(Ominaisuudet.palauta_voima(self)))
        self.sp_voima.valueChanged.connect(self.paivita_voima)
        self.scene.addWidget(self.sp_voima)
        self.sp_voima.hide()
    
        '''Luo yksikönvalinta QComboBOxin'''
        self.yksikko_voima = QComboBox()
        self.yksikko_voima.addItem("kN", 0)
        self.yksikko_voima.addItem("N", 1)
        self.yksikko_voima.move(820, 5)
        self.yksikko_voima.setMinimumHeight(30)
        self.yksikko_voima.setCurrentIndex(int(Ominaisuudet.palauta_voiman_yksikko(self)))
        self.yksikko_voima.setEditable(True)
        self.yksikko_voima.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.scene.addWidget(self.yksikko_voima)    
        self.yksikko_voima.currentIndexChanged.connect(self.paivita_yksikko_voima)
        self.yksikko_voima.hide()
        
    def ulkoinen_voima_nuoli_seinatuki(self):
        '''Luo nuolen osoittamaan ulkoisen voiman paikkaa'''
        voima_viiva = QtGui.QPen(QtCore.Qt.black, 2)
        voima_viiva.setStyle(QtCore.Qt.SolidLine)
    
        '''Nuolen kärkien koordinaatit seinätuelle'''
        nuoli_piste_1 = QtCore.QPointF(self.palkin_paatypiste - 7, 185)
        nuoli_piste_2 = QtCore.QPointF(self.palkin_paatypiste, 200)
        nuoli_piste_3 = QtCore.QPointF(self.palkin_paatypiste + 7, 185)
        viiva_x = self.palkin_paatypiste
        self.viiva = QGraphicsLineItem(QtCore.QLineF(viiva_x, 100, viiva_x, 200))
        
        '''Luodaan nuoli QPolygonItem olio'''
        self.nuoli_3  = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_piste_1, nuoli_piste_2, nuoli_piste_3]))
        self.nuoli_brush = QtGui.QBrush(1)
        self.nuoli_pencil = QtGui.QPen(QtCore.Qt.black, 2)
        self.nuoli_pencil.setStyle(QtCore.Qt.SolidLine )
        
        '''Lisätään viiva sekä päiden nuolet sceneen'''
        self.scene.addItem(self.viiva)
        self.scene.addItem(self.nuoli_3)   
        self.viiva.hide()
        self.nuoli_3.hide()
        
        '''Lisätään tieto, että voima on asetettu'''
        Ominaisuudet.ulkoinen_voima(self, 1)   
    
    def ulkoinen_voima_nuoli_alatuki(self): 
        '''Nuolen kärkien koordinaatit alhaalta tuetulle palkille'''
        nuoli_piste_1 = QtCore.QPointF(self.palkin_keskipiste - 7, 185)
        nuoli_piste_2 = QtCore.QPointF(self.palkin_keskipiste, 200)
        nuoli_piste_3 = QtCore.QPointF(self.palkin_keskipiste + 7, 185)
        viiva_x = self.palkin_keskipiste
            
        '''Luodaan nuoli QPolygonItem olio'''
        self.nuoli_6  = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_piste_1, nuoli_piste_2, nuoli_piste_3]))
        self.nuoli_brush = QtGui.QBrush(1)
        self.nuoli_pencil = QtGui.QPen(QtCore.Qt.black, 2)
        self.nuoli_pencil.setStyle(QtCore.Qt.SolidLine )
        
        self.viiva_5 = QGraphicsLineItem(QtCore.QLineF(viiva_x, 100, viiva_x, 200))
        '''Lisätään viiva sekä päiden nuolet sceneen'''
        self.scene.addItem(self.viiva_5)
        self.scene.addItem(self.nuoli_6)   
        self.viiva_5.hide()
        self.nuoli_6.hide()
        
        '''Lisätään tieto, että voima on asetettu'''
        Ominaisuudet.ulkoinen_voima(self, 1)   
    
    def paivita_voima(self):
        '''Lukee voiman arvon 
        ja kutsuu Ominaisuudet luoka metodia voima'''
        voima = self.sp_voima.value()
        Ominaisuudet.voima(self, voima)
        
    def paivita_yksikko_voima(self):
        '''Lukee ykiskön arvon 
        ja kutsuu Ominaisuudet-luokan metodia yksikko_voima'''
        self.yksikko_voima_arvo = self.yksikko_voima.currentData()
        Ominaisuudet.yksikko_voima(self, self.yksikko_voima_arvo)
        
    def materiaali_valikko(self):
        ''' Luo Materiaali-otsikon'''
        self.materiaali = QGraphicsSimpleTextItem("Materiaali")
        self.materiaali.setPos(0, 3 * self.button_height + 3 * self.button_separation)
        self.materiaali.font = QtGui.QFont()
        self.materiaali.font.setPointSize(12)
        self.materiaali.setFont(self.materiaali.font)
        self.scene.addItem(self.materiaali)
        
        '''Luo drop down valikon materiaalivalinnalle'''
        self.materiaali_valinta = QComboBox()
        self.materiaali_valinta.addItem("Teräs", 0)
        self.materiaali_valinta.addItem("Alumiini", 1)
        self.materiaali_valinta.addItem("Muovi", 2)
        self.materiaali_valinta.move(0, 3 * self.button_height + 3 * self.button_separation + 25)
        self.materiaali_valinta.resize(self.button_width, self.button_height - 25)
        self.materiaali_valinta.setEditable(True)
        self.materiaali_valinta.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.materiaali_valinta.setCurrentIndex(0)
        self.scene.addWidget(self.materiaali_valinta)
        self.materiaali_valinta.setEnabled(False)
        self.materiaali_valinta.currentIndexChanged.connect(self.paivita_materiaali)
    
    def paivita_materiaali(self):
        '''Lukee materiaalin arvon 
        ja kutsuu Ominaisuudet-luokan metodia materiaali'''
        materiaali = self.materiaali_valinta.currentData()
        Ominaisuudet.materiaali(self, materiaali) 
            
    def simulaatio_nappi(self):
        '''Luo SIMULOI-napin'''
        self.simuloi = QPushButton('SIMULOI')
        self.simuloi.setToolTip('Simuloi valittu rakenne')
        self.simuloi.move(0, 4 * self.button_height + 4 * self.button_separation)
        self.simuloi.setStyleSheet("background-color:rgb(122, 201, 255)") 
        self.simuloi.resize(self.button_width, self.button_height)
        self.simuloi.font = QtGui.QFont()
        self.simuloi.font.setPointSize(12)
        self.simuloi.setFont(self.simuloi.font)
        self.simuloi.setEnabled(False)
        self.simuloi.clicked.connect(self.simulaatio)
        self.scene.addWidget(self.simuloi)
        
    def simulaatio(self):
        '''Kutsuu laskentaa suorittavaa metodia ja tallentaa tuloksen.
        Tämän jälkeen kutsuu lopputuloksen esittävän tekstin päivittävää metodia
        sekä palkin visualisoivaa gradient-metodia'''
        Laskin.laskin(self)
        Ominaisuudet.palauta_tulos(self)
        self.paivita_tulos_teksti()
        self.tallennaAction.setEnabled(True)
        
        if Ominaisuudet.palauta_tuen_tyyppi(self) == 0:
            
            if Ominaisuudet.onko_ulkoinen_voima_asetettu(self) == 1:
                self.gradient_seina_tuki()
            
            if Ominaisuudet.onko_ulkoinen_voima_asetettu(self) == 0:
                self.gradient_seina_tuki_ei_voimaa()
                
        if Ominaisuudet.palauta_tuen_tyyppi(self) == 1:
            self.gradient_alatuki()
            
    def tulos_teksti(self):
        '''Lisää tekstin, joka kertoo maksimijänintyksen arvon'''
        teksti = "Maksimijännitys " + str(self.maks_jannitys) + " MPa"
        self.tulos = QGraphicsSimpleTextItem(teksti)
        self.tulos.setPos(550, 500)
        self.tulos.font = QtGui.QFont()
        self.tulos.font.setPointSize(12)
        self.tulos.setFont(self.tulos.font)
        self.scene.addItem(self.tulos)
        self.tulos.hide()
    
    def paivita_tulos_teksti(self):
        '''Päivittää maksimijännityksen arvoa kuvaavan tekstin'''
        maks_jannitys = Ominaisuudet.palauta_tulos(self)
        self.tulos.setText("Maksimijännitys " + str(maks_jannitys) + " MPa")  
        self.tulos.show()
        
    def palkin_pituus_valikko(self):
        '''Luo palkin pituus tekstin sekä spinbox-valitsimen pituuden asettamista varten
        Päivittää palkin pituuden Ominaisuudet luokan avulla'''
        self.palkin_pituus = QGraphicsSimpleTextItem("Palkin pituus")
        self.palkin_pituus.setPos(300, 5)
        self.palkin_pituus.font = QtGui.QFont()
        self.palkin_pituus.font.setPointSize(12)
        self.palkin_pituus.setFont(self.palkin_pituus.font)
        self.scene.addItem(self.palkin_pituus)
        self.palkin_pituus.hide()
        
        self.sp = QSpinBox()
        self.scene.addWidget(self.sp)
        self.sp.hide()
        self.sp.move(450, 5)
        self.sp.setRange(0, 100)
        self.sp.setSingleStep(1)
        self.sp.setMinimumHeight(30)
        self.sp.setValue(int(Ominaisuudet.palauta_palkin_pituus(self)))
        self.paivita_pituus()
        self.sp.valueChanged.connect(self.paivita_pituus)
        
    def paivita_pituus(self):
        '''Lukee palkin pituuden ja aktivoi Ominaisuudet luokan meodin palkin pituus'''
        self.palkin_pituus_arvo = self.sp.value()
        Ominaisuudet.palkin_pituus(self, self.palkin_pituus_arvo)
        self.paivita_asteikon_arvot()
        
    def yksikko_pituus(self):
        '''Luo yksikönvalinta dropdown-menun
        ja arvon muuttuessa päivittää yksikön Ominaisuudet-luokassa'''
        self.yksikko = QComboBox()
        self.yksikko.addItem("m", 0)
        self.yksikko.addItem("cm", 1)
        self.yksikko.addItem("mm", 2)
        self.yksikko.move(500, 5)
        self.yksikko.setMinimumHeight(30)
        self.yksikko.setEditable(True)
        self.yksikko.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.yksikko.setCurrentIndex(Ominaisuudet.palauta_pituuden_yksikko(self))
        self.scene.addWidget(self.yksikko) 
        self.yksikko.hide()  
        self.yksikko_arvo = self.yksikko.currentData() 
        self.yksikko.currentIndexChanged.connect(self.paivita_yksikko)
    
    def paivita_yksikko(self): 
        '''Lukee yksikön arvon 
        ja kutsuu Ominaisuudet-luokan metodia yksikko''' 
        self.yksikko_arvo = self.yksikko.currentData()
        Ominaisuudet.yksikko(self, self.yksikko_arvo)
        self.paivita_asteikon_arvot()
        
    def asteikko(self):
        ''''Luodaan viivaa kuvaava olio'''
        viiva = QtGui.QPen(QtCore.Qt.black, 2)
        viiva.setStyle(QtCore.Qt.SolidLine)
        
        '''Oikean puoleisen nuolen kärkien koordinaatit'''
        nuoli_1_piste_1 = QtCore.QPointF(990, 390)
        nuoli_1_piste_2 = QtCore.QPointF(1000, 400)
        nuoli_1_piste_3 = QtCore.QPointF(990, 410)
        
        '''Vasemman puoleisen nuolen kärkien koordinaatit'''
        nuoli_2_piste_1 = QtCore.QPointF(310, 390)
        nuoli_2_piste_2 = QtCore.QPointF(300, 400)
        nuoli_2_piste_3 = QtCore.QPointF(310, 410)
        
        '''Luodaan nuoli QPolygonF oliot'''
        self.nuoli_1  = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_1_piste_1, nuoli_1_piste_2, nuoli_1_piste_3]))
        self.nuoli_2  = QGraphicsPolygonItem(QtGui.QPolygonF([nuoli_2_piste_1, nuoli_2_piste_2, nuoli_2_piste_3]))
       
        self.nuoli_brush = QtGui.QBrush(1)
        self.nuoli_pencil = QtGui.QPen(QtCore.Qt.black, 2)
        self.nuoli_pencil.setStyle(QtCore.Qt.SolidLine )
        
        self.line = QGraphicsLineItem(QtCore.QLineF(300, 400, 1000, 400))
        '''Lisätään viiva sekä päiden nuolet sceneen'''
        self.scene.addItem(self.line)
        self.scene.addItem(self.nuoli_1)
        self.scene.addItem(self.nuoli_2)
        self.line.hide()
        self.nuoli_1.hide()
        self.nuoli_2.hide()
        
    def lisaa_asteikko_arvo(self):
        '''Lisää tekstikentän pituuden arvolle sekä yksikölle'''
        teksti = (str(Ominaisuudet.palauta_palkin_pituus(self)) + " " + "m")   
        self.asteikko_teksti = QGraphicsSimpleTextItem()
        self.asteikko_teksti.setText(teksti)
        self.asteikko_teksti.setPos(650, 425)
        self.asteikko_teksti.font = QtGui.QFont()
        self.asteikko_teksti.font.setPointSize(12)
        self.asteikko_teksti.setFont(self.asteikko_teksti.font)
        self.scene.addItem(self.asteikko_teksti)
        self.asteikko_teksti.hide()
    
    def paivita_asteikon_arvot(self):
        '''Päivittää palkin pituutta kuvaavan asteikon'''
        yksikko = Ominaisuudet.palauta_pituuden_yksikko(self)
        
        if yksikko == 0:
            self.yksikko_merkki = "m"
        if yksikko == 1:
            self.yksikko_merkki = "cm"
        if yksikko == 2:
            self.yksikko_merkki = "mm"
        
        pituus = float(Ominaisuudet.palauta_palkin_pituus(self))
        teksti = str(str(pituus) + " " + self.yksikko_merkki)    
        self.asteikko_teksti.setText(teksti)
        self.asteikko_teksti.show()
        
    def gradient_seina_tuki(self):
        '''Luo seinästä tuetun palkin rasitusta kuvaavan gradientin'''
        gradient = QLinearGradient(300, 200, 300 + self.palkin_leveys, 200)
        gradient.setColorAt(0, QColor(244, 72, 66))
        gradient.setColorAt(1, QColor(65, 244, 83))
        self.rect.setBrush(gradient)
    
    def gradient_seina_tuki_ei_voimaa(self):
        '''Luo ilman ulkoista voimaa olevan gradientin'''
        gradient = QLinearGradient(300, 200, 300 + (self.palkin_leveys / 2), 200)
        gradient.setColorAt(0, QColor(244, 72, 66))
        gradient.setColorAt(1, QColor(65, 244, 83))
        self.rect.setBrush(gradient)
    
    def gradient_alatuki(self):
        '''Luo kahdella alatuella olevan palkin rasitusta kuvaavan gradientin'''
        gradient = QLinearGradient(300, 200, 300 + self.palkin_leveys, 200)
        gradient.setColorAt(0, QColor(65, 244, 83))
        gradient.setColorAt(0.5, QColor(244, 72, 66))
        gradient.setColorAt(1, QColor(65, 244, 83))
        self.rect.setBrush(gradient)
        
    def nollaa_gradientti(self):
        '''Asettaa palkin "normaaliksi"'''
        self.rect.setBrush(QBrush(4))
        
    def uusi_rakenne(self):
        '''Muokkaa ikkunaa uuden simulaation luomista varten'''
        self.rect.hide()
        self.ulkoinen_voima.hide()
        self.sp_voima.hide()
        self.yksikko_voima.hide()
        self.nuoli_1.hide()
        self.nuoli_2.hide()
        self.nuoli_3.hide()
        self.nuoli_4.hide()
        self.nuoli_5.hide()
        self.nuoli_6.hide()
        self.viiva_1.hide()
        self.viiva_2.hide()
        self.viiva_3.hide()
        self.viiva_4.hide()
        self.viiva_5.hide()
        self.viiva.hide()
        self.palkin_pituus.hide()
        self.sp.hide()
        self.yksikko.hide()
        self.line.hide()
        self.asteikko_teksti.hide()
        self.tulos.hide()
        self.nollaa_gradientti()
        self.lisaa_tuki.show()
        self.vaihda_tuki.hide()
        self.poista_ulkoinen_voima.hide()
        self.lisaa_ulkoinen_voima.show()
        Ominaisuudet.alkuarvot(self)
        
        '''Asettaa napit'''
        self.uusi_palkki.setEnabled(True)
        self.lisaa_ulkoinen_voima.setEnabled(False)
        self.lisaa_tuki.setEnabled(False)
        self.simuloi.setEnabled(False)
        self.tallennaAction.setEnabled(False)
        
        '''Päivittää tuen tyypiksi arvon, joka vastaa, ettei tukea ole'''
        self.tuen_tyyppi = 2
    
    def close_application(self):
        '''sulkee ohjelman'''
        sys.exit()
        