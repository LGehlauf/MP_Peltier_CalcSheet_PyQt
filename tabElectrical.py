from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMenu, QLabel,QHeaderView
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction

class TabElectrical(QWidget):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.currentLayoutIndex = 0

        ### input new row fields
        self.inMaterial = QLineEdit()
        self.inCrossSection = QLineEdit()
        self.inLength = QLineEdit()
        self.inSpecElResistance = QLineEdit()
        self.inRowNum = QLineEdit()

        self.inMaterial.setPlaceholderText("Material")
        self.inCrossSection.setPlaceholderText("Cross-Section [mm²]")
        self.inLength.setPlaceholderText("Length [mm]")
        self.inSpecElResistance.setPlaceholderText("Spec. Elec. Resistance [Ohm*m]")
        self.inRowNum.setPlaceholderText("Insert After Row")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inMaterial)
        inputLayout.addWidget(self.inCrossSection)
        inputLayout.addWidget(self.inLength)
        inputLayout.addWidget(self.inSpecElResistance)
        inputLayout.addWidget(self.inRowNum)

        ### add layer button
        buttonAddRow = QPushButton("Add Conductor")
        buttonAddRow.clicked.connect(self.addRow)
        inputLayout.addWidget(buttonAddRow)

        ### layer table
        self.table = QTableWidget(0,4)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setHorizontalHeaderLabels(["Material", "Cross-Section [mm²]", "Length [mm]", "Spec. Elec. Resistance [Ohm*m]"])
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.rightClickOnTable)
        self.setTable(layoutIndex=0)

        ### input number of Repetititions and Peltier Coeff Layout
        repLayout = QHBoxLayout()
        self.inNumReps = QLineEdit()
        self.displayNumReps(self.currentLayoutIndex)
        self.inNumReps.textChanged.connect(self.saveNumReps)

        self.inSeebeckCoeff = QLineEdit()
        self.displaySeebeckCoeff(self.currentLayoutIndex)
        self.inSeebeckCoeff.textChanged.connect(self.saveSeebeckCoeff)
        repLayout.addWidget(QLabel("Number of Repititions: "))
        repLayout.addWidget(self.inNumReps)
        repLayout.addWidget(QLabel("Combined Seebeck Coefficient: (µV/K)"))
        repLayout.addWidget(self.inSeebeckCoeff)

        ### output layout 
        outputLayout = QHBoxLayout()
        self.outputResLabel = QLabel(alignment=Qt.AlignmentFlag.AlignLeft)
        outputLayout.addWidget(self.outputResLabel)
        self.setOutput(self.currentLayoutIndex)

        assemblyLayout = QVBoxLayout()
        assemblyLayout.addLayout(inputLayout)
        assemblyLayout.addWidget(self.table)
        assemblyLayout.addLayout(repLayout)
        assemblyLayout.addLayout(outputLayout)

        self.setLayout(assemblyLayout)

    def addRow(self):
        material = self.inMaterial.text()
        crossSection = self.inCrossSection.text()
        length = self.inLength.text()
        specElResistance = self.inSpecElResistance.text()
        rowNum = self.inRowNum.text()
        for x in [crossSection, length, specElResistance]:
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
        self.cache['layouts'][self.currentLayoutIndex]['electricalStructure'].insert( rowNum, 
            {'material': material, 'crossSection': float(crossSection), 'length': float(length), 'specElResistance': float(specElResistance)}
        )
        self.table.insertRow(rowNum)
        self.table.setItem(rowNum, 0, QTableWidgetItem(material))
        self.table.setItem(rowNum, 1, QTableWidgetItem(crossSection))
        self.table.setItem(rowNum, 2, QTableWidgetItem(length))
        self.table.setItem(rowNum, 3, QTableWidgetItem(specElResistance))

        self.inMaterial.clear()
        self.inCrossSection.clear()
        self.inLength.clear()
        self.inSpecElResistance.clear()
        self.inRowNum.clear()
        
        self.setOutput(self.currentLayoutIndex)

    def setTable(self, layoutIndex):
        self.currentLayoutIndex = layoutIndex
        self.table.clearContents()
        self.table.setRowCount(0)
        for layer in self.cache['layouts'][layoutIndex]['electricalStructure']:
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
        self.cache['layouts'][self.currentLayoutIndex]['electricalStructure'].pop(rowNum)
        self.table.removeRow(rowNum)
        self.setOutput(self.currentLayoutIndex)

    def displayNumReps(self, layoutIndex):
        self.inNumReps.setText(str(self.cache['layouts'][layoutIndex]['numberOfElectricalRepetitions']))

    def saveNumReps(self):
        print("saveNum")
        numReps = self.inNumReps.text()
        try: 
            numReps = int(numReps)
        except:
            return
        self.cache['layouts'][self.currentLayoutIndex]['numberOfElectricalRepetitions'] = numReps
        self.setOutput(self.currentLayoutIndex)

    def displaySeebeckCoeff(self, layoutIndex):
        self.inNumReps.setText(str(self.cache['layouts'][layoutIndex]['combinedSeebeckCoefficient']))

    def saveSeebeckCoeff(self):
        seebeckCoeff = self.inSeebeckCoeff.text()
        try: 
            seebeckCoeff = float(seebeckCoeff)
        except:
            return
        self.cache['layouts'][self.currentLayoutIndex]['combinedSeebeckCoefficient'] = seebeckCoeff

    def setOutput(self, layoutIndex):
        structure = self.cache['layouts'][layoutIndex]['electricalStructure']

        self.resElResistance = 0
        for con in structure:
            self.resElResistance += con['specElResistance'] * (con['length']/1000) / (con['crossSection']/1000/1000)
        self.resElResistance *= self.cache['layouts'][layoutIndex]['numberOfElectricalRepetitions']
        self.outputResLabel.setText(f"Resulting Electrical Resistance: {self.resElResistance:e} Ohm") 

        

        
