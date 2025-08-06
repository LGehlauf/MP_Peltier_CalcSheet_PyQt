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

        ### layer assembly
        self.layerLayout = QHBoxLayout()

        ### layer table
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Material", "Area [mm²]", "Thickness [mm]", "Thermal Conductivity [W/mK]"])
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.rightClickOnTable)
        self.setThermalTable(layoutIndex=0)

        ### layer svg
        self.svg = QSvgWidget("assets/thermal.svg")
        self.drawLayersSvg(self.currentLayoutIndex)

        ### layer assembly
        self.layerLayout.addWidget(self.table)
        self.layerLayout.addWidget(self.svg)

        ### assembly
        assemblyLayout = QVBoxLayout()
        assemblyLayout.addLayout(inputLayout)
        assemblyLayout.addLayout(self.layerLayout)

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

        self.drawLayersSvg(self.currentLayoutIndex)

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
        self.drawLayersSvg(self.currentLayoutIndex)

    def drawLayersSvg(self, layoutIndex):
        totalWidth = 100
        # height should corresponding to the number of table rows
        # svgHeight = 50 * len(self.cache['layouts'][self.currentLayoutIndex]['thermalStructure'])
        svgHeight = 100
        self.svg.setFixedSize(totalWidth, svgHeight)
        self.currentLayoutIndex = layoutIndex
        colors = [
            (1.0, 0.701, 0.729),   # Pastellrosa
            (1.0, 0.874, 0.729),   # Pastellorange
            (1.0, 1.0, 0.729),     # Pastellgelb
            (0.729, 1.0, 0.788),   # Pastellgrün
            (0.729, 0.882, 1.0),   # Pastellblau
            (0.855, 0.729, 1.0),   # Pastelllila
            (1.0, 0.729, 0.945),   # Pastellmagenta
            (0.729, 1.0, 1.0),     # Pastelltürkis
            (0.941, 0.941, 0.941), # Hellgrau / Weißpastell
            (1.0, 0.8, 0.898),     # Zartes Rosa
        ]
        layout = self.cache['layouts'][self.currentLayoutIndex]['thermalStructure']
        totalHeight = sum((5 * layer['thickness'] for layer in layout))
        # canvas should be square
        with cairo.SVGSurface("assets/thermal.svg", totalHeight, totalHeight) as surface:
            context = cairo.Context(surface)
            cumuThickness = 0
            for i, layer in enumerate(layout):
                r = colors[i%len(colors)][0]
                g = colors[i%len(colors)][1]
                b = colors[i%len(colors)][2]
                context.set_source_rgba(r, g, b, 1)
                context.rectangle(2, 2 + cumuThickness, totalWidth, 5 * layer['thickness'])
                cumuThickness += 5 * layer['thickness']
                context.fill()
        self.svg.load("assets/thermal.svg")

