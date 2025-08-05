from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem
)
import json

class TabThermal(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache

        ### input parameter fields
        self.inMaterial = QLineEdit()
        self.inArea = QLineEdit()
        self.inThickness = QLineEdit()
        self.inThermConduct = QLineEdit()

        self.inMaterial.setPlaceholderText("Material")
        self.inArea.setPlaceholderText("Area [mm²]")
        self.inThickness.setPlaceholderText("Thickness [mm]")
        self.inThermConduct.setPlaceholderText("Thermal Conductivity [W/mK]")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inMaterial)
        inputLayout.addWidget(self.inArea)
        inputLayout.addWidget(self.inThickness)
        inputLayout.addWidget(self.inThermConduct)

        ### add layer button
        self.buttonAddRow = QPushButton("Add Layer")
        self.buttonAddRow.clicked.connect(self.addRow)

        ### layer table
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Material", "Area [mm²]", "Thickness [mm]", "Thermal Conductivity [W/mK]"])
        self.setThermalTable(0)

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

    def setThermalTable(self, layoutIndex):
        self.table.clearContents()
        self.table.setRowCount(0)
        for layer in self.cache['layouts'][layoutIndex]['thermalStructure']:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, item in enumerate(layer.values()):
                self.table.setItem(row, i, QTableWidgetItem(str(item)))

