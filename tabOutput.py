from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel, QHeaderView,
    QCheckBox, QSizePolicy, QSlider, QButtonGroup
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction
from PyQt6.QtSvgWidgets import QSvgWidget
import numpy as np
from tabOutputSankey import drawSankeySvg
from tabOutputMpl import PlotCanvas


class TabOutput(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        self.init()
        self.connect()
    
    drawSankeySvg = drawSankeySvg
    
    def init(self):
        self.setStyleSheet("QLineEdit { color: white; }")
        self.tempDiffs = [0, 10, 30, 60]
        self.hfPlot = PlotCanvas(parent=self)
        self.hfPlot.setStyleSheet("background: transparent;")
        self.copPlot = PlotCanvas(parent=self)
        self.copPlot.setStyleSheet("background: transparent;")

        ### y-lims 
        self.inPlot_I_P_ylim_L = QLineEdit()
        self.inPlot_I_P_ylim_U = QLineEdit()
        self.inPlot_I_COP_ylim_L = QLineEdit()
        self.inPlot_I_COP_ylim_U = QLineEdit()

        self.inPlot_I_P_ylim_L.setPlaceholderText("auto")
        self.inPlot_I_P_ylim_U.setPlaceholderText("auto")
        self.inPlot_I_COP_ylim_L.setPlaceholderText("0")
        self.inPlot_I_COP_ylim_U.setPlaceholderText("20")

        mplLimQLabels = QHBoxLayout()
        mplLimQLabels.addWidget(QLabel("Heatflux Min [W]"))
        mplLimQLabels.addWidget(QLabel("Heatflux Max [W]"))
        mplLimQLabels.addWidget(QLabel("COP Min"))
        mplLimQLabels.addWidget(QLabel("COP Max"))
        mplYLimQLineEdits = QHBoxLayout()
        mplYLimQLineEdits.addWidget(self.inPlot_I_P_ylim_L)
        mplYLimQLineEdits.addWidget(self.inPlot_I_P_ylim_U)
        mplYLimQLineEdits.addWidget(self.inPlot_I_COP_ylim_L)
        mplYLimQLineEdits.addWidget(self.inPlot_I_COP_ylim_U)
        mplYLimLayout = QVBoxLayout()
        mplYLimLayout.addLayout(mplLimQLabels)
        mplYLimLayout.addLayout(mplYLimQLineEdits)

        ### x-lims
        self.inPlot_xlim_L = QLineEdit()
        self.inPlot_xlim_U = QLineEdit()

        self.inPlot_xlim_L.setPlaceholderText("0")
        self.inPlot_xlim_U.setPlaceholderText("6")

        mplXLimQLabels = QHBoxLayout()
        mplXLimQLabels.addWidget(QLabel("Min I [A]"))
        mplXLimQLabels.addWidget(QLabel("Max I [A]"))
        mplXLimQLineEdits = QHBoxLayout()
        mplXLimQLineEdits.addWidget(self.inPlot_xlim_L)
        mplXLimQLineEdits.addWidget(self.inPlot_xlim_U)
        mplXLimLayout = QVBoxLayout()
        mplXLimLayout.addLayout(mplXLimQLabels)
        mplXLimLayout.addLayout(mplXLimQLineEdits)

        ### checkboxes delta T
        deltaTLayoutContainer = QWidget()
        deltaTLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        deltaTLayout = QHBoxLayout(deltaTLayoutContainer)
        deltaTLayout.addStretch()

        self.toggleButtonHeatfluxComponents = QPushButton("Toggle\nComponents")
        self.toggleButtonHeatfluxComponents.setCheckable(True)
        self.toggleButtonHeatfluxComponents.setChecked(True)
        self.toggleButtonHeatfluxComponents.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        checkBoxTempDiffLabel = QLabel()
        checkBoxTempDiffLabel.setText("ΔT:")
        deltaTLayout.addWidget(checkBoxTempDiffLabel)
        self.checkBoxesTempDiff = [] 
        for tempDiff in self.tempDiffs:
            checkBoxTempDiff = QCheckBox(f"{tempDiff} K")
            deltaTLayout.addWidget(checkBoxTempDiff)
            self.checkBoxesTempDiff.append(checkBoxTempDiff)
        # deltaTLayout.addWidget(self.toggleButtonHeatfluxComponents)
        deltaTLayout.addStretch()

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
        sankeyLayout = QVBoxLayout()
        self.sankeyLabel = QLabel("")
        self.sankeyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sankeyMaxPowButton = QPushButton("")
        self.sankeyMaxPowButton.setCheckable(True)
        self.sankeyMaxPowButton.setChecked(True)
        self.sankeyMaxCopButton = QPushButton("")
        self.sankeyMaxCopButton.setCheckable(True)
        buttonGroupLayout = QHBoxLayout()
        buttonGroup = QButtonGroup(self)
        buttonGroup.setExclusive(True)
        buttonGroup.addButton(self.sankeyMaxPowButton)
        buttonGroup.addButton(self.sankeyMaxCopButton)

        sankeyLayout.addWidget(self.sankeyLabel)
        buttonGroupLayout.addWidget(self.sankeyMaxPowButton)
        buttonGroupLayout.addWidget(self.sankeyMaxCopButton)
        sankeyLayout.addLayout(buttonGroupLayout)
        layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
        self.svg = QSvgWidget(f"assets/outputSankey_{layoutName}.svg")
        sankeyLayout.addWidget(self.svg)
        bigLegendL = QLabel("ΔT...\nP_In\nP_S\nP_J\nP_HS...\nP_CS...\nP_Pe...\nP_λ...")
        bigLegendL.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        bigLegendR = QLabel("Temperature Difference between Hot- and Coldside\nInput Power\nSeebeck Power\nJoule Heatflux\nHotside Heatflux\nColdside Heatflux\nPeltier Heatflux\nReturning Conductivity Heatflux")
        bigLegendLayout = QHBoxLayout()
        bigLegendLayout.addWidget(bigLegendL)
        bigLegendLayout.addWidget(bigLegendR)
        sankeyLayout.addLayout(bigLegendLayout)


        ### assembly
        assemblyLayout = QVBoxLayout()
        boxesAndPlotsLayoutContainer = QWidget()
        boxesAndPlotsLayout = QHBoxLayout(boxesAndPlotsLayoutContainer)
        mplPlotsLayoutContainer = QWidget()
        mplPlotsLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        mplPlotsLayout = QHBoxLayout(mplPlotsLayoutContainer)
        mplPlotsLayout.addWidget(self.toggleButtonHeatfluxComponents)
        mplPlotsLayout.addWidget(self.hfPlot)
        mplPlotsLayout.addWidget(self.copPlot)
        mplPlotsAndDTLayout = QVBoxLayout()
        mplPlotsAndDTLayout.addWidget(deltaTLayoutContainer)
        mplPlotsAndDTLayout.addWidget(mplPlotsLayoutContainer)
        mplPlotsAndDTLayout.addWidget(QLabel("Plot Limit Setters:"))
        mplPlotsAndDTLayout.addLayout(mplYLimLayout)
        mplPlotsAndDTLayout.addLayout(mplXLimLayout)
        boxesAndPlotsLayout.addLayout(mplPlotsAndDTLayout)
        boxesAndPlotsLayout.addLayout(sankeyLayout)
        boxesAndPlotsLayoutContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        assemblyLayout.addWidget(boxesAndPlotsLayoutContainer)
        assemblyLayout.addWidget(manipLayoutContainer)
        self.setLayout(assemblyLayout)

    def connect(self):
        self.toggleButtonHeatfluxComponents.toggled.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        for box in self.checkBoxesTempDiff:
            box.stateChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex)) 
        self.sankeyMaxPowButton.toggled.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.sliderElRes.valueChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.sliderThermRes.valueChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_I_P_ylim_L.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_I_P_ylim_U.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_I_COP_ylim_L.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_I_COP_ylim_U.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_xlim_L.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.inPlot_xlim_U.textChanged.connect(lambda _: self.createPlots(self.currentLayoutIndex))
        self.checkBoxesTempDiff[1].setChecked(True)
    
    def createPlots(self, layoutIndex, ylim_l=None, ylim_u=None, xlim_l=None, xlim_u=None):
        self.currentLayoutIndex = layoutIndex
        tempDiffs = []
        for i, box in enumerate(self.checkBoxesTempDiff):
            if box.isChecked():
                tempDiffs.append(self.tempDiffs[i])
        maxPowerBool = self.sankeyMaxPowButton.isChecked()

        elResFactor = self.sliderElRes.value() / 100
        thermResFactor = self.sliderThermRes.value() / 100
        
        showComponents = self.toggleButtonHeatfluxComponents.isChecked()

        heatfluxiDict = self.calcHeatfluxi(self.currentLayoutIndex, tempDiffs, elResFactor, thermResFactor)

        self.hfPlot.plot_I_P(heatfluxiDict, tempDiffs, showComponents, self.inPlot_I_P_ylim_L.text(), self.inPlot_I_P_ylim_U.text(), self.inPlot_xlim_L.text(), self.inPlot_xlim_U.text())
        self.copPlot.plot_I_COP(heatfluxiDict, tempDiffs, self.inPlot_I_COP_ylim_L.text(), self.inPlot_I_COP_ylim_U.text(), self.inPlot_xlim_L.text(), self.inPlot_xlim_U.text())
        sankeyDict = self.calcSankeyDict(heatfluxiDict, tempDiffs, maxPowerBool)
        self.drawSankeySvg(layoutIndex, sankeyDict)

    def calcHeatfluxi(self, layoutIndex, tempDiffs, elResFactor, thermResFactor):
        layout = self.cache['layouts'][layoutIndex]
        moduleSeebeckCoefficient = (layout['combinedSeebeckCoefficient']/1000/1000 # µV/K -> V/K
            * layout['numberOfElectricalRepetitions'])
        self.currentLayoutIndex = layoutIndex
        current = np.linspace(0, 6, 100)
        P_Joule = - current * current * layout['resElectricalResistance'] * elResFactor
        P_Peltiers = []
        P_HeatConducts = []
        P_Results = []
        P_Ins = []
        COPs = []
        for tempDiff in tempDiffs:
            P_Peltier = ( moduleSeebeckCoefficient     
                * (293.15 - tempDiff) # coldside temperature
                * current
            ) # W
            P_Peltiers.append(P_Peltier)
            npTempDiff = np.linspace(tempDiff, tempDiff, 100)
            P_HeatConduct = - npTempDiff / (layout['resThermalResistance'] * thermResFactor)
            P_HeatConducts.append(P_HeatConduct)
            P_Res = P_Peltier + 0.5 * P_Joule + P_HeatConduct
            P_Results.append(P_Res)
            P_In = -P_Joule + moduleSeebeckCoefficient * current * tempDiff
            P_Ins.append(P_In)
            COPs.append(np.divide(P_Res, P_In, out=np.zeros_like(P_Res), where=P_Joule!=0)) 

        self.manipElResMidLabel.setText(f"""
            {elResFactor * 100:.0f} % ({elResFactor * self.cache['layouts'][self.currentLayoutIndex]['resElectricalResistance']:.2f} Ω)
        """)
        self.manipThermResMidLabel.setText(f"""
            {thermResFactor * 100:.0f} % ({thermResFactor * self.cache['layouts'][self.currentLayoutIndex]['resThermalResistance']:.2f} K/W)
        """)

        return {
            'I': current,
            'P_Joule': P_Joule,
            'P_Peltiers': P_Peltiers,
            'P_HeatConducts': P_HeatConducts,
            'P_Results': P_Results,
            'P_Ins': P_Ins,
            'COPs': COPs
        }
        
    def calcSankeyDict(self, hfDict, tempDiffs, maxPowerBool):
        if len(tempDiffs) > 0:
            maxCOP = max(hfDict['COPs'][0])
            maxCOPIndex = np.argmax(hfDict['COPs'][0])
            currentMaxCOP = hfDict['I'][maxCOPIndex]

            maxCSPower = max(hfDict['P_Results'][0])
            maxCSPowerIndex = np.argmax(hfDict['P_Results'][0])
            currentMaxCSPower = hfDict['I'][maxCSPowerIndex]

            if maxPowerBool:
                P_Coldside = maxCSPower
                P_Joule = - hfDict['P_Joule'][maxCSPowerIndex]
                P_HeatConduct = - hfDict['P_HeatConducts'][0][maxCSPowerIndex]
                P_Peltier = hfDict['P_Peltiers'][0][maxCSPowerIndex] 
                P_In = hfDict['P_Ins'][0][maxCSPowerIndex]
                P_Seebeck = hfDict['P_Ins'][0][maxCSPowerIndex] - P_Joule

            else:
                P_Coldside = hfDict['P_Results'][0][maxCOPIndex] 
                P_Joule = - hfDict['P_Joule'][maxCOPIndex]
                P_HeatConduct = - hfDict['P_HeatConducts'][0][maxCOPIndex]
                P_Peltier = hfDict['P_Peltiers'][0][maxCOPIndex] 
                P_In = hfDict['P_Ins'][0][maxCOPIndex]
                P_Seebeck = hfDict['P_Ins'][0][maxCOPIndex] - P_Joule

            P_Hotside = 0.5 * P_Joule + P_Peltier - P_HeatConduct

            decPlaces = 1 if P_Coldside > 1 else 2

            self.sankeyMaxCopButton.setText(f"\nMax. COP ({maxCOP:.1f})\nI = {currentMaxCOP:.2f} A\n")
            self.sankeyMaxPowButton.setText(f"\nMax. Coldside Heatflux ({maxCSPower:.{decPlaces}f} W)\nI = {currentMaxCSPower:.2f} A\n")

            self.sankeyLabel.setText(f"""
                Sankey-Heatflux Diagram for ΔT = {tempDiffs[0]} K
            """)

        else:
            self.sankeyLabel.setText(f"Sankey-Heatflux Diagram")
            return {}

        return {
            'P_Hotside': P_Hotside,
            'P_Coldside': P_Coldside,
            'P_Joule': P_Joule,
            'P_HeatConduct': P_HeatConduct,
            'P_Peltier': P_Peltier,
            'P_In': P_In,
            'P_Seebeck': P_Seebeck
        }
