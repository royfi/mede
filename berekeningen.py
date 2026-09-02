import pprint
from bieb import SMAKEN

karakterOpties = ('subtiel','gebalanceerd','intens')
categorieOpties = ('fruit', 'kruid', 'elders') #later evt meer opties toevoegen

#def main():

def normaliseerDichtheid(dichtheid):
    if dichtheid > 2:
        dichtheid /= 1000
    return dichtheid

def alcoholPercentage(start_dichtheid, eind_dichtheid):
    start_dichtheid = normaliseerDichtheid(start_dichtheid)
    eind_dichtheid = normaliseerDichtheid(eind_dichtheid)
    if eind_dichtheid > start_dichtheid:
        raise ValueError('Einddichtheid mag niet hoger zijn dan uw begin dichtheid.')
    
    return(start_dichtheid - eind_dichtheid)*131.25
    
def fruitMelomel(mede_volume, mede_smaak):
    
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
    ingrediënt_verhouding = smaakgegevens['ingrediënt_verhouding']
    karakter = smaakgegevens['smaakKarakter']

    if karakter =='subtiel':
        ingrediënt_totaal = ingrediënt_verhouding * .5
    elif karakter =='gebalanceerd':
        ingrediënt_totaal = ingrediënt_verhouding
    elif karakter =='intens':
        ingrediënt_totaal = ingrediënt_verhouding * 1.33
   
    return honing, ingrediënt_totaal, karakter

def recepten():
    #niet echt een recept nu, moet later dit beter formateren, en echte receptenlijst geven. ipv de dictLijst. mss extra dict met recepten?
    #  or alleen belangrijke keys uit de dict pakken?
    print('Welke smaak uit de volgende lijst zou u het recept van willen inzien?')
    print(list(SMAKEN.keys()))
    smaak = input().strip().title()
    pprint.pprint(SMAKEN[smaak])
    
def receptenBouwer(naam, verhoudingen, categorie, karakter, tijd):
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

    SMAKEN[naam] = {
        'ingrediënt_verhouding': ingrediënt_verhouding,
        'categorie': categorie,
        'smaakKarakter': karakter,
        'smaakDuur': f'{tijd} dagen',
    }

#main()

