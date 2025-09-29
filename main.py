import sys
# from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QComboBox, QVBoxLayout, 
    QWidget, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
from tabThermal import TabThermal
from tabElectrical import TabElectrical
from tabOutput import TabOutput
import json
import tempfile
import os

# from PyQt6.QtGui import QPixmap # for making HQ screenshots

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentLayoutIndex = 0
        self.cache = self.readCache()
        self.setWindowTitle("Thermoelectric Calculator")
        # self.setFixedSize(QSize(400, 300))

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        ### layout choice
        layoutChoice = QHBoxLayout()
        ### layout choice drop down menu
        self.layoutChoiceDropdown = QComboBox()
        for layout in self.cache['layouts']:
            self.layoutChoiceDropdown.addItem(layout['name'])
        ### save button
        self.buttonSaveLayout = QPushButton("Save All Layouts")
        self.buttonSaveLayout.clicked.connect(self.saveCache)
        ### label + assembly
        layoutChoice.addWidget(QLabel("Layout: ", alignment = Qt.AlignmentFlag.AlignCenter))
        layoutChoice.addWidget(self.layoutChoiceDropdown)
        layoutChoice.addWidget(self.buttonSaveLayout)

        ### different tabs
        tabs = QTabWidget()
        self.tabThermal = TabThermal(self.cache)
        self.tabElectrical = TabElectrical(self.cache)
        self.tabOutput = TabOutput(self.cache)
        tabs.addTab(self.tabOutput, "Output")
        tabs.addTab(self.tabThermal, "Thermal Structure")
        tabs.addTab(self.tabElectrical, "Electrical Structure")
        tabs.setCurrentIndex(0)
        tabs.currentChanged.connect(self.activateTab)
        self.layoutChoiceDropdown.activated.connect(self.setCurrentLayoutIndexUpdateTabs)

        mainLayout.addLayout(layoutChoice)
        mainLayout.addWidget(tabs)

    def setCurrentLayoutIndexUpdateTabs(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex

        self.tabOutput.createPlots(layoutIndex)

        self.tabThermal.setTable(layoutIndex)
        self.tabThermal.drawLayersSvg(layoutIndex)
        self.tabThermal.setOutput(layoutIndex)

        self.tabElectrical.setTable(layoutIndex)
        self.tabElectrical.displayNumReps(layoutIndex)
        self.tabElectrical.displaySeebeckCoeff(self.currentLayoutIndex)
        self.tabElectrical.setOutput(layoutIndex)

    def activateTab(self, tabIndex):
        if tabIndex == 0:
            self.tabOutput.createPlots(self.currentLayoutIndex)
        elif tabIndex == 1:
            self.tabThermal.setTable(self.currentLayoutIndex)
            self.tabThermal.drawLayersSvg(self.currentLayoutIndex)
            self.tabThermal.setOutput(self.currentLayoutIndex)
        elif tabIndex == 2:
            self.tabElectrical.setTable(self.currentLayoutIndex)
            self.tabElectrical.displayNumReps(self.currentLayoutIndex)
            self.tabElectrical.displaySeebeckCoeff(self.currentLayoutIndex)
            self.tabElectrical.setOutput(self.currentLayoutIndex)

    def readCache(self):
        with open('cache.json', 'r') as file:
            try:
                return(json.load(file))
            except:
                return(dict())

    def saveCache(self):
        try:
            dirName = os.path.dirname(os.path.abspath('cache.json'))
            with tempfile.NamedTemporaryFile('w', dir=dirName, delete=False) as file:
                json.dump(self.cache, file, indent=4)

            # so far no exceptions -> writing was successful
            os.replace(file.name, 'cache.json')

        except Exception as e:
            print(f"saving did not work: {e}")

    

app = QApplication(sys.argv)
window = MainWindow()
window.show()

# pixmap = window.grab() # for making HQ screenshots
# scaled = pixmap.scaled(16800, 10000)
# scaled.save("output.png")

app.exec()
