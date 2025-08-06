from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel,QHeaderView
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from PyQt6.QtSvgWidgets import QSvgWidget
import cairo
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.ax.plot(x, y, label="sin(x)")
        self.ax.set_title("X-Y Diagramm")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend()
        self.draw()

class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        ### svg
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        self.drawSankeySvg(self.currentLayoutIndex)

        ### mpl plot
        self.mplPlot = PlotCanvas(self)

        assemblyLayout = QHBoxLayout()
        assemblyLayout.addWidget(self.mplPlot)
        assemblyLayout.addWidget(self.svg)
        self.setLayout(assemblyLayout)
    
    def calcHeatflux(self, layoutIndex):
        # seebeck coefficient: 480 µV/K  
        # -> peltier coefficient: 140.7 mV
        self.currentLayoutIndex = layoutIndex
        layout = self.cache['layouts'][layoutIndex]
        resPeltierCoefficient = 0.48 * layout['numberOfElectricalRepetitions'] # mV
        # TODO: build W/U diagram, sankeys


    def drawSankeySvg(self, layoutIndex): # TODO: redraw when cache changes
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