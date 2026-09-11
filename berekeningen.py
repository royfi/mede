import pprint
import json
import sys
from datetime import datetime
from pathlib import Path
from bieb import BATCHES, GIST, SMAKEN

if getattr(sys, 'frozen', False):
    RECEPTEN_BESTAND = Path(sys.executable).resolve().with_name('recepten.json')
    RECEPTEN_BUNDEL = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / 'recepten.json'
else:
    RECEPTEN_BESTAND = Path(__file__).with_name('recepten.json')
    RECEPTEN_BUNDEL = RECEPTEN_BESTAND

if getattr(sys, 'frozen', False):
    BATCHES_BESTAND = Path(sys.executable).resolve().with_name('batches.json')
    BATCHES_BUNDEL = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / 'batches.json'
else:
    BATCHES_BESTAND = Path(__file__).with_name('batches.json')
    BATCHES_BUNDEL = BATCHES_BESTAND

RECEPTEN_BRON = RECEPTEN_BESTAND if RECEPTEN_BESTAND.exists() else RECEPTEN_BUNDEL #zorgt ervoor dat ik de receptenbibliotheek permanent kan opslaan.
if RECEPTEN_BRON.exists():
    with RECEPTEN_BRON.open(encoding='utf-8') as bestand:
        SMAKEN.update(json.load(bestand))

BATCHES_BRON = BATCHES_BESTAND if BATCHES_BESTAND.exists() else BATCHES_BUNDEL
if BATCHES_BRON.exists():
    with BATCHES_BRON.open(encoding='utf-8') as bestand:
        BATCHES.update(json.load(bestand))

karakterOpties = ('subtiel','gebalanceerd','intens')
categorieOpties = ('fruit', 'kruid', 'elders') #later evt meer opties toevoegen
gistOpties = tuple(GIST.keys())
smaakOpties = tuple(SMAKEN.keys())

def valideerDatum(datum):
    try:
        datetime.strptime(datum.strip(), '%d/%m/%Y')
    except (AttributeError, TypeError, ValueError):
        raise ValueError('Vul een geldige datum in als dd/MM/yyyy.')

    return datum.strip()

def slaBatchesOp():
    with BATCHES_BESTAND.open('w', encoding='utf-8') as bestand:
        json.dump(BATCHES, bestand, ensure_ascii=False, indent=4)

#def main():

def normaliseerDichtheid(dichtheid):
    min_dichtheid = 0.900
    ingevoerde_dichtheid = dichtheid

    if dichtheid > 2:
        dichtheid /= 1000

    if dichtheid <= min_dichtheid:
        if ingevoerde_dichtheid > 2:
            raise ValueError(f'Dichtheid moet hoger zijn dan {min_dichtheid * 1000:.0f}')
        raise ValueError(f'Dichtheid moet hoger zijn dan {min_dichtheid}')

    return dichtheid

def alcoholPercentage(start_dichtheid, eind_dichtheid):
    start_dichtheid = normaliseerDichtheid(start_dichtheid)
    eind_dichtheid = normaliseerDichtheid(eind_dichtheid)

    if eind_dichtheid > start_dichtheid:
        raise ValueError('Einddichtheid mag niet hoger zijn dan uw begin dichtheid.')
    #elif eind_dichtheid <= min_dichtheid or start_dichtheid <= min_dichtheid:
        

    return(start_dichtheid - eind_dichtheid)*131.25
    
def fruitMelomel(mede_volume, mede_smaak,karakter):
    
    try: 
        mede_volume = float(mede_volume)
    except (TypeError, ValueError):
        raise ValueError('Vul a.u.b. een getal in.')
    
    if mede_volume <= 0:
        raise ValueError('De hoeveelheid mede moet groter dan 0 zijn.')

    mede_smaak = mede_smaak.strip().title()

    if mede_smaak not in SMAKEN:
        raise ValueError('Kies een geldige smaak.')
    
     
    honing = (mede_volume / 100)*45
    smaakgegevens = SMAKEN[mede_smaak]
    ingrediënt_verhouding = honing * smaakgegevens['ingrediënt_verhouding']
    

    if karakter =='subtiel':
        ingrediënt_totaal = ingrediënt_verhouding * .5
    elif karakter =='gebalanceerd':
        ingrediënt_totaal = ingrediënt_verhouding
    elif karakter =='intens':
        ingrediënt_totaal = ingrediënt_verhouding * 1.33
   
    return honing, ingrediënt_totaal, karakter

    
def receptenBouwer(naam, verhoudingen, categorie, karakter, tijd, gist):
    naam = naam.strip().title()
    if not naam:
        raise ValueError('Vul een naam in.')

    try:
        ingrediënt_verhouding = float(verhoudingen)
        tijd = int(tijd)
    except (TypeError, ValueError):
        raise ValueError('Verhoudingen en tijd moeten getallen zijn.')

    if ingrediënt_verhouding <= 0:
        raise ValueError('De verhouding moet groter dan 0 zijn.')
    if tijd <= 0:
        raise ValueError('De tijd moet groter dan 0 zijn.')
    if categorie not in categorieOpties:
        raise ValueError('Kies een geldige categorie.')
    if karakter not in karakterOpties:
        raise ValueError('Kies een geldig smaakkarakter.')
    if gist not in GIST:
        raise ValueError('Kies een geldige gist.')

    SMAKEN[naam] = {
        'ingrediënt_verhouding': ingrediënt_verhouding,
        'categorie': categorie,
        'smaakKarakter': karakter,
        'smaakDuur': f'{tijd} dagen',
        'gistSleutel': gist,
    }

    with RECEPTEN_BESTAND.open('w', encoding='utf-8') as bestand:
        json.dump(SMAKEN, bestand, ensure_ascii=False, indent=4)

def honingBerekenen(): 
    pass

def batchBeheer():
    pass

def doelAbv(volume,abv, doel_dichtheid):
  
    try: 
        volume = float(volume)
        abv = float(abv)
        doel_dichtheid = float(doel_dichtheid)
    except (TypeError, ValueError):
        raise ValueError('Vul a.u.b. een getal in.')
 
   
    doel_dichtheid = normaliseerDichtheid(doel_dichtheid)
    max_abv = 25

    if abv >= max_abv:
        raise ValueError(f'Alcoholpercentage kan niet gelijk of hoger zijn dan {max_abv}%')
    
    start_dichtheid = abv / 131.25 + doel_dichtheid
    gravity_punten = (start_dichtheid - 1)*1000
    honing = ((gravity_punten*volume) / 292)

    
    return doel_dichtheid, start_dichtheid, gravity_punten, honing,

def medeRekenmachine():
    pass



