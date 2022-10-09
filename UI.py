from PyQt5.QtGui import QDoubleValidator

from Project import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from enum import Enum


class SchemeType(Enum):
    SIMPLE_APPARENT = 0
    MODIFIED_APPARENT = 1
    SIMPLE_IMPLICIT = 2
    MODIFIED_IMPLICIT = 3


class PlotWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.schemeType = SchemeType.SIMPLE_APPARENT
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setupRadioButtons()
        self.connectButtons()
        self.setupValidators()
        self.setupStarterParameters()
        self.SimpleApparent.toggle()

    # Setup functions
    def setupRadioButtons(self):
        self.SimpleApparent.toggled.connect(self.setPlottingScheme(SchemeType.SIMPLE_APPARENT))
        self.ModifiedApparent.toggled.connect(self.setPlottingScheme(SchemeType.MODIFIED_APPARENT))
        self.SimpleImplicit.toggled.connect(self.setPlottingScheme(SchemeType.SIMPLE_IMPLICIT))
        self.ModifiedImplicit.toggled.connect(self.setPlottingScheme(SchemeType.MODIFIED_IMPLICIT))

    def setupValidators(self):
        validator = QDoubleValidator()
        self.ParameterI.setValidator(validator)
        self.ParameterS.setValidator(validator)
        self.ParameterT.setValidator(validator)
        self.ParameterAlpha.setValidator(validator)
        self.ParameterU0.setValidator(validator)
        self.ParameterK.setValidator(validator)
        self.ParameterC.setValidator(validator)

    def setupStarterParameters(self):
        self.ParameterI.setText('6')
        self.ParameterS.setText('0.01')
        self.ParameterT.setText('250')
        self.ParameterAlpha.setText('0.003')
        self.ParameterU0.setText('0')
        self.ParameterK.setText('0.065')
        self.ParameterC.setText('1.84')

    def connectButtons(self):
        self.Plotting.clicked.connect(self.plotGraph)

    # Fabric functions
    def setPlottingScheme(self, scheme=SchemeType.SIMPLE_APPARENT):
        def setSimpleApparent():
            self.schemeType = SchemeType.SIMPLE_APPARENT

        def setModifiedApparent():
            self.schemeType = SchemeType.MODIFIED_APPARENT

        def setSimpleImplicit():
            self.schemeType = SchemeType.SIMPLE_IMPLICIT

        def setModifiedImplicit():
            self.schemeType = SchemeType.MODIFIED_IMPLICIT

        if scheme == SchemeType.SIMPLE_APPARENT:
            return setSimpleApparent
        if scheme == SchemeType.MODIFIED_APPARENT:
            return setModifiedApparent
        if scheme == SchemeType.SIMPLE_IMPLICIT:
            return setSimpleImplicit
        if scheme == SchemeType.MODIFIED_IMPLICIT:
            return setModifiedImplicit

    # Other functions

    def plotGraph(self):
        pass
