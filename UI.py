from PyQt5.QtGui import QDoubleValidator

from Project import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from enum import Enum

from DifferentiationScheme import DifferentiationScheme

class SchemeType(Enum):
    SIMPLE_APPARENT = 0
    MODIFIED_APPARENT = 1
    SIMPLE_IMPLICIT = 2
    MODIFIED_IMPLICIT = 3


class PlottingType(Enum):
    X = 0
    T = 1


class PlotWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.schemeType = SchemeType.SIMPLE_APPARENT
        self.plottingType = PlottingType.X
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)
        self.params = {"l": 6,
                       "s": 0.01,
                       'T': 250,
                       'alpha': 0.003,
                       'U_0': 0,
                       'k': 0.065,
                       'c': 1.84,
                       't': 125,
                       'I': 50,
                       'K': 10000,
                       'x': 3}
        self.setupUi(self)
        self.setupRadioButtons()
        self.connectButtons()
        self.setupValidators()
        self.setupStarterParameters()
        self.SimpleApparent.toggle()
        self.XGraph.toggle()
        self.difSchemes = DifferentiationScheme(self.params)
        self.drawn = False
        self.Plotting_2.setEnabled(False)

    # Setup functions
    def setupRadioButtons(self):
        self.SimpleApparent.toggled.connect(self.setPlottingScheme(SchemeType.SIMPLE_APPARENT))
        self.ModifiedApparent.toggled.connect(self.setPlottingScheme(SchemeType.MODIFIED_APPARENT))
        self.SimpleImplicit.toggled.connect(self.setPlottingScheme(SchemeType.SIMPLE_IMPLICIT))
        self.ModifiedImplicit.toggled.connect(self.setPlottingScheme(SchemeType.MODIFIED_IMPLICIT))
        self.XGraph.toggled.connect(self.setPlottingTypeAndBlockButton(PlottingType.X))
        self.TGraph.toggled.connect(self.setPlottingTypeAndBlockButton(PlottingType.T))

    def setupValidators(self):
        validator = QDoubleValidator()
        self.ParameterL.setValidator(validator)
        self.ParameterS.setValidator(validator)
        self.ParameterT.setValidator(validator)
        self.ParameterAlpha.setValidator(validator)
        self.ParameterU0.setValidator(validator)
        self.ParameterK.setValidator(validator)
        self.ParameterKSmall.setValidator(validator)
        self.ParameterC.setValidator(validator)
        self.ParameterTSmall.setValidator(validator)
        self.ParameterI.setValidator(validator)
        # self.ParameterX.setValidator(validator)

    def setupStarterParameters(self):
        self.ParameterS.setText(str(self.params['s']))
        self.ParameterT.setText(str(self.params['T']))
        self.ParameterAlpha.setText(str(self.params['alpha']))
        self.ParameterU0.setText(str(self.params['U_0']))
        self.ParameterK.setText(str(self.params['K']))
        self.ParameterC.setText(str(self.params['c']))
        self.ParameterTSmall.setText(str(self.params['t']))
        self.ParameterI.setText(str(self.params['I']))
        self.ParameterKSmall.setText(str(self.params['k']))
        self.ParameterL.setText(str(self.params['l']))
        self.ParameterX.setText(str(self.params['x']))

    def connectButtons(self):
        self.Plotting.clicked.connect(self.plotGraph)
        self.Plotting_2.clicked.connect(self.addPlot)

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

    def setPlottingTypeAndBlockButton(self, plotType=PlottingType.X):
        def setXGraph():
            self.plottingType = PlottingType.X

        def setTGraph():
            self.plottingType = PlottingType.T

        if plotType == PlottingType.X:
            return setXGraph
        if plotType == PlottingType.T:
            return setTGraph



    # Other functions

    def getNewParams(self):
        self.params['I'] = float(self.ParameterI.text())
        self.params['l'] = float(self.ParameterL.text())
        self.params['s'] = float(self.ParameterS.text())
        self.params['alpha'] = float(self.ParameterAlpha.text())
        self.params['k'] = float(self.ParameterKSmall.text())
        self.params['c'] = float(self.ParameterC.text())
        self.params['T'] = float(self.ParameterT.text())
        self.params['x'] = float(self.ParameterX.text())
        self.params['t'] = float(self.ParameterTSmall.text())
        self.params['K'] = float(self.ParameterK.text())
        self.params['U_0'] = float(self.ParameterU0.text())
        self.difSchemes.setNewParams(self.params)

    def plotGraph(self):
        if not self.Plotting_2.isEnabled():
            self.Plotting_2.setEnabled(True)
        self.Graphics.clearPlot()
        self.addPlot()

    def addPlot(self):
        self.getNewParams()
        x, y, label, xLabel, yLabel = None, None, None, None, None
        if self.plottingType == PlottingType.X:
            xLabel = 'x, Длина'
            yLabel = 'U, Температура'
            if self.schemeType == SchemeType.SIMPLE_APPARENT:
                x, y, label = self.difSchemes.SimpleApparentX()
            elif self.schemeType == SchemeType.MODIFIED_APPARENT:
                x, y, label = self.difSchemes.ModifiedApparentX()
            elif self.schemeType == SchemeType.SIMPLE_IMPLICIT:
                x, y, label = self.difSchemes.SimpleImplicitX()
            elif self.schemeType == SchemeType.MODIFIED_IMPLICIT:
                x, y, label = self.difSchemes.ModifiedImplicitX()
        elif self.plottingType == PlottingType.T:
            xLabel = 't, Время'
            yLabel = 'U, Температура'
            if self.schemeType == SchemeType.SIMPLE_APPARENT:
                x, y, label = self.difSchemes.SimpleApparentT()
            elif self.schemeType == SchemeType.MODIFIED_APPARENT:
                x, y, label = self.difSchemes.ModifiedApparentT()
            elif self.schemeType == SchemeType.SIMPLE_IMPLICIT:
                x, y, label = self.difSchemes.SimpleImplicitT()
            elif self.schemeType == SchemeType.MODIFIED_IMPLICIT:
                x, y, label = self.difSchemes.ModifiedImplicitT()
        self.Graphics.setLabels(xLabel, yLabel)
        self.Graphics.addPlot(x, y, label)
        self.Graphics.draw()


