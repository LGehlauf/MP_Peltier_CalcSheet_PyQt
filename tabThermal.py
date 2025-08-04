from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem
)
import json

class tabThermal(QWidget):
    def __init__(self, cache):
        super().__init__()

        ### input parameter fields
        self.inArea = QLineEdit()
        self.inThickness = QLineEdit()
        self.inThermConduct = QLineEdit()

        self.inArea.setPlaceholderText("Area [mm]")
        self.inThickness.setPlaceholderText("Thickness [mm]")
        self.inThermConduct.setPlaceholderText("Thermal Conductivity [W/mK]")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inArea)
        inputLayout.addWidget(self.inThickness)
        inputLayout.addWidget(self.inThermConduct)

        ### add layer button
        self.buttonAddRow = QPushButton("Add Layer")
        self.buttonAddRow.clicked.connect(self.addRow)

        ### layer table
        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Area [mm]", "Thickness [mm]", "Thermal Conductivity [W/mK]"])

        ### save button
        self.buttonSaveLayout = QPushButton("Save Layout")
        self.buttonSaveLayout.clicked.connect(self.saveLayout)

        ### assembly
        layout = QVBoxLayout()
        layout.addLayout(inputLayout)
        layout.addWidget(self.buttonAddRow)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def addRow(self):
        area = self.inArea.text()
        thickness = self.inThickness.text()
        thermConduct = self.inThermConduct.text()
        for x in [area, thickness, thermConduct]:
            try:
                float(x)
            except:
                return
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(area))
        self.table.setItem(row, 1, QTableWidgetItem(thickness))
        self.table.setItem(row, 2, QTableWidgetItem(thermConduct))

        self.inArea.clear()
        self.inThickness.clear()
        self.inThermConduct.clear()

    def saveLayout():
        with open('cache.json', 'w') as file:
            pass
