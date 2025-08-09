from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel, QHeaderView,
    QCheckBox, QSizePolicy, QSlider
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

    def plot_I_P(self, heatfluxi, dTs, showComponents):
        self.ax.clear()
        I = heatfluxi['I']
        P_Ress = heatfluxi['P_Results']
        P_Pe = heatfluxi['P_Peltier']
        P_J = heatfluxi['P_Joule']
        P_Ls = heatfluxi['P_HeatConducts']
        if len(dTs) == 1:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{Res}}$($\Delta$T={dTs[0]} K)", c='green', lw=2)
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$($\Delta T=${dTs[0]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$($\Delta T=${dTs[0]} K)", c='red', lw=1)

        elif len(dTs) == 2:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{Res}}$($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{Res}}$($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$($\Delta T=${dTs[0]},{dTs[1]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$($\Delta T=${dTs[0]},{dTs[1]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')

        elif len(dTs) == 3:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{Res}}$($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{Res}}$($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{Res}}$($\Delta$T={dTs[2]} K)", c='green', lw=2, ls=':')
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':')

        elif len(dTs) == 4:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{Res}}$($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{Res}}$($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{Res}}$($\Delta$T={dTs[2]} K)", c='green', lw=2, ls=':')
            self.ax.plot(I, P_Ress[3], label=f"$P_{{Res}}$($\Delta$T={dTs[3]} K)", c='green', lw=2, ls='-.')
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]},{dTs[3]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]},{dTs[3]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':')
                self.ax.plot(I, P_Ls[3], label=f"$P_{{\lambda}}$($\Delta T=${dTs[3]} K)", c='red', lw=1, ls='-.')

        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("P [W]")
        self.ax.grid()
        self.ax.legend()
        self.draw()

class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        self.init()
        self.connect()
    
    def init(self):
        self.tempDiffs = [0, 10, 20, 30]
        self.mplPlot = PlotCanvas(parent=self)

        ### checkboxes delta T
        deltaTLayout = QVBoxLayout()

        self.toggleButtonHeatfluxComponents = QPushButton("Toggle\nComponents")
        self.toggleButtonHeatfluxComponents.setCheckable(True)
        self.toggleButtonHeatfluxComponents.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkBoxTempDiffLabel = QLabel()
        checkBoxTempDiffLabel.setText("Δ T")
        deltaTLayout.addWidget(checkBoxTempDiffLabel)
        self.checkBoxesTempDiff = [] 
        for tempDiff in self.tempDiffs:
            checkBoxTempDiff = QCheckBox(f"{tempDiff} K")
            deltaTLayout.addWidget(checkBoxTempDiff)
            self.checkBoxesTempDiff.append(checkBoxTempDiff)
        self.checkBoxesTempDiff[1].setChecked(True)
        deltaTLayout.addWidget(self.toggleButtonHeatfluxComponents)

        ### slider electrical and thermal resistance
        manipLayoutContainer = QWidget()
        manipLayout = QHBoxLayout(manipLayoutContainer)

        manipElResLayout = QVBoxLayout()
        manipElResLayout.addWidget(QLabel("Electrical Resistance Manipulation"))
        self.sliderElRes = QSlider(Qt.Orientation.Horizontal)
        self.sliderElRes.setMinimum(1)
        self.sliderElRes.setMaximum(200)
        self.sliderElRes.setValue(100)
        manipElResLayout.addWidget(self.sliderElRes)
        manipElResLabelLayout = QHBoxLayout()
        manipElResMinLabel = QLabel(f"{self.sliderElRes.minimum()} %")
        manipElResMinLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.manipElResMidLabel = QLabel()
        self.manipElResMidLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manipElResMaxLabel = QLabel(f"{self.sliderElRes.maximum()} %")
        manipElResMaxLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        manipElResLabelLayout.addWidget(manipElResMinLabel)
        manipElResLabelLayout.addStretch()
        manipElResLabelLayout.addWidget(self.manipElResMidLabel)
        manipElResLabelLayout.addStretch()
        manipElResLabelLayout.addWidget(manipElResMaxLabel)
        manipElResLayout.addLayout(manipElResLabelLayout)
        manipLayout.addLayout(manipElResLayout)

        manipThermResLayout = QVBoxLayout()
        sliderThermResLabel = QLabel()
        sliderThermResLabel.setText("Thermal Resistance Manipulation")
        manipThermResLayout.addWidget(sliderThermResLabel)
        self.sliderThermRes = QSlider(Qt.Orientation.Horizontal)
        self.sliderThermRes.setMinimum(1)
        self.sliderThermRes.setMaximum(200)
        self.sliderThermRes.setValue(100)
        manipThermResLayout.addWidget(self.sliderThermRes)
        manipThermResLabelLayout = QHBoxLayout()
        manipThermResMinLabel = QLabel(f"{self.sliderThermRes.minimum()} %")
        manipThermResMinLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.manipThermResMidLabel = QLabel()
        self.manipThermResMidLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manipThermResMaxLabel = QLabel(f"{self.sliderThermRes.maximum()} %")
        manipThermResMaxLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        manipThermResLabelLayout.addWidget(manipThermResMinLabel)
        manipThermResLabelLayout.addStretch()
        manipThermResLabelLayout.addWidget(self.manipThermResMidLabel)
        manipThermResLabelLayout.addStretch()
        manipThermResLabelLayout.addWidget(manipThermResMaxLabel)
        manipThermResLayout.addLayout(manipThermResLabelLayout)
        manipLayout.addLayout(manipThermResLayout)

        manipLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        ### mpl plot
        heatfluxi = self.calcHeatfluxi(self.currentLayoutIndex, self.tempDiffs, 1, 1)
        self.createPlot(self.currentLayoutIndex)

        ### svg
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        self.drawSankeySvg(self.currentLayoutIndex)

        assemblyLayout = QVBoxLayout()
        boxesAndPlotsLayoutContainer = QWidget()
        boxesAndPlotsLayout = QHBoxLayout(boxesAndPlotsLayoutContainer)
        boxesAndPlotsLayout.addLayout(deltaTLayout)
        boxesAndPlotsLayout.addWidget(self.mplPlot)
        boxesAndPlotsLayout.addWidget(self.svg)
        boxesAndPlotsLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # assemblyLayout.addLayout(boxesAndPlotsLayout)
        assemblyLayout.addWidget(boxesAndPlotsLayoutContainer)
        # assemblyLayout.addLayout(manipLayout)
        assemblyLayout.addWidget(manipLayoutContainer)
        self.setLayout(assemblyLayout)

    def connect(self):
        self.toggleButtonHeatfluxComponents.toggled.connect(lambda _: self.createPlot(self.currentLayoutIndex))
        for box in self.checkBoxesTempDiff:
            box.stateChanged.connect(lambda _: self.createPlot(self.currentLayoutIndex)) 
        self.sliderElRes.valueChanged.connect(lambda _: self.createPlot(self.currentLayoutIndex))
        self.sliderThermRes.valueChanged.connect(lambda _: self.createPlot(self.currentLayoutIndex))
    
    def createPlot(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex
        tempDiffs = []
        for i, box in enumerate(self.checkBoxesTempDiff):
            if box.isChecked():
                tempDiffs.append(self.tempDiffs[i])

        elResFactor = self.sliderElRes.value() / 100
        thermResFactor = self.sliderThermRes.value() / 100
        self.manipElResMidLabel.setText(f"{elResFactor * 100:.0f} % ({elResFactor * self.cache['layouts'][self.currentLayoutIndex]['resElectricalResistance']:.2f} Ω)")
        self.manipThermResMidLabel.setText(f"{thermResFactor * 100:.0f} % ({thermResFactor * self.cache['layouts'][self.currentLayoutIndex]['resThermalResistance']:.2f} W/mK)")
        thermResFactor = self.sliderThermRes.value() / 100
        
        showComponents = self.toggleButtonHeatfluxComponents.isChecked()

        heatfluxiDict = self.calcHeatfluxi(self.currentLayoutIndex, tempDiffs, elResFactor, thermResFactor)
        self.mplPlot.plot_I_P(heatfluxiDict, tempDiffs, showComponents)

    def calcHeatfluxi(self, layoutIndex, tempDiffs, elResFactor, thermResFactor):
        self.currentLayoutIndex = layoutIndex
        layout = self.cache['layouts'][layoutIndex]
        current = np.linspace(0, 6, 100)
        resPeltierCoefficient = (
            layout['combinedSeebeckCoefficient']/1000/1000 # µV/K -> V/K
            * layout['numberOfElectricalRepetitions'] 
            * 293.15 # temperature
        ) # V
        P_Peltier = current * resPeltierCoefficient
        P_Joule = - current * current * layout['resElectricalResistance'] * elResFactor
        P_HeatConducts = []
        P_Results = []
        for tempDiff in tempDiffs:
            npTempDiff = np.linspace(tempDiff, tempDiff, 100)
            P_HeatConduct = - npTempDiff / (layout['resThermalResistance'] * thermResFactor)
            P_HeatConducts.append(P_HeatConduct)
            P_Results.append(P_Peltier + 0.5 * P_Joule + P_HeatConduct)

        return {
            'I': current,
            'P_Joule': P_Joule,
            'P_Peltier': P_Peltier,
            'P_HeatConducts': P_HeatConducts,
            'P_Results': P_Results
        }


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