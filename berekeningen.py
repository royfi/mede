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
    
def fruitMelomel():
    
    while True:
        try:
            medeVolume = float(input('Hoeveel liter aan mede wilt u maken?'))
            break
        except ValueError:
            print('Vul alstublieft een getal in')
    
    honing = (medeVolume / 100)*45
    
    smaken = [smaak.title() for smaak in SMAKEN.keys()]
    print(smaken)
    medeSmaak = input('Van welke smaak uit de volgende lijst wilt u het recept zien?').strip().title()
    
  

    while medeSmaak not in SMAKEN.keys():
        medeSmaak = input(f'Kies een van de smaken uit de lijst {smaken}: ').strip().title()

    melomel = SMAKEN[medeSmaak]['smaakKarakter']
    fruit = SMAKEN[medeSmaak]['fruitBasis']

    if melomel =='subtiel':
        fruitTotaal = fruit * .5
    elif melomel =='gebalanceerd':
        fruitTotaal = fruit
    elif melomel =='intens':
        fruitTotaal = fruit * 1.33
    else:
        print('Gebruik een van de aangeboden opties.')
        return
    
    print(f'Voor uw melomel wordt {honing}kg aan honing aangeraden, en {fruitTotaal}kg aan {medeSmaak} voor een totale hoeveelheid van {medeVolume}L aan mede, voor een {melomel}e smaak')

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

