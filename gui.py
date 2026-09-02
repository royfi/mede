import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from berekeningen import alcoholPercentage, fruitMelomel, recepten, receptenBouwer


class Selectie(QDialog):
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

        alcohol.clicked.connect(alcoholPercentage)
        melomel.clicked.connect(fruitMelomel)
        recept.clicked.connect(recepten)
        recepten_maker.clicked.connect(receptenBouwer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    selectie = Selectie()
    selectie.show()
    sys.exit(app.exec())