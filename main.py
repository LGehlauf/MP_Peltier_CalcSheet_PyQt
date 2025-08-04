import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableView, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyApp")
        self.setFixedSize(QSize(400, 300))

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Alter", "Stadt"])

        self.view = QTableView()
        self.view.setModel(self.model)

        self.button = QPushButton("Zeile hinzufügen")
        self.button.clicked.connect(self.add_row)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_row(self):
        data = ["Max", "30", "Berlin"]
        items = [QStandardItem(field) for field in data]
        self.model.appendRow(items)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()