'''
Created on 12.4.2018

@author: MJwork
'''
import datetime
from ominaisuudet import Ominaisuudet
from PyQt5.QtWidgets import QFileDialog

class Tallennin():
        
    def tallenin(self):
        '''Suorittaa tiedoston tallennuksen'''
        pvm = str(datetime.date.today())
        palkin_pituus = Ominaisuudet.palauta_palkin_pituus(self)
        pituuden_yksikko = Ominaisuudet.palauta_pituuden_yksikko(self)
        voiman_suuruus = Ominaisuudet.palauta_voima(self)
        voiman_yksikko = Ominaisuudet.palauta_voiman_yksikko(self)
        materiaali = Ominaisuudet.palauta_materiaali(self)
        tuen_tyyppi = Ominaisuudet.palauta_tuen_tyyppi(self)
        ulkoinen_voima_asetettu = Ominaisuudet.onko_ulkoinen_voima_asetettu(self)
        
        tiedostonimi= QFileDialog.getSaveFileName(self,"Tallenna tiedosto","","Text Files (*);;Text Files (*.txt)")      
        try:
            tiedosto = open(tiedostonimi[0], 'w')
        except FileNotFoundError:
            return
        
        teksti = "Lujuusanalysaattori" + "\n"\
        + pvm + "\n" \
        + str(palkin_pituus) +"\n"\
        + str(pituuden_yksikko) + "\n"\
        + str(voiman_suuruus) + "\n"\
        + str(voiman_yksikko) + "\n"\
        + str(materiaali) + "\n"\
        + str(tuen_tyyppi) + "\n"\
        + str(ulkoinen_voima_asetettu)
        
        tiedosto.write(teksti)
        tiedosto.close()
        
        return True
    
        