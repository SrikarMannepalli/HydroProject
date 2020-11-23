from Gui import Ui_WQItool
import sys
import pet
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd 
import matplotlib.pyplot as plt
filename = None

def Actions(ui):
    ui.pushButton.clicked.connect(SingleETOcalculator)
    ui.solarRadiationLineEdit.setText(str("0.19")) #for now
    ui.pushButton_2.clicked.connect(Filepicker)
    ui.pushButton_3.clicked.connect(FileETOcalculator)
    ui.pushButton_4.clicked.connect(plot_individual)

def SingleETOcalculator():
    press      = float(ui.pressureLineEdit.text())
    temp       = float(ui.temperatureLineEdit.text())
    wind_speed = float(ui.wind_speedLineEdit.text())
    rel_hum    = float(ui.relativeHumidityLineEdit.text())
    dew_temp   = float(ui.dewPointTemperatureLineEdit.text())
    g		   = float(ui.psychrometricConstantLineEdit.text())
    Rn        =  float(ui.solarRadiationLineEdit.text())
    G         =  float(ui.soilHeatFluxDensityLineEdit.text())
    D          = float(ui.slopeVapourPressureCurveLineEdit.text())
    pet_tool = pet.PET(press, temp, dew_temp, rel_hum, wind_speed, None,None,g, G, D, Rn, False)
    ans = pet_tool.penman()
    ui.label_14.setText(str(ans))


def plot(dates, all_vals):
    # df = pd.DataFrame(all_vals, index=dates)
    plt.bar(dates, height = all_vals)
    plt.xticks(rotation='vertical')
    plt.savefig("plot.png", dpi=300, bbox_inches='tight')

    # plt.imsave(white, 'white.png', dpi=300, bbox_inches='tight')
    # x = [0, 2, 4, 6,10,11]
    # y = [1, 3, 4, 8,9,6]
    # plt.plot(x,y)
    # plt.xlabel('x values')
    # plt.ylabel('y values')
    # plt.title('plotted x and y values')
    # plt.legend(['line 1'])
    # plt.savefig('plot.png', dpi=300, bbox_inches='tight')

def plot_individual():
    # filename = ui.label_13.text()
    global filename
    df = pd.read_csv(filename)
    checked_op = None
    if ui.radioButton.isChecked(): #pressure
        checked_op=0
    elif ui.radioButton_2.isChecked(): #temperature
        checked_op=1
    elif ui.radioButton_3.isChecked(): #windspeed
        checked_op=4
    elif ui.radioButton_4.isChecked(): #relative humidity
        checked_op=3
    elif ui.radioButton_5.isChecked(): #dew temp
        checked_op=2

    vals = []
    dates = []    
    for i in range(30):
        if df.iloc[i,checked_op+3] is np.nan:
            continue
        vals.append(df.iloc[i,checked_op+3])
        dates.append(str(df.iloc[i,0])+"-" +str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
    plot(dates, vals)
    # ui.label_15.clear()
    # ui.label_15.setPixmap(1,0)
    pixmap = QPixmap('plot.png')
    ui.label_15.setPixmap(pixmap)


def Filepicker():
    name,typ =QFileDialog.getOpenFileName()
    global filename
    filename = name
    ui.label_13.setText(name.split("/")[-1].split(".")[0])

def FileETOcalculator():
    # filename = ui.label_13.text()
    global filename
    df = pd.read_csv(filename)
    all_vals = []
    dates = []
    # for i in range(len(df)):
    for i in range(30):
        # print(float(df.iloc[i,0+3]),float(df.iloc[i,1+3]),float(df.iloc[i,2+3]),float(df.iloc[i,3+3]),float(df.iloc[i,4+3]),float(df.iloc[i,5+3]),float(df.iloc[i,6+3]))
        pet_tool = pet.PET(float(df.iloc[i,0+3]),float(df.iloc[i,1+3]),float(df.iloc[i,2+3]),float(df.iloc[i,3+3]),float(df.iloc[i,4+3]),float(df.iloc[i,5+3]),float(df.iloc[i,6+3]),None,None,None,None,True)
        ans = pet_tool.penman()
        if ans is not np.nan:
            all_vals.append(ans)
            dates.append(str(df.iloc[i,0])+"-"+str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
        # break
    # print(df)
    plot(dates, all_vals)
    # ui.label_15.setPixmap(QtGui.QPixmap("a.png"))
    # ui.label_15.clear()
    # ui.label_15.setPixmap(1,0)
    pixmap = QPixmap('plot.png')
    ui.label_15.setPixmap(pixmap)




app = QtWidgets.QApplication(sys.argv)
WQItool = QtWidgets.QMainWindow()
ui = Ui_WQItool()
ui.setupUi(WQItool)


Actions(ui)


WQItool.show()
sys.exit(app.exec_())
