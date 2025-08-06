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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cache = self.readCache()
        self.setWindowTitle("MyApp")
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
        tabThermal = TabThermal(self.cache)
        tabElectrical = TabElectrical(self.cache)
        tabOutput = TabOutput(self.cache)
        tabs.addTab(tabOutput, "Output")
        tabs.addTab(tabThermal, "Thermal Structure")
        tabs.addTab(tabElectrical, "Electrical Structure")
        self.layoutChoiceDropdown.activated.connect(tabThermal.setTable) # dropdown menu tells current layout index
        self.layoutChoiceDropdown.activated.connect(tabThermal.drawLayersSvg) 
        self.layoutChoiceDropdown.activated.connect(tabThermal.setOutput) 
        self.layoutChoiceDropdown.activated.connect(tabElectrical.setTable) 
        self.layoutChoiceDropdown.activated.connect(tabElectrical.displayNumReps) 
        self.layoutChoiceDropdown.activated.connect(tabElectrical.setOutput) 
        self.layoutChoiceDropdown.activated.connect(tabOutput.drawSankeySvg) 

        mainLayout.addLayout(layoutChoice)
        mainLayout.addWidget(tabs)
        # self.setCentralWidget(self.layoutChoice)

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
app.exec()