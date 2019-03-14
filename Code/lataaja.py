'''
Created on 13.4.2018

@author: MJwork
'''
from ominaisuudet import Ominaisuudet
from PyQt5.Qt import QMessageBox, QPushButton

class Lataaja():
    
    def lataaja(self, tiedosto):
        '''Hoitaa muuttujien lataamisen annetusta tiedostosta'''
        lataus = False 
        try:
            '''Yrittää avata annetun tiedoston. Ilmoittaa jos tulee virhe'''
            file = open(tiedosto, "r")
            rivi = file.readline()
            rivi = rivi.strip()
            if rivi != "Lujuusanalysaattori":
                '''Kerrotaan käyttäjälle, että tiedosto oli virheellinen''' 
                msgBox = QMessageBox()
                msgBox.setText("Tiedoston lukeminen ei onnistu: Virheellinen tiedosto")
                msgBox.setWindowTitle("Virhe")
                msgBox.setMinimumWidth(50)
                msgBox.addButton(QPushButton('OK'), QMessageBox.NoRole)
                msgBox.exec_() 
                return lataus
        except FileNotFoundError:
            return lataus
        
        try:
            '''Ohitetaan päivämäärä'''
            rivi = file.readline()
            '''Luetaan arvot ja tallennetaan ne ominaisuudet luokan avulla'''
            '''Palkin pituus'''
            rivi = file.readline()
            Ominaisuudet.palkin_pituus(self, int(rivi))
            
            '''Palkin pituuden yksikko'''
            rivi = file.readline()
            Ominaisuudet.yksikko(self, int(rivi))
            
            '''Voiman suuruus'''
            rivi = file.readline()
            Ominaisuudet.voima(self, int(rivi)) 
            
            '''Voiman yksikkö'''
            rivi = file.readline()
            Ominaisuudet.yksikko_voima(self, int(rivi)) 
            
            '''Materiaali'''
            rivi = file.readline()
            Ominaisuudet.materiaali(self, int(rivi)) 
            
            '''Tuen tyyppi'''
            rivi = int(file.readline())
            Ominaisuudet.tuki(self, rivi)
            
            '''Onko ulkoinen voima asetettu 0=ei, 1=kyllä'''
            rivi = file.readline()
            Ominaisuudet.ulkoinen_voima(self, int(rivi)) 
            
            return True 
        
        except AttributeError:
            pass     