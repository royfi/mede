import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton , QLineEdit, QLabel, QMessageBox
from berekeningen import alcoholPercentage, fruitMelomel, recepten, receptenBouwer

def open_menu(dialog):
    dialog.close()
    menu = SelectieDialog()
    menu.exec()

def knop_toevoegen(layout, dialog):
    knop_menu = QPushButton('Menu')
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
        recept = QPushButton("Zie uw recepten in.")
        recepten_maker = QPushButton("Voeg nieuwe recepten toe.")

        layout.addWidget(alcohol)
        layout.addWidget(melomel)
        layout.addWidget(recept)
        layout.addWidget(recepten_maker)

    
        alcohol.clicked.connect(self.open_alcohol_dialog)


        melomel.clicked.connect(self.run_melomel)
        recept.clicked.connect(self.run_recept)
        recepten_maker.clicked.connect(self.run_recepten_maker)

    def open_alcohol_dialog(self):
        self.close()
        dialog = AlcoholDialog()
        dialog.exec()
        
    def run_melomel(self):
        self.close()
        fruitMelomel()
        
    def run_recept(self):
        self.close()
        recepten()
        
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

        layout.addWidget(QLabel('Voer uw begin dichtheid / gravity in'))
        layout.addWidget(self.start_input)

        layout.addWidget(self.end_input)

        knop = QPushButton('Bereken uw percentage')
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

        QMessageBox.information(self, 'Resultaat: ',f'Uw verwachte alcoholpercentage is {abv:.2f}%')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    selectie = SelectieDialog()
    selectie.show()
    sys.exit(app.exec())
    