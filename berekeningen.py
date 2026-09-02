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
    fruit = smaakgegevens['fruitBasis']
    karakter = smaakgegevens['smaakKarakter']

    if karakter =='subtiel':
        fruit_totaal = fruit * .5
    elif karakter =='gebalanceerd':
        fruit_totaal = fruit
    elif karakter =='intens':
        fruit_totaal = fruit * 1.33
   
    return honing, fruit_totaal, karakter

def recepten():
    #niet echt een recept nu, moet later dit beter formateren, en echte receptenlijst geven. ipv de dictLijst. mss extra dict met recepten?
    #  or alleen belangrijke keys uit de dict pakken?
    print('Welke smaak uit de volgende lijst zou u het recept van willen inzien?')
    print(list(SMAKEN.keys()))
    smaak = input().strip().title()
    pprint.pprint(SMAKEN[smaak])
    
def receptenBouwer(): 
    
    
    naam = input('Welk naam wilt u het recept geven?').strip().title()

    while True:
        try:
            fruitBasis = float(input('Hoeveel delen fruit wilt u per 1 deel honing toevoegen?'))
            break
        except ValueError:
            print('Vul alstublieft een getal in!')
                

    categorie = input(f'Welke categorie wilt u het recept onder opslaan? kies uit: {categorieOpties}')
    while categorie not in categorieOpties:
        categorie = input(f'Kies alstublieft een van de volgende opties. {categorieOpties}')

    karakter = input(f'Welk smaak karakter wilt u geven aan de drank? {karakterOpties}?')
    while karakter not in karakterOpties:
        karakter = input(f'Kies alstublieft een van de opties, {karakterOpties}')

    while True:
        try:
            tijd = int(input('Hoeveel dagen wilt u de smaak in secundaire fermentatie laten rijpen?'))
            break
        except ValueError:
            print('Vul alstublieft een heel getal in!')
    smaakDuur = f'{tijd} dagen'
    
    SMAKEN[naam] = {
        'fruitBasis': fruitBasis,
        'categorie': categorie,
        'smaakKarakter': karakter,
        'smaakDuur': smaakDuur,
    }

    pprint.pprint(SMAKEN[naam])

#main()

