import sys
# from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QComboBox, QVBoxLayout, 
    QWidget, QHBoxLayout, QLabel
)
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
from tabThermal import tabThermal
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        cache = readCache()
        self.setWindowTitle("MyApp")
        # self.setFixedSize(QSize(400, 300))

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        ### layout choice
        ### layout choice drop down menu
        self.layoutChoiceDropdown = QComboBox()
        for layout in cache['layouts']:
            self.layoutChoiceDropdown.addItem(layout['name'])
        layoutChoice = QHBoxLayout()
        layoutChoice.addWidget(QLabel("layout"))
        layoutChoice.addWidget(self.layoutChoiceDropdown)

        ### different tabs
        tabs = QTabWidget()
        tabs.addTab(tabThermal(cache), "Thermal Input")

        mainLayout.addLayout(layoutChoice)
        mainLayout.addWidget(tabs)
        # self.setCentralWidget(self.layoutChoice)

def readCache():
    with open('cache.json', 'r') as file:
        try:
            return(json.load(file))
        except:
            return(dict())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()