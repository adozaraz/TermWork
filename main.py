from UI import PlotWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ in "__main__":
    app = QApplication(sys.argv)

    window = PlotWindow()
    window.show()

    app.exec()
