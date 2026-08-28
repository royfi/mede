medeDict = { #deze is voor later, ik wil de functie fruitMelomel deze laten gebruiken in de GUI ipv zelf invullen via input(), via een dropdown menu oid. 
    "smaken": {
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

    print('Wat is uw begin dichtheid?') 
    startDichtheid = float(input())
    print('Wat is uw eind dichtheid?')
    eindDichtheid = float(input())
    AlcoholPercentage(startDichtheid, eindDichtheid)
    fruitMelomel() 

def AlcoholPercentage(startDichtheid,eindDichtheid):
    # test toevoegen, dat ik ook 1050 kan invoeren, en niet alleen 1.050 voor juiste hoeveelheid
    abv = (startDichtheid - eindDichtheid)*131.25 
    procent = f'{abv:.2f}%'
    print(f'Als uw begin dichtheid {startDichtheid} is en uw eind dichtheid {eindDichtheid} dan is uw alcohol percentage {procent}')

def fruitMelomel():
    print('Hoeveel liter aan mede wilt u maken?')
    mede = float(input())
    honing = (mede / 100)*45

    print('Wat voor melomel zou u willen maken, subtiel, gebalanceerd of intens?')
    melomel = input()
    fruitBasis = honing*1.5
# later dit doen via dictionary, en de fruitBasis daarvan halen, zodat elke smaak zijn eigen formule heeft
    if melomel =='subtiel':
        fruitTotaal = fruitBasis * .5
    elif melomel =='gebalanceerd':
        fruitTotaal = fruitBasis
    elif melomel =='intens':
        fruitTotaal = fruitBasis * 1.33
    else:
        print('Gebruik een van de aangeboden opties.')
        return
    # Later een optie toevoegen om ook te kiezen of er tijdens primaire en/of secundaire fermentatie fruit toegevoegd wordt, bepalen hoeveel fruit er dan nodig is in beide rondes
    
    print(f'Voor uw melomel wordt {honing}kg aan honing aangeraden, en {fruitTotaal}kg aan fruit voor een totale hoeveelheid van {mede}L aan mede')



main()
   
