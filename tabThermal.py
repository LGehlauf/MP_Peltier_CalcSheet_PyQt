from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem
)

class tabThermal(QWidget):
    def __init__(self):
        super().__init__()

        self.inArea = QLineEdit()
        self.inThickness = QLineEdit()
        self.inThermConduct = QLineEdit()

        self.inArea.setPlaceholderText("Area [mm]")
        self.inThickness.setPlaceholderText("Thickness [mm]")
        self.inThermConduct.setPlaceholderText("Thermal Conductivity [W/mK]")

        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Area [mm]", "Thickness [mm]", "Thermal Conductivity [W/mK]"])

        self.add_button = QPushButton("Add Layer")
        self.add_button.clicked.connect(self.addRow)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.inArea)
        form_layout.addWidget(self.inThickness)
        form_layout.addWidget(self.inThermConduct)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def addRow(self):
        area = self.inArea.text()
        thickness = self.inThickness.text()
        thermConduct = self.inThermConduct.text()
        for x in [area, thickness, thermConduct]:
            try:
                x = float(x)
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