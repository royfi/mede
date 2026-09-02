import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton , QLineEdit, QLabel, QMessageBox, QComboBox
from berekeningen import alcoholPercentage, fruitMelomel, recepten, receptenBouwer
from bieb import SMAKEN

def open_menu(dialog):
    dialog.close()
    menu = SelectieDialog()
    menu.exec()

def knop_toevoegen(layout, dialog):
    knop_menu = QPushButton('Menu')
    #setAutoDefault(False) zorgt ervoor dat knop niet automatisch terug gaat naar het SelectieDialog als men enter indruk
    knop_menu.setAutoDefault(False)
    #lambda _checked=False: is ervoor om te zorgen dat de vensters niet gelijk sluiten, maar alleen als de knop is ingedrukt, snap niet hoe het werkt, maar het werkt.
    knop_menu.clicked.connect(lambda _checked=False: open_menu(dialog)) 

    layout.addWidget(knop_menu)
    return knop_menu

class SelectieDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")

        layout = QVBoxLayout(self)

        alcohol = QPushButton("Alcoholpercentage berekenen.")
        melomel = QPushButton("Bereken de verhoudingen van uw fruitmelomel.")
        #recept = QPushButton("Zie uw recepten in.")
        recepten_maker = QPushButton("Voeg nieuwe recepten toe.")

        layout.addWidget(alcohol)
        layout.addWidget(melomel)
       # layout.addWidget(recept)
        layout.addWidget(recepten_maker)

    
        alcohol.clicked.connect(self.open_alcohol)


        melomel.clicked.connect(self.open_melomel)
       # recept.clicked.connect(self.run_recept)
        recepten_maker.clicked.connect(self.run_recepten_maker)

    def open_alcohol(self):
        self.close()
        dialog = AlcoholDialog()
        dialog.exec()
        
    def open_melomel(self):
        self.close()
        dialog = MelomelDialog()
        dialog.exec()
        
    '''def run_recept(self):
        self.close()
        recepten()
    '''    
    def run_recepten_maker(self):
        self.close()
        receptenBouwer()
    

class AlcoholDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bereken uw alcohol percentage')

        layout = QVBoxLayout(self)

        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        self.start_input.returnPressed.connect(self.end_input.setFocus) # zorgt ervoor dat de cursor naar het volgende inputform gaat. zet de focus op end_input. 
        self.end_input.returnPressed.connect(self.run_alcohol)

        layout.addWidget(QLabel('Voer uw begin dichtheid / gravity in'))
        layout.addWidget(self.start_input)

        layout.addWidget(self.end_input)

        knop = QPushButton('Bereken uw percentage')
        knop.setAutoDefault(False) #zorgt ervoor dat mijn knop bij enter niet gelijk teruggaat naar het keuze menu.
        knop.clicked.connect(self.run_alcohol)
        layout.addWidget(knop)

        knop_menu = knop_toevoegen(layout, self)

    def run_alcohol(self):
        
        try:
            start = float(self.start_input.text())
            einde = float(self.end_input.text())
            abv = alcoholPercentage(start, einde)
        except ValueError as e:
            QMessageBox.warning(self, 'Fout', str(e))
            return

        QMessageBox.information(self, 'Resultaat: ',f'Uw verwachte alcoholpercentage is {abv:.2f}%')

class MelomelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fruitmelomel")

        layout = QVBoxLayout(self)
        
        self.volume_input = QLineEdit()
        self.smaak_input = QComboBox()
        self.smaak_input.addItems(SMAKEN.keys())
        
        layout.addWidget(QLabel('Hoeveel liter mede wilt u maken?'))
        layout.addWidget(self.volume_input)
        layout.addWidget(self.smaak_input)

        knop = QPushButton('Krijg uw verhouden voor uw fruitmelomels.')
        knop.clicked.connect(self.run_melomel)
        layout.addWidget(knop)
        
        knop_menu = knop_toevoegen(layout,self)


    def run_melomel(self):
    
        volume = self.volume_input.text()
        smaak = self.smaak_input.currentText()
        try:
           honing, fruit, karakter = fruitMelomel(volume,smaak)
        except ValueError as error:
            QMessageBox.warning(self, 'Fout', str(error))

        if fruit <= 1:
            fruit = fruit * 1000
            QMessageBox.information(
            self,
            'Resultaat',
            f'Honing: {honing:.2f} kg\n'
            f'Fruit: {fruit:.0f} gr\n'
            f'Smaak: {karakter}'
            )
        else:
            QMessageBox.information(
            self,
            'Resultaat',
            f'Honing: {honing:.2f} kg\n'
            f'Fruit: {fruit:.2f} kg\n'
            f'Smaak: {karakter}'
            )
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    selectie = SelectieDialog()
    selectie.show()
    sys.exit(app.exec())
