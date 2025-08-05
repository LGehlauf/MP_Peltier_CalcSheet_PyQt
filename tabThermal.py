from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from PyQt6.QtSvgWidgets import QSvgWidget
import cairo

class TabThermal(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        ### input parameter fields
        self.inMaterial = QLineEdit()
        self.inArea = QLineEdit()
        self.inThickness = QLineEdit()
        self.inThermConduct = QLineEdit()
        self.inRowNum = QLineEdit()

        self.inMaterial.setPlaceholderText("Material")
        self.inArea.setPlaceholderText("Area [mm²]")
        self.inThickness.setPlaceholderText("Thickness [mm]")
        self.inThermConduct.setPlaceholderText("Thermal Conductivity [W/mK]")
        self.inRowNum.setPlaceholderText("Insert After Row")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inMaterial)
        inputLayout.addWidget(self.inArea)
        inputLayout.addWidget(self.inThickness)
        inputLayout.addWidget(self.inThermConduct)
        inputLayout.addWidget(self.inRowNum)

        ### add layer button
        self.buttonAddRow = QPushButton("Add Layer")
        self.buttonAddRow.clicked.connect(self.addRow)
        inputLayout.addWidget(self.buttonAddRow)

        ### layer table
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Material", "Area [mm²]", "Thickness [mm]", "Thermal Conductivity [W/mK]"])
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.rightClickOnTable)
        self.setThermalTable(layoutIndex=0)

        ### layer svg
        self.drawLayersSvg()
        self.svg = QSvgWidget("assets/thermal.svg")
        self.svg.setFixedSize(600, 100)

        ### layer assembly
        layerLayout = QHBoxLayout()
        layerLayout.addWidget(self.table)
        layerLayout.addWidget(self.svg)

        ### assembly
        assemblyLayout = QVBoxLayout()
        assemblyLayout.addLayout(inputLayout)
        assemblyLayout.addLayout(layerLayout)

        self.setLayout(assemblyLayout)

    def addRow(self):
        material = self.inMaterial.text()
        area = self.inArea.text()
        thickness = self.inThickness.text()
        thermConduct = self.inThermConduct.text()
        rowNum = self.inRowNum.text()
        for x in [area, thickness, thermConduct]:
            try:
                float(x)
            except:
                return
        try: 
            rowNum = int(rowNum)
        except:
            return
        if rowNum < 0 or rowNum > self.table.rowCount():
            return
        self.cache['layouts'][self.currentLayoutIndex]['thermalStructure'].insert( rowNum, 
            {'material': material, 'area': float(area), 'thickness': float(thickness), 'thermalConductivity': float(thermConduct)}
        )
        self.table.insertRow(rowNum)
        self.table.setItem(rowNum, 0, QTableWidgetItem(material))
        self.table.setItem(rowNum, 1, QTableWidgetItem(area))
        self.table.setItem(rowNum, 2, QTableWidgetItem(thickness))
        self.table.setItem(rowNum, 3, QTableWidgetItem(thermConduct))

        self.inMaterial.clear()
        self.inArea.clear()
        self.inThickness.clear()
        self.inThermConduct.clear()
        self.inRowNum.clear()

    def setThermalTable(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex
        self.table.clearContents()
        self.table.setRowCount(0)
        for layer in self.cache['layouts'][layoutIndex]['thermalStructure']:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, item in enumerate(layer.values()):
                self.table.setItem(row, i, QTableWidgetItem(str(item)))
    
    def rightClickOnTable(self, pos: QPoint):
        item = self.table.itemAt(pos)
        if item:
            menu = QMenu(self)

            deleteRowAction = QAction("Delete Row", self)
            deleteRowAction.triggered.connect(lambda _, r=item.row(): self.deleteRow(r))

            menu.addAction(deleteRowAction)
            menu.exec(self.table.viewport().mapToGlobal(pos))

    def deleteRow(self, rowNum):
        self.cache['layouts'][self.currentLayoutIndex]['thermalStructure'].pop(rowNum)
        self.table.removeRow(rowNum)

    def drawLayersSvg(self):
        layout = self.cache['layouts'][self.currentLayoutIndex]['thermalStructure']
        totalThickness = 20 + sum((5 * layer['thickness'] for layer in layout))
        with cairo.SVGSurface("assets/thermal.svg", totalThickness, 50) as surface:
            context = cairo.Context(surface)
            context.set_line_width(0.04)
            context.set_source_rgba(0.4, 1, 0.4, 1)
            for layer in layout:
                context.rectangle(10, 10, 40, layer['thickness']) # TODO: move next rectangle, dynamically changing painting
                context.stroke()

