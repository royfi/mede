import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton , QLineEdit, QLabel, QMessageBox, QComboBox
from berekeningen import (
    alcoholPercentage,
    categorieOpties,
    karakterOpties,
    gistOpties,
    fruitMelomel,
    receptenBouwer,
    doelAbv
)
from bieb import SMAKEN

def open_menu(dialog):
    dialog.close()
    menu = SelectieDialog()
    menu.exec()

def knop_toevoegen(layout, dialog, actieknop=None):
    knoppen_layout = QHBoxLayout()

    if actieknop is not None:
        knoppen_layout.addWidget(actieknop)

    knop_menu = QPushButton('Menu')
    #setAutoDefault(False) zorgt ervoor dat knop niet automatisch terug gaat naar het SelectieDialog als men enter indruk
    knop_menu.setAutoDefault(False)
    #lambda _checked=False: is ervoor om te zorgen dat de vensters niet gelijk sluiten, maar alleen als de knop is ingedrukt, snap niet hoe het werkt, maar het werkt.
    knop_menu.clicked.connect(lambda _checked=False: open_menu(dialog)) 

    knoppen_layout.addWidget(knop_menu) # zorgt ervoor dat bij meerdere knoppen ze naast elkaar terecht komen, ipv onder elkaar
    layout.addLayout(knoppen_layout) 
    return knop_menu

class SelectieDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")

        layout = QVBoxLayout(self)

        alcohol = QPushButton("Alcoholpercentage berekenen.")
        melomel = QPushButton("Bereken de verhoudingen van uw fruitmelomel.")
        recept = QPushButton("Zie uw recepten in.")
        recepten_maker = QPushButton("Voeg nieuwe recepten toe.")
        doel_abv = QPushButton('Bereken hoe u uw doel alcohol percentage kan bereiken.')

        layout.addWidget(alcohol)
        layout.addWidget(melomel)
        layout.addWidget(recept)
        layout.addWidget(recepten_maker)
        layout.addWidget(doel_abv)

    
        alcohol.clicked.connect(self.open_alcohol)
        melomel.clicked.connect(self.open_melomel)
        recept.clicked.connect(self.run_recept)
        recepten_maker.clicked.connect(self.run_recepten_maker)
        doel_abv.clicked.connect(self.open_doel_abv)

    def open_alcohol(self):
        self.close()
        dialog = AlcoholDialog()
        dialog.exec()
        
    def open_melomel(self):
        self.close()
        dialog = MelomelDialog()
        dialog.exec()
        
    def open_doel_abv(self):
        self.close()
        dialog = DoelAbvDialog()
        dialog.exec()

    def run_recept(self):
        self.close()
        dialog = ReceptenDialog()
        dialog.exec()
    
    def run_recepten_maker(self):
        self.close()
        dialog = BouwerDialog()
        dialog.exec()
    
class AlcoholDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bereken uw alcohol percentage')

        layout = QVBoxLayout(self)

        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        self.start_input.returnPressed.connect(self.end_input.setFocus) # zorgt ervoor dat de cursor naar het volgende inputform gaat. zet de focus op end_input. 
        self.end_input.returnPressed.connect(self.run_alcohol)

        layout.addWidget(QLabel('Bereken uw alcohol percentage aan de hand van uw gemeten dichtheid / gravity met uw hydrometer. \n'))

        layout.addWidget(QLabel('Voer uw begin dichtheid / gravity in.'))
        layout.addWidget(self.start_input)

        layout.addWidget(QLabel('Voer uw eind dichtheid / gravity in.'))
        layout.addWidget(self.end_input)

        knop = QPushButton('Bereken uw percentage')
        knop.setAutoDefault(False) #zorgt ervoor dat mijn knop bij enter niet gelijk teruggaat naar het keuze menu.
        knop.clicked.connect(self.run_alcohol)
        knop_menu = knop_toevoegen(layout, self, knop)

    def run_alcohol(self):
        
        try:
            start = float(self.start_input.text())
            einde = float(self.end_input.text())
            abv = alcoholPercentage(start, einde)
        except ValueError as e:
            QMessageBox.warning(self, 'Fout', str(e))
            return

        QMessageBox.information(self, 'Resultaat: ',f'Uw verwachte alcoholpercentage is {abv:.2f}%')

class DoelAbvDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bereken uw start dichtheid.')

        layout = QVBoxLayout(self)
       
        self.volume_input = QLineEdit()
        self.abv_input = QLineEdit()
        self.dichtheid_input = QLineEdit()
        self.abv_input.returnPressed.connect(self.dichtheid_input.setFocus) # zorgt ervoor dat de cursor naar het volgende inputform gaat. zet de focus op end_input. 
        self.dichtheid_input.returnPressed.connect(self.run_abv)


        layout.addWidget(QLabel('Bereken de dichtheid waarmee u moet beginnen als u een bepaald alcoholpercentage wilt bereiken, a.h.v. uw verwachte eind dichtheid.'))

        layout.addWidget(QLabel('Hoeveel liter mede wilt u maken?'))
        layout.addWidget(self.volume_input)

        layout.addWidget(QLabel('Voer uw gewenste alcohol percentage in.'))
        layout.addWidget(self.abv_input)

        layout.addWidget(QLabel('Voer uw verwachte eind dichtheid in.')) #later vervangen door gist bieb
        layout.addWidget(self.dichtheid_input)

        knop = QPushButton('Bereken uw benodigde start dichtheid.')
        knop.setAutoDefault(False) #zorgt ervoor dat mijn knop bij enter niet gelijk teruggaat naar het keuze menu.
        knop.clicked.connect(self.run_abv)
        knop_menu = knop_toevoegen(layout, self, knop)

    def run_abv(self):
        try:
            volume = (self.volume_input.text())
            abv = (self.abv_input.text())
            e_dichtheid = (self.dichtheid_input.text())
            e_dichtheid,d_dichtheid,g_punten, honing = doelAbv(volume, abv, e_dichtheid)
        except ValueError as e:
            QMessageBox.warning(self, 'Fout', str(e))
            return

        QMessageBox.information(self, 
        'Resultaat',
        f'Uw gewenste volume: {volume}L \n'
        f'Gewenste alcoholpercentage: {abv}% \n'
        f'Uw benodigde begin dichtheid: {d_dichtheid:.3f}\n'
        f'Uw verwachte eind dichtheid: {e_dichtheid:.3f} \n'
        f'Uw gravitypunten zijn: {g_punten:.0f}\n'
        f'Uw benodigde honing (in kg): {honing:.2f}kg'
        
        )

class MelomelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fruitmelomel")

        layout = QVBoxLayout(self)
        
        self.volume_input = QLineEdit()
        self.smaak_input = QComboBox()
        self.smaak_input.addItems(SMAKEN.keys())
        self.karakter_input =QComboBox()
        self.karakter_input.addItems(karakterOpties)
        
        layout.addWidget(QLabel('Hoeveel liter mede wilt u maken?'))
        layout.addWidget(self.volume_input)
        layout.addWidget(self.smaak_input)
        layout.addWidget(QLabel('Welk smaakprofiel wilt u aan uw mede geven?'))
        layout.addWidget(self.karakter_input)

       

        knop = QPushButton('Krijg uw verhouden voor uw fruitmelomels.')
        knop.clicked.connect(self.run_melomel)
        knop_menu = knop_toevoegen(layout, self, knop)


    def run_melomel(self):
    
        volume = self.volume_input.text()
        smaak = self.smaak_input.currentText()
        karakter = self.karakter_input.currentText()
        try:
           honing, fruit, karakter = fruitMelomel(volume,smaak,karakter)
        except ValueError as error:
            QMessageBox.warning(self, 'Fout', str(error))
            return

        if fruit <= 1:
            fruit = fruit * 1000
            QMessageBox.information(
            self,
            'Resultaat',
            f'Honing: {honing:.2f} kg\n'
            f'{smaak}: {fruit:.0f} gr\n'
            f'Smaak: {karakter}'
            )
        else:
            QMessageBox.information(
            self,
            'Resultaat',
            f'Honing: {honing:.2f} kg\n'
            f'{smaak}: {fruit:.2f} kg\n'
            f'Smaak: {karakter}'
            )

class ReceptenDialog(QDialog):
    veld_namen = {
        'categorie': 'Categorie',
        'smaakKarakter': 'Smaak karakter',
        'smaakDuur': 'secundaire fermentatie',
        'gistSleutel': 'Gist',
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recepten Bibliotheek")

        layout = QVBoxLayout(self)

        self.recept_input = QComboBox()
        self.recept_input.addItems(list(SMAKEN.keys()))

        layout.addWidget(QLabel('Van welke smaak wilt u het recept inzien?'))
        layout.addWidget(self.recept_input)

        self.recept_resultaat = QLabel()
        layout.addWidget(self.recept_resultaat)

        knop = QPushButton('Recept bekijken')
        knop.clicked.connect(self.run_recept)
        knop_menu = knop_toevoegen(layout, self, knop)

    def run_recept(self):
        smaak = self.recept_input.currentText()
        recept = SMAKEN[smaak]

        tekst = '\n'.join(
            f'{self.veld_namen.get(sleutel, sleutel)}: {waarde}'
            for sleutel, waarde in recept.items()
            if sleutel != 'ingrediënt_verhouding'
        )
        self.recept_resultaat.setText(tekst)



class BouwerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recepten Maker")

        layout = QVBoxLayout(self)

        self.naam_input = QLineEdit()
        self.verhoudingen_input = QLineEdit()
        self.categorie_input = QComboBox()
        self.categorie_input.addItems(categorieOpties)
        self.karakter_input = QComboBox()
        self.karakter_input.addItems(karakterOpties)
        self.tijd_input = QLineEdit()
        self.gist_input = QComboBox()
        self.gist_input.addItems(gistOpties)

        layout.addWidget(QLabel('Welke naam wilt u het recept geven?'))
        layout.addWidget(self.naam_input)

        layout.addWidget(QLabel('Met welke factor wilt u uw fruit / kruiden vermenigvuldigen t.o.v. uw honing?'))
        layout.addWidget(self.verhoudingen_input)

        layout.addWidget(QLabel('Welke categorie wilt u de drank bij indelen?'))
        layout.addWidget(self.categorie_input)

        layout.addWidget(QLabel('Welk karakter wilt u de drank geven?'))
        layout.addWidget(self.karakter_input)

        layout.addWidget(QLabel('Hoe lang wilt u de ingrediënten toevoegen aan secundaire fermentatie?'))
        layout.addWidget(self.tijd_input)

        layout.addWidget(QLabel('Welk type gist wilt u gebruiken?'))
        layout.addWidget(self.gist_input)

        knop = QPushButton('Recept opslaan')
        knop.clicked.connect(self.run_bouwer)
        knop_menu = knop_toevoegen(layout, self, knop)

    def run_bouwer(self):
        try:
            receptenBouwer(
                self.naam_input.text(),
                self.verhoudingen_input.text(),
                self.categorie_input.currentText(),
                self.karakter_input.currentText(),
                self.tijd_input.text(),
                self.gist_input.currentText(),
            )
        except ValueError as error:
            QMessageBox.warning(self, 'Fout', str(error))
            return

        QMessageBox.information(self, 'Opgeslagen', 'Het recept is opgeslagen.')
        open_menu(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    selectie = SelectieDialog()
    selectie.show()
    sys.exit(app.exec())
