from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel, QHeaderView,
    QCheckBox
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

    def plot_I_P(self, heatfluxi, tempDiffs):
        self.ax.clear()
        for i, tempDiff in enumerate(tempDiffs):
            self.ax.plot(heatfluxi['I'], heatfluxi['P_Results'][i], label=f"{tempDiff}", color='green', linewidth=2)
            if False: # !!! # TODO -> also better labels
                self.ax.plot(heatfluxi['I'], heatfluxi['P_Peltier'], label="Peltier Heatflux", color='blue', linewidth=1)
                self.ax.plot(heatfluxi['I'], heatfluxi['P_Joule'], label="Joule Heatflux", color='orange', linewidth=1)
                self.ax.plot(heatfluxi['I'], heatfluxi['P_HeatConduct'], label="Conductivity Heatflux", color='red', linewidth=1)
        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("P [W]")
        self.ax.legend()
        self.draw()

class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0
        self.tempDiffs = [0, 10, 20, 30]
        self.mplPlot = PlotCanvas(parent=self)

        ### checkboxes
        checkBoxLayout = QVBoxLayout()
        checkBoxLayout.addWidget(QLabel("Hot-Cold-Side\nTemperature\nDifference:"))
        self.checkBoxes = [] 
        for tempDiff in self.tempDiffs:
            checkBox = QCheckBox(f"{tempDiff} K")
            checkBox.stateChanged.connect(lambda _: self.createPlot(self.currentLayoutIndex)) # function needs mplplot
            checkBoxLayout.addWidget(checkBox)
            self.checkBoxes.append(checkBox)

        ### mpl plot
        heatfluxi = self.calcHeatfluxi(self.currentLayoutIndex, self.tempDiffs)
        self.createPlot(self.currentLayoutIndex)

        ### svg
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        self.drawSankeySvg(self.currentLayoutIndex)

        assemblyLayout = QHBoxLayout()
        assemblyLayout.addLayout(checkBoxLayout)
        assemblyLayout.addWidget(self.mplPlot)
        assemblyLayout.addWidget(self.svg)
        self.setLayout(assemblyLayout)
    
    def calcHeatfluxi(self, layoutIndex, tempDiffs):
        self.currentLayoutIndex = layoutIndex
        layout = self.cache['layouts'][layoutIndex]
        current = np.linspace(0, 6, 100)
        resPeltierCoefficient = (
            layout['combinedSeebeckCoefficient']/1000/1000 # µV/K -> V/K
            * layout['numberOfElectricalRepetitions'] 
            * 293.15 # temperature
        ) # V
        P_Peltier = current * resPeltierCoefficient
        P_Joule = current * current * layout['resElectricalResistance']
        # tempDiff = np.linspace(10, 10, 100)
        P_HeatConducts = []
        P_Results = []
        for tempDiff in tempDiffs:
            npTempDiff = np.linspace(tempDiff, tempDiff, 100)
            P_HeatConduct = npTempDiff / layout['resThermalResistance']
            P_HeatConducts.append(P_HeatConduct)
            P_Results.append(P_Peltier - 0.5 * P_Joule - P_HeatConduct)

        # P_HeatConduct = tempDiff / layout['resThermalResistance']
        # P_Res = P_Peltier - 0.5 * P_Joule - P_HeatConduct

        return {
            'I': current,
            'P_Joule': P_Joule,
            'P_Peltier': P_Peltier,
            'P_HeatConducts': P_HeatConducts,
            'P_Results': P_Results
        }

    def createPlot(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex
        tempDiffs = []
        for i, box in enumerate(self.checkBoxes):
            if box.isChecked():
                tempDiffs.append(self.tempDiffs[i])

        heatfluxi = self.calcHeatfluxi(self.currentLayoutIndex, tempDiffs)
        self.mplPlot.plot_I_P(heatfluxi, tempDiffs)


    def drawSankeySvg(self, layoutIndex): 
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
            (0.729, 1.0, 1.0),     # Pastelltürkis
            (0.729, 0.882, 1.0),   # Pastellblau
            (0.855, 0.729, 1.0),   # Pastelllila
            (1.0, 0.729, 0.945),   # Pastellmagenta
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