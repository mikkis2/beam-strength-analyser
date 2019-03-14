'''
Created on 27.3.2018

@author: MJwork
'''
from ominaisuudet import Ominaisuudet

class Laskin():
    
    def laskin(self):
        '''Ladataan tarvittavat muuttujat'''
        sivun_pituus = 0.2 #Neliönmuotoisen palkin sivun pituus metreinä
        voima = float(Ominaisuudet.palauta_voima(self))
        pituus = float(Ominaisuudet.palauta_palkin_pituus(self))
        pituuden_yksikko = float(Ominaisuudet.palauta_pituuden_yksikko(self))
        voiman_yksikko = float(Ominaisuudet.palauta_voiman_yksikko(self))
        tuen_tyyppi = int(Ominaisuudet.palauta_tuen_tyyppi(self))
        ulkoinen_voima = int(Ominaisuudet.onko_ulkoinen_voima_asetettu(self))
        palkin_paino = pituus*sivun_pituus**2*7850*9.81*10**-3
    
        '''Asetetaan kertoimia yksikkömuunnosten tekemiseksi'''
        if voiman_yksikko == 0: 
            voimakerroin = 1000
        
        if voiman_yksikko == 1:     
            voimakerroin = 1 
            
        if pituuden_yksikko == 0: 
            pituuskerroin = 1 
            
        if pituuden_yksikko == 1: 
            pituuskerroin = 10**-2 
        
        if pituuden_yksikko == 2: 
            pituuskerroin = 10**-3 
        
        if tuen_tyyppi == 0:   
            '''Sivutuki''' 
            if ulkoinen_voima == 1:
                '''Ulkoinen voima asetettu'''
                maks_jannitys = ((6 * voima * pituus) / (sivun_pituus ** 3)*10**-6)*voimakerroin*pituuskerroin
                Ominaisuudet.simulaation_tulos(self, int(maks_jannitys))
            
            if ulkoinen_voima == 0:
                '''ulkoinen voima ei asetettu, 7850 teräksen tiheys''' 
                maks_jannitys = ((6 * palkin_paino * (pituus/2)) / (sivun_pituus ** 3)*10**-6)*voimakerroin*pituuskerroin 
                Ominaisuudet.simulaation_tulos(self, int(maks_jannitys))
                
        if tuen_tyyppi == 1: 
            '''Alatuki'''
            if ulkoinen_voima == 1:
                vastaus = (3/2) * ((voima*pituus) / (sivun_pituus**3)*10**-6)*voimakerroin*pituuskerroin
                Ominaisuudet.simulaation_tulos(self, int(vastaus))
            
            if ulkoinen_voima == 0: 
                vastaus = (3/2) * ((palkin_paino*pituus) / (sivun_pituus**3)*10**-6)*voimakerroin*pituuskerroin
                Ominaisuudet.simulaation_tulos(self, int(vastaus))