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
    try:
        press      = float(ui.pressureLineEdit.text())
    except:
        press = None
    
    try:
        temp       = float(ui.temperatureLineEdit.text())
    except:
        temp = None
    try:
        wind_speed = float(ui.wind_speedLineEdit.text())
    except:
        wind_speed = None
    try:
        rel_hum    = float(ui.relativeHumidityLineEdit.text())
    except:
        rel_hum = None
    try:
        dew_temp   = float(ui.dewPointTemperatureLineEdit.text())
    except:
        dew_temp = None
    try:
        g		   = float(ui.psychrometricConstantLineEdit.text())
    except:
        g = None
    try:
        Rn        =  float(ui.solarRadiationLineEdit.text())
    except:
        Rn = None
    try:
        G         =  float(ui.soilHeatFluxDensityLineEdit.text())
    except:
        G = None
    try:
        D          = float(ui.slopeVapourPressureCurveLineEdit.text())
    except:
        D = None
    try:
        prec = float(ui.precipitationLineEdit.text())
    except:
        prec = None
    pet_tool = pet.PET(press, temp, dew_temp, rel_hum, wind_speed, None,None,g, G, D, Rn, False)
    ans = pet_tool.penman()
    aet_tool = pet.AET(prec, ans)
    aetans = aet_tool.zhang()
    ui.label_16.setText(str(ans)+" mm")
    ui.label_14.setText(str(aetans)+" mm")


def plot(dates, all_vals, ylab,close=True):
    # df = pd.DataFrame(all_vals, index=dates)
    plt.bar(dates, height = all_vals)
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel(ylab)
    plt.savefig("plot.png", dpi=300, bbox_inches='tight')
    # if close:
    plt.close()
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
    poss_labs = ["Pressure", "Temperature", "Dew point Temperature", "Relative Humidity","Wind Speed"]
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
    for i in range(min(30,len(df))):
        if df.iloc[i,checked_op+3] is np.nan:
            continue
        vals.append(df.iloc[i,checked_op+3])
        dates.append(str(df.iloc[i,0])+"-" +str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
    plot(dates, vals, poss_labs[checked_op])
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
    all_aet_vals = []
    dates = []
    for i in range(len(df)):
    # for i in range(min(30,len(df))):
        # print(float(df.iloc[i,0+3]),float(df.iloc[i,1+3]),float(df.iloc[i,2+3]),float(df.iloc[i,3+3]),float(df.iloc[i,4+3]),float(df.iloc[i,5+3]),float(df.iloc[i,6+3]))
        pet_tool = pet.PET(float(df.iloc[i,0+3]),float(df.iloc[i,1+3]),float(df.iloc[i,2+3]),float(df.iloc[i,3+3]),float(df.iloc[i,4+3]),float(df.iloc[i,5+3]),float(df.iloc[i,6+3]),None,None,None,None,True)
        ans = pet_tool.penman()
        if ans is not np.nan:
            all_vals.append(ans)
            aet_tool = pet.AET(float(df.iloc[i,7+3]), ans)
            aet_v = aet_tool.zhang()
            all_aet_vals.append(aet_v)
            dates.append(str(df.iloc[i,0])+"-"+str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
        else:
            all_vals.append(ans)
        # break
    # print(df)
    df['PETo'] = all_vals
    df['AETo'] = all_aet_vals
    df.to_csv("output.csv")
    # plot(dates, all_vals, "ETo",False)
    # plot(dates, all_aet_vals, "ETo",False)
    fileplot(dates,all_vals,all_aet_vals)


    # ui.label_15.setPixmap(QtGui.QPixmap("a.png"))
    # ui.label_15.clear()
    # ui.label_15.setPixmap(1,0)
    pixmap = QPixmap('plot.png')
    ui.label_15.setPixmap(pixmap)

def fileplot(labels,pet,aet):
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, pet, width, label='pet')
    rects2 = ax.bar(x + width/2, aet, width, label='aet')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Scores')
    ax.set_title('AET and PET')
    ax.set_xticks(x)
    ax.set_xticklabels(labels,rotation = 90)
    ax.legend()

    fig.tight_layout()
    plt.savefig("plot.png", dpi=300, bbox_inches='tight')
    plt.close()



app = QtWidgets.QApplication(sys.argv)
WQItool = QtWidgets.QMainWindow()
ui = Ui_WQItool()
ui.setupUi(WQItool)


Actions(ui)


WQItool.show()
sys.exit(app.exec_())
