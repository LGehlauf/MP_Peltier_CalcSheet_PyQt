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
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=2)
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)

        elif len(dTs) == 2:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]},{dTs[1]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')

        elif len(dTs) == 3:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{CS}}$ ($\Delta$T={dTs[2]} K)", c='green', lw=2, ls=':')
            if showComponents:
                self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':')

        elif len(dTs) == 4:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=2)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=2, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{CS}}$ ($\Delta$T={dTs[2]} K)", c='green', lw=2, ls=':')
            self.ax.plot(I, P_Ress[3], label=f"$P_{{CS}}$ ($\Delta$T={dTs[3]} K)", c='green', lw=2, ls='-.')
            if showComponents:
                    self.ax.plot(I, P_Pe, label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]},{dTs[3]} K)", c='blue', lw=1)
                    self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]},{dTs[3]} K)", c='orange', lw=1)
                    self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                    self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                    self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':')
                    self.ax.plot(I, P_Ls[3], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[3]} K)", c='red', lw=1, ls='-.')

        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("P [W]")
        self.ax.grid()
        self.ax.legend()
        self.draw()

    def plot_I_COP(self, heatfluxi, dTs):
        self.ax.clear()
        cop = []
        linetypes = ['-', '--', ':', '-.']
        for i, res in enumerate(heatfluxi['P_Results']):
            cop.append(res/ -heatfluxi['P_Joule'])
            self.ax.plot(heatfluxi['I'], cop[i], label=f"COP ($\Delta$T={dTs[i]} K)", c='black', lw=2, ls=linetypes[i])

        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("COP")
        self.ax.grid()
        self.ax.legend()
        self.ax.set_ylim(0, 3)
        self.draw()

class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        self.init()
        self.connect()
    
    def init(self):
        self.tempDiffs = [0, 10, 30, 60]
        self.hfPlot = PlotCanvas(parent=self)
        self.copPlot = PlotCanvas(parent=self)

        ### checkboxes delta T
        deltaTLayout = QVBoxLayout()
        deltaTLayout.addStretch()

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

        ### svg
        svgLayout = QVBoxLayout()
        self.svgLabel = QLabel("")
        self.svgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        svgLayout.addWidget(self.svgLabel)
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        svgLayout.addWidget(self.svg)

        assemblyLayout = QVBoxLayout()
        boxesAndPlotsLayoutContainer = QWidget()
        boxesAndPlotsLayout = QHBoxLayout(boxesAndPlotsLayoutContainer)
        boxesAndPlotsLayout.addLayout(deltaTLayout)
        boxesAndPlotsLayout.addWidget(self.copPlot)
        boxesAndPlotsLayout.addWidget(self.hfPlot)
        boxesAndPlotsLayout.addLayout(svgLayout)
        boxesAndPlotsLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        assemblyLayout.addWidget(boxesAndPlotsLayoutContainer)
        assemblyLayout.addWidget(manipLayoutContainer)
        self.setLayout(assemblyLayout)

    def connect(self):
        self.toggleButtonHeatfluxComponents.toggled.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        for box in self.checkBoxesTempDiff:
            box.stateChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex)) 
        self.sliderElRes.valueChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.sliderThermRes.valueChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.checkBoxesTempDiff[1].setChecked(True)
    
    def createPlots(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex
        tempDiffs = []
        for i, box in enumerate(self.checkBoxesTempDiff):
            if box.isChecked():
                tempDiffs.append(self.tempDiffs[i])

        elResFactor = self.sliderElRes.value() / 100
        thermResFactor = self.sliderThermRes.value() / 100
        
        showComponents = self.toggleButtonHeatfluxComponents.isChecked()

        heatfluxiDict = self.calcHeatfluxi(self.currentLayoutIndex, tempDiffs, elResFactor, thermResFactor)
        self.hfPlot.plot_I_P(heatfluxiDict, tempDiffs, showComponents)
        self.copPlot.plot_I_COP(heatfluxiDict, tempDiffs)
        sankeyDict = self.calcSankeyDict(heatfluxiDict, tempDiffs)
        self.drawSankeySvg(layoutIndex, sankeyDict)

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

        self.manipElResMidLabel.setText(f"""
            {elResFactor * 100:.0f} % ({elResFactor * self.cache['layouts'][self.currentLayoutIndex]['resElectricalResistance']:.2f} Ω)
        """)
        self.manipThermResMidLabel.setText(f"""
            {thermResFactor * 100:.0f} % ({thermResFactor * self.cache['layouts'][self.currentLayoutIndex]['resThermalResistance']:.2f} K/W)
        """)

        return {
            'I': current,
            'P_Joule': P_Joule,
            'P_Peltier': P_Peltier,
            'P_HeatConducts': P_HeatConducts,
            'P_Results': P_Results
        }
        
    def calcSankeyDict(self, hfDict, tempDiffs):
        P_Coldside = max(hfDict['P_Results'][0])
        maxCSPowerIndex = np.argmax(hfDict['P_Results'][0])
        current = hfDict['I'][maxCSPowerIndex]
        P_Joule = - hfDict['P_Joule'][maxCSPowerIndex]
        P_HeatConduct = - hfDict['P_HeatConducts'][0][maxCSPowerIndex]
        P_Peltier = hfDict['P_Peltier'][maxCSPowerIndex] 
        P_Hotside = 0.5 * P_Joule + P_Peltier - P_HeatConduct

        if len(tempDiffs) > 0:
            self.svgLabel.setText(f"""
                Heatfluxes visualized\n
                for ΔT = {tempDiffs[0]} K\n
                at max. P = {P_Coldside:.1f} W ({current:.1f} A)

            """)
        else:
            self.svgLabel.setText(f"""
            """)

        return {
            'P_Hotside': P_Hotside,
            'P_Coldside': P_Coldside,
            'P_Joule': P_Joule,
            'P_HeatConduct': P_HeatConduct,
            'P_Peltier': P_Peltier
        }


    def drawSankeySvg(self, layoutIndex, hfDict): # TODO: sankey for max cs power/ max cop, also global legend
        def createText(context, text, centerx, centery):
            context.save()
            (x, y, width, height, dx, dy) = context.text_extents(text)
            textPosx = centerx - width/2 - x 
            textPosy = centery - height/2 - y
            context.set_source_rgba(*hfCols['bgText'])
            context.rectangle(textPosx-2, textPosy-height-3, width+7, height+8)
            context.fill()
            context.set_source_rgba(*hfCols['text'])
            context.move_to(textPosx, textPosy)
            context.show_text(text)
            context.restore()
            context.new_path()

        self.currentLayoutIndex = layoutIndex
        layoutName = self.cache['layouts'][layoutIndex]['name']
        svgWidth, svgHeight = 500, 500
        bgWidth, bgHeight = 0.9 * svgWidth, 0.9 * svgHeight
        self.svg.setFixedSize(svgWidth, svgHeight)
        layerCols = [
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
        hfCols = {
            'bgText': (1.0, 1.0, 1.0, 0.3),
            'text': (0.0, 0.0, 0.0, 1.0),
            'endBlock': (0.0, 0.0, 0.0, 0.7), # black
            'heatConduct': (1.0, 0.0, 0.0, 0.7), # red
            'coldside': (0.0, 0.5019607843137255, 0.0, 0.7), # green
            'peltier': (0.0, 0.0, 1.0, 0.7), # blue
            'hotside': (1.0, 0.0, 1.0, 0.7), # violet
            'joule': (1.0, 0.6470588235294118, 0.0, 0.7) # orange
        }
        structure = self.cache['layouts'][self.currentLayoutIndex]['thermalStructure']
        structureHeight = sum((layer['thickness'] for layer in structure))
        structureArea = max((layer['area'] for layer in structure))
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        with cairo.SVGSurface(f"assets/outputSankey_{layoutName}.svg", svgWidth, svgHeight) as surface:
            ### draw background
            ct = cairo.Context(surface)
            ct.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ct.set_font_size(12)
            bgStartx = (svgWidth-bgWidth)/2
            bgStarty = (svgHeight-bgHeight)/2
            cumuThickness = bgStarty
            for i, layer in enumerate(structure):
                r = layerCols[i%len(layerCols)][0]
                g = layerCols[i%len(layerCols)][1]
                b = layerCols[i%len(layerCols)][2]
                ct.set_source_rgba(r, g, b, 0.2)
                height = layer['thickness'] / structureHeight * bgHeight
                if layer['area'] == structureArea: # full rectangle
                    ct.rectangle(bgStartx, cumuThickness, bgWidth, height)
                else: # stripes
                    coverage = (layer['area'] / structureArea)**(1/2)
                    nStripes = 5
                    coveredArea = coverage * bgWidth
                    blankArea = (1-coverage) * bgWidth
                    stripeWidth = coveredArea / (nStripes + 1)
                    gapWidth = blankArea / nStripes 
                    x = bgStartx + (gapWidth + stripeWidth) / 2
                    for i in range(nStripes):
                        ct.rectangle(x, cumuThickness, stripeWidth, height)
                        x += (stripeWidth + gapWidth)
                cumuThickness += height
                ct.fill()
            
            ### draw heatfluxi
            # > 0 check
            if any([val<0 for val in hfDict.values()]):
                createText(ct, f"Error: negative Heatflux values", svgWidth/2, svgHeight/2)
            else:
                # variables
                margin = 20
                hfStartx = bgStartx + margin
                hfStarty = bgStarty + margin
                hfEndx = bgStartx + bgWidth - margin
                hfEndy = bgStarty + bgHeight - margin
                hfMidx = (hfEndx + hfStartx)/2
                hfMidy = (hfEndy + hfStarty)/2

                hfPixelRatio = (bgWidth - 8 * margin) / (hfDict['P_Hotside'] + hfDict['P_HeatConduct'])
                PHotSideWidth = hfDict['P_Hotside'] * hfPixelRatio
                PJouleWidth = hfDict['P_Joule'] * hfPixelRatio
                PColdsideWidth = hfDict['P_Coldside'] * hfPixelRatio
                PHeatConductWidth = hfDict['P_HeatConduct'] * hfPixelRatio
                PPeltierWidth = hfDict['P_Peltier'] * hfPixelRatio

                PHotSideAndHeatConductWidth = PHotSideWidth + PHeatConductWidth

                # Heatconduct line
                heatConductX = hfMidx+((PHotSideAndHeatConductWidth)/2)-PHeatConductWidth/2
                ct.set_source_rgba(*hfCols['heatConduct'])
                ct.set_line_width(PHeatConductWidth)
                ct.move_to(heatConductX, hfEndy-margin)
                ct.line_to(heatConductX, hfStarty+margin)
                ct.stroke()
                # Heatconduct start and end block
                ct.set_source_rgba(*hfCols['endBlock'])
                ct.move_to(heatConductX, hfEndy)
                ct.line_to(heatConductX, hfEndy-margin)
                ct.stroke()
                ct.move_to(heatConductX, hfStarty)
                ct.line_to(heatConductX, hfStarty+margin)
                ct.stroke()
                

                # Joule start line
                ct.set_source_rgba(*hfCols['joule'])
                ct.set_line_width(PJouleWidth)
                ct.move_to(0, svgHeight/2)
                ct.line_to(hfStartx, svgHeight/2)
                ct.stroke()

                # Joule-Hotside-arc
                ct.set_line_width(PJouleWidth/2)
                ct.set_source_rgba(*hfCols['joule'])
                ct.save()
                ct.translate(hfStartx, hfStarty+margin)
                scalex = (hfMidx - PHotSideAndHeatConductWidth/2 + PJouleWidth/4) - hfStartx
                scaley = (hfMidy - PJouleWidth/4) - (hfStarty + margin) 
                ct.scale(scalex, scaley)
                ct.arc(0.0, 0.0, 1.0, 0, 0.5*np.pi)
                ct.restore()
                ct.stroke()

                # Joule-Coldside endblock
                ct.set_source_rgba(*hfCols['endBlock'])
                ct.move_to(hfMidx-(PHotSideAndHeatConductWidth/2)+ 0.75 * PJouleWidth, hfEndy)
                ct.line_to(hfMidx-(PHotSideAndHeatConductWidth/2)+ 0.75 * PJouleWidth, hfEndy-margin)
                ct.stroke()

                # Coldside start line
                ct.set_source_rgba(*hfCols['coldside'])
                ct.set_line_width(PColdsideWidth)
                ct.move_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, svgHeight)
                ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, hfEndy-margin)
                ct.stroke()

                # HotSide End Line
                ct.set_source_rgba(*hfCols['hotside'])
                ct.set_line_width(PHotSideWidth)
                ct.move_to(hfMidx - PHeatConductWidth/2, hfStarty+margin)
                ct.line_to(hfMidx - PHeatConductWidth/2, 0)
                ct.stroke()

                # Peltier Line
                ct.set_source_rgba(*hfCols['peltier'])
                ct.set_line_width(PPeltierWidth)
                ct.move_to(hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, hfEndy-margin)
                ct.line_to(hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, hfStarty+margin)
                ct.stroke()

                # Joule-Coldside-arc
                ct.set_line_width(PJouleWidth/2)
                ct.set_source_rgba(*hfCols['joule'])
                ct.save()
                ct.translate(hfStartx, hfEndy-margin)
                scalex = (hfMidx - PHotSideAndHeatConductWidth/2 + PJouleWidth * 3/4) - hfStartx
                scaley = (hfEndy - margin) - (hfMidy + PJouleWidth/4)
                ct.scale(scalex, scaley)
                ct.arc(0.0, 0.0, 1.0, 1.5*np.pi, 2*np.pi)
                ct.restore()
                ct.stroke()

                # labels
                createText(ct, f"P_ J ({hfDict['P_Joule']:.1f} W)", 40, svgHeight/2)
                createText(ct, f"P_HS ({hfDict['P_Hotside']:.1f} W)", hfMidx - PHeatConductWidth/2, 30)
                createText(ct, f"P_CS ({hfDict['P_Coldside']:.1f} W)", hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, svgHeight-30)
                createText(ct, f"P_Pe ({hfDict['P_Peltier']:.1f} W)", hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, svgHeight/2-30)
                ct.set_line_width(5)
                ct.set_source_rgba(*hfCols['bgText'])
                ct.move_to(hfMidx+PHotSideAndHeatConductWidth/2-PPeltierWidth/2 - PPeltierWidth/2, svgHeight/2-19)
                ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PPeltierWidth/2 + PPeltierWidth/2, svgHeight/2-19)
                ct.stroke()
                createText(ct, f"P_λ ({hfDict['P_HeatConduct']:.1f} W)", heatConductX+35, svgHeight/2+30)

        self.svg.load(f"assets/outputSankey_{layoutName}.svg")