'''
Created on 20.3.2018

@author: MJwork
'''

class Ominaisuudet():   
    
    def alkuarvot(self):
        '''Asettaa muuttujien default-arot'''
        self.palkin_pituus_value = 10
        self.yksikko_value = 0    
        self.voiman_suuruus = 100
        self.yksikko_voima_value = 0 
        self.materiaali = 0 
        self.tuen_tyyppi = 2 
        self.ulkoinen_voima_asetettu = 0
        self.maksimi_jannitys = 0 
        
    def palkin_pituus(self, pituus):
        '''Tallentaa palkin pituuden'''
        self.palkin_pituus_value = pituus
        
    def palauta_palkin_pituus(self):
        '''Palauttaa palkin pituuden'''
        return self.palkin_pituus_value
        
    def yksikko(self, yksikko):
        '''tallentaa pituudessa käytettävän yksikön arvon'''
        self.yksikko_value = yksikko
        
    def palauta_pituuden_yksikko(self):
        '''Palauttaa pituuden yksikön lukuarvon'''
        return self.yksikko_value
    
    def voima(self, voima):
        '''tallentaan ulkoisen voiman suuruudeen'''
        self.voiman_suuruus = voima
    
    def palauta_voima(self):
        '''Palauttaa ulkoisen voiman suuruuden'''
        return self.voiman_suuruus    
    
    def yksikko_voima(self, yksikko):
        '''tallentaa voiman yksikön arvon'''
        self.yksikko_voima_value = yksikko
    
    def ulkoinen_voima(self, arvo):
        '''Muuttaa arvon, joka kuvaa ulkoisen voiman asettamista'''
        self.ulkoinen_voima_asetettu = arvo 
    
    def palauta_voiman_yksikko(self):
        '''Palauttaa voiman yksikköä kuvaavan arvon'''
        return self.yksikko_voima_value
    
    def onko_ulkoinen_voima_asetettu(self):
        '''Palauttaa tiedon onko ulkoinen voima asetettu'''
        return self.ulkoinen_voima_asetettu
    
    def materiaali(self, materiaali):
        '''tallentaa valitun materiaalin'''
        self.materiaali = materiaali
    
    def palauta_materiaali(self):
        '''Palauttaa materiaalin lukuarvon'''
        return self.materiaali
    
    def tuki(self, tyyppi):
        '''Tallentaa tuen tyyppiä kuvaavan arvon'''
        self.tuen_tyyppi = tyyppi
    
    def palauta_tuen_tyyppi(self):
        '''Palauttaa tuen tyyppiä kuvaavan lukuarvon'''
        return self.tuen_tyyppi
    
    def simulaation_tulos(self, arvo):
        '''Tallentaa simulaation tuloksen'''
        self.maksimi_jannitys = arvo
        
    def palauta_tulos(self):
        '''Palauttaa laskennan tuloksen'''
        return self.maksimi_jannitys
    