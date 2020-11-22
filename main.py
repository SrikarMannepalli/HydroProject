from Gui import Ui_WQItool
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd 
import matplotlib.pyplot as plt
def Actions(ui):
    ui.pushButton.clicked.connect(SingleETOcalculator)
    ui.solarRadiationLineEdit.setText(str("0.19")) #for now
    ui.pushButton_2.clicked.connect(Filepicker)
    ui.pushButton_3.clicked.connect(FileETOcalculator)

def SingleETOcalculator():
    press      = ui.pressureLineEdit.text()
    temp       = ui.temperatureLineEdit.text()
    wind_speed = ui.wind_speedLineEdit.text()
    rel_hum    = ui.relativeHumidityLineEdit.text()
    dew_temp   = ui.dewPointTemperatureLineEdit.text()
    #		   = ui.psychrometricConstantLineEdit.text()
    #Rn        = ui.solarRadiationLineEdit.text()
    #          = ui.soilHeatFluxDensityLineEdit.text()
    #          = ui.slopeVapourPressureCurveLineEdit.text()
    ans = 100 # calculate using funct
    ui.label_14.setText(str(ans))


def plot():
    x = [0, 2, 4, 6,10,11]
    y = [1, 3, 4, 8,9,6]
    plt.plot(x,y)
    plt.xlabel('x values')
    plt.ylabel('y values')
    plt.title('plotted x and y values')
    plt.legend(['line 1'])
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')


def Filepicker():
    name,typ =QFileDialog.getOpenFileName()
    ui.label_13.setText(name)
def FileETOcalculator():
    filename = ui.label_13.text()
    df = pd.read_csv(filename)
    # print(df)
    plot()
    pixmap = QPixmap('plot.png')
    ui.label_15.setPixmap(pixmap)




app = QtWidgets.QApplication(sys.argv)
WQItool = QtWidgets.QMainWindow()
ui = Ui_WQItool()
ui.setupUi(WQItool)


Actions(ui)


WQItool.show()
sys.exit(app.exec_())
