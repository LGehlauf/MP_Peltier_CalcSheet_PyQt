import sys
# from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
from tabThermal import tabThermal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        cache = readJson()
        self.setWindowTitle("MyApp")
        # self.setFixedSize(QSize(400, 300))

        tabs = QTabWidget()
        tabs.addTab(tabThermal(), "Thermal Input")

        self.setCentralWidget(tabs)

    def readJson():
        with open('cache.json', 'r') as file:
            try:
                return(json.load(file))
            except:
                return(dict())
            

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()