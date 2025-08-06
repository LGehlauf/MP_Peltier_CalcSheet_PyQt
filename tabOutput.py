from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel,QHeaderView
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from PyQt6.QtSvgWidgets import QSvgWidget
import cairo

class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        self.drawSankeySvg(self.currentLayoutIndex)

        assemblyLayout = QHBoxLayout()
        assemblyLayout.addWidget(self.svg)
        self.setLayout(assemblyLayout)


    def drawSankeySvg(self, layoutIndex): # TODO: Research peltier coefficient find out if P_el = P_R + P_P.E.
        self.currentLayoutIndex = layoutIndex
        layoutName = self.cache['layouts'][layoutIndex]['name']
        svgWidth, svgHeight = 500, 500
        bgWidth, bgHeight = 250, 250
        self.svg.setFixedSize(bgWidth, bgHeight)
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
            (1.0, 0.8, 0.898)      # Zartes Rosa
        ]
        structure = self.cache['layouts'][self.currentLayoutIndex]['thermalStructure']
        structureHeight = sum((layer['thickness'] for layer in structure))
        structureArea = max((layer['area'] for layer in structure))
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        with cairo.SVGSurface(f"assets/outputSankey_{layoutName}.svg", bgWidth, bgHeight) as surface:
            context = cairo.Context(surface)
            cumuThickness = 0
            for i, layer in enumerate(structure):
                r = colors[i%len(colors)][0]
                g = colors[i%len(colors)][1]
                b = colors[i%len(colors)][2]
                context.set_source_rgba(r, g, b, 0.1)
                height = layer['thickness'] / structureHeight * bgHeight
                if layer['area'] == structureArea:
                    context.rectangle(0, cumuThickness, bgWidth, height)
                else:
                    coverage = (layer['area'] / structureArea)**(1/2)
                    nStripes = 5
                    coveredArea = coverage * bgWidth
                    blankArea = (1-coverage) * bgWidth
                    stripeWidth = coveredArea / (nStripes + 1)
                    gapWidth = blankArea / nStripes 
                    x = (gapWidth + stripeWidth) / 2
                    for i in range(nStripes):
                        context.rectangle(x, cumuThickness, stripeWidth, height)
                        x += (stripeWidth + gapWidth)
                cumuThickness += height
                context.fill()
        self.svg.load(f"assets/outputSankey_{layoutName}.svg")