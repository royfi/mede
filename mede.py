from PySide6.QtWidgets import QApplication, QWidget
import pprint

karakterOpties = ('subtiel','gebalanceerd','intens')
categorieOpties = ('fruit', 'kruid', 'elders') #later evt meer opties toevoegen



medeDict = { 
    'smaken': {
        "kers": {
            'fruitBasis':2.5, #fruitbasis gaat uit van per 4kg mede (of ~1 Gallon)
            'categorie':'fruit',
            'smaakKarakter':'gebalanceerd',
            'smaakDuur':'14 dagen', #smaakDuur is hoelang de smaakmaker in de mede moet blijven om z'n smaak te onttrekken.
        },
        "munt": {
            'fruitBasis':.25,
            'categorie':'kruid',
            'smaakKarakter':'subtiel',
            'smaakDuur':'5 dagen'
        }
    },

    "gist": { #Nog kijken wat ik hier later mee ga doen, mss alleen om recepten uit te printen
        "71B": {
            "maxAbv": 14,
            "tempMin": 15,
            "tempMax": 30,
            "gistType": 'Droge wijn, mede',
            'smaakProfiel':'fruitig, minder zuur',
        }
    }
}


def main():

  
    alcoholPercentage()
    fruitMelomel() 
    #recepten()

def alcoholPercentage():
    # test toevoegen, dat ik ook 1050 kan invoeren, en niet alleen 1.050 voor juiste hoeveelheid\
    while True:
        try:
            startDichtheid = float(input('Wat is uw begin dichtheid / gravity?'))
            eindDichtheid = float(input('Wat is uw eind dichtheid / gravity?'))
            break
        except ValueError:
            print('Vul bij beide alstublieft een getal in!')

    abv = (startDichtheid - eindDichtheid)*131.25 
    procent = f'{abv:.2f}%'
    print(f'Als uw begin dichtheid {startDichtheid} is en uw eind dichtheid {eindDichtheid} dan is uw alcohol percentage {procent}')

def fruitMelomel():
    
    while True:
        try:
            medeVolume = float(input('Hoeveel liter aan mede wilt u maken?'))
            break
        except ValueError:
            print('Vul alstublieft een getal in')
    
    honing = (medeVolume / 100)*45
    
    print('Van welke smaak uit de volgende lijst zou u het recept in van willen zien?')
    print(list(medeDict["smaken"].keys()))
    medeSmaak = input()

    while medeSmaak not in medeDict['smaken'].keys():
        medeSmaak = input(f'Kies een van de smaken uit de lijst{list(medeDict['smaken'].keys)}')

    melomel = medeDict['smaken'][medeSmaak]['smaakKarakter']
    fruit = medeDict['smaken'][medeSmaak]['fruitBasis']

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
    print('Welke smaak uit de volgende lijst zou u het recept van willen inzien?')
    print(list(medeDict["smaken"].keys()))
    smaak = input()
    pprint.pprint(medeDict["smaken"][smaak])
    
def receptenBouwer():
    
    naam = input('Welk naam wilt u het recept geven?')
    
    while True:
        try:
            fruitBasis = float(input('Wat is de fruitbasis?'))
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
    
    medeDict['smaken'][naam] = {
        'fruitBasis': fruitBasis,
        'categorie': categorie,
        'smaakKarakter': karakter,
        'smaakDuur': smaakDuur,
    }

    pprint.pprint(medeDict['smaken'][naam])
    


#main()
#alcoholPercentage()
#fruitMelomel()
#recepten() 
receptenBouwer() 
fruitMelomel()

