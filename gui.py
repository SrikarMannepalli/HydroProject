import wqi
import vis
import tkinter as tk
from tkinter import ttk 
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
import pandas as pd
import homepage
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from geopy.geocoders import Nominatim
import time

root = tk.Tk()
root.wm_title("Water Quality Index Estimation Tool")
root.geometry("900x600")
tabControl = ttk.Notebook(root) 


home = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl) 
tab4 = ttk.Frame(tabControl) 
tabControl.add(home, text ='HOME') 
tabControl.add(tab1, text ='TASK 1') 
tabControl.add(tab2, text ='TASK 2') 
tabControl.add(tab3, text ='TASK 3') 
# tabControl.add(tab4, text ='VIZ') 

tabControl.pack(expand = 1, fill ="both") 

csv =None
csv_q2 = None
csv_q3 = None
df_q3 = None

def add_tab1(tab1, tab4):
	head = tk.Label(tab1, text="TASK 1", font=("Verdana", 20))
	head.place(x=400,y=10)

	attrs = ["pH", "Temperature"," Turbidity","TDS","Nitrates","Fecal Coliform"]
	labs = []
	ets = []
	for i in range(len(attrs)):
		labs.append(tk.Label(tab1, text=attrs[i]))
		ets.append(tk.Entry(tab1))
		labs[i].place(x = 200, y = 50 + (50 * i))
		ets[i].place(x = 450, y = 50 + (50 * i))

	def open_file():
		file = filedialog.askopenfilename(title = "choose your file",filetypes =[('csv files','*.csv')])
		global csv 
		csv = pd.read_csv(file)

	btn = Button(tab1, text ='Choose file', command = lambda:open_file()) 
	# btn.grid(row=6,column=1)
	btn.place(x=420, y=400)
	out_name = tk.Label(tab1, text="Output File Name")
	out_name.place(x=200, y=450)
	ets.append(tk.Entry(tab1))
	ets[-1].place(x=450, y=450)

	classes = ["Very Bad", "Bad", "Medium", "Good", "Excellent"]
	def show_entry_fields():
		qual_ind_vec = []
		qual_cls_vec = []
		if csv is not None:
			for i in range(len(csv)) : 
				# print(csv.iloc[i, 0], csv.iloc[i, 2]) 
				if 'NIT' not in csv:
					csv['NIT'] = 0.5
				if 'FEC' not in csv:
					csv['FEC'] = 0
				# print(csv.iloc[i, 6],csv.iloc[i, 3],csv.iloc[i, 11],csv.iloc[i, 5],csv.iloc[i, 18],csv.iloc[i, 19])
				qual_ind = wqi.q1_main(csv.iloc[i, 6],csv.iloc[i, 3],csv.iloc[i, 11],csv.iloc[i, 5],csv.iloc[i, 18],csv.iloc[i, 19])
				# tk.Label(tab1,text=qual_ind).grid(row=i,column=7)
				if qual_ind>=0 and qual_ind<25:
					wq_clss = classes[0]
				elif qual_ind>=25 and qual_ind<50:
					wq_clss = classes[1]
				elif qual_ind>=50 and qual_ind<70:
					wq_clss = classes[2]
				elif qual_ind>=70 and qual_ind<90:
					wq_clss = classes[3]
				else:
					wq_clss = classes[4]
				qual_ind_vec.append(qual_ind)
				qual_cls_vec.append(wq_clss)
		
			csv["WQI"] = qual_ind_vec
			csv["WQC"] = qual_cls_vec
			outputfname = ets[-1].get()

			if not outputfname:
				outputfname = "out.csv"
			csv.to_csv(outputfname, index=False)
			# vis.q1(csv)
		else:
			evals = [float(et.get()) for et in ets[:-1]]
			qual_ind = wqi.q1_main(evals[0],evals[1],evals[2],evals[3],evals[4],evals[5])
			if qual_ind>=0 and qual_ind<25:
				wq_clss = classes[0]
			elif qual_ind>=25 and qual_ind<50:
				wq_clss = classes[1]
			elif qual_ind>=50 and qual_ind<70:
				wq_clss = classes[2]
			elif qual_ind>=70 and qual_ind<90:
				wq_clss = classes[3]
			else:
				wq_clss = classes[4]
				
					
			wq = tk.Label(tab1,text=qual_ind, font=("Verdana",15))
			wq_lab = tk.Label(tab1,text="WQI", font=("Verdana",20))
			wq_class = tk.Label(tab1,text="WQC", font=("Verdana",20))
			wq_class_val = tk.Label(tab1,text=wq_clss, font=("Verdana",15))
			wq.place(x=700, y=300)
			wq_lab.place(x=700, y=250)
			wq_class.place(x=700, y=350)
			wq_class_val.place(x=700, y=400)
	
	def show_entry_fields1():
		qual_ind_vec = []
		qual_cls_vec = []
		
		evals = [float(et.get()) for et in ets[:-1]]
		qual_ind = wqi.q1_main(evals[0],evals[1],evals[2],evals[3],evals[4],evals[5])
		if qual_ind>=0 and qual_ind<25:
			wq_clss = classes[0]
		elif qual_ind>=25 and qual_ind<50:
			wq_clss = classes[1]
		elif qual_ind>=50 and qual_ind<70:
			wq_clss = classes[2]
		elif qual_ind>=70 and qual_ind<90:
			wq_clss = classes[3]
		else:
			wq_clss = classes[4]
			
				
		wq = tk.Label(tab1,text=qual_ind, font=("Verdana",15))
		wq_lab = tk.Label(tab1,text="WQI", font=("Verdana",20))
		wq_class = tk.Label(tab1,text="WQC", font=("Verdana",20))
		wq_class_val = tk.Label(tab1,text=wq_clss, font=("Verdana",15))
		wq.place(x=700, y=300)
		wq_lab.place(x=700, y=250)
		wq_class.place(x=700, y=350)
		wq_class_val.place(x=700, y=400)

	qt = tk.Button(tab1, text='QUIT', command=tab1.quit)
	qt.place(x=500, y=500)
	calc = tk.Button(tab1, text='CALCULATE', command=show_entry_fields)
	calc.place(x=350, y=500)
	calc1 = tk.Button(tab1, text='CALCULATE', command=show_entry_fields1)
	calc1.place(x=350, y=350)
	viz = tk.Button(tab1, text='VISUALIZE', command=lambda:get_vis(tab4, csv))
	viz.place(x=600, y=500)


def add_tab2(tab2, tab4):
	head = tk.Label(tab2, text="TASK 2", font=("Verdana", 20))
	head.place(x=400,y=10)
	atts = ["Turbidity", "pH","Color","DO", "BOD","TDS", "Hardness","Cl","No3","So4","Coliform","As","F"]
	classes2 = ["Heavily polluted", "Polluted", "Slightly polluted", "Acceptable", "Excellent"]
	labs = []
	ets= []
	for i in range(0, len(atts)):
		labs.append(tk.Label(tab2, text=atts[i]))
		ets.append(tk.Entry(tab2))
		labs[i].place(x = 200, y = 50 + (30 * i))
		ets[i].place(x = 450, y = 50 + (30 * i))

	def open_file():
		file = filedialog.askopenfilename(title = "choose your file",filetypes =[('csv files','*.csv')])
		global csv_q2
		csv_q2 = pd.read_csv(file)

	btn = Button(tab2, text ='Choose file', command = lambda:open_file()) 
	btn.place(x=420, y=450)
	out_name = tk.Label(tab2, text="Output File Name")
	out_name.place(x=200, y=500)
	ets.append(tk.Entry(tab2))
	ets[-1].place(x=450, y=500)

	def show_entry_fields():
		qual_ind_vec = []
		qual_cls_vec = []
		if csv_q2 is not None:
			for i in range(len(csv_q2)) : 
				# print(csv_q2.iloc[i, 0], csv_q2.iloc[i, 2]) 
				pars = [csv_q2.iloc[i,j] for j in range(4, 17)]
				qual_ind = wqi.q2_main(pars)
				# print(qual_ind)
				if qual_ind>=0 and qual_ind<=1:
					wq_clss = classes2[4]
				elif qual_ind>1 and qual_ind<=2:
					wq_clss = classes2[3]
				elif qual_ind>2 and qual_ind<=4:
					wq_clss = classes2[2]
				elif qual_ind>4 and qual_ind<=8:
					wq_clss = classes2[1]
				elif qual_ind>8:
					wq_clss = classes2[0]
				qual_ind_vec.append(qual_ind)
				qual_cls_vec.append(wq_clss)
				# tk.Label(tab1,text=qual_ind).grid(row=i,column=7)
		
			csv_q2["OIP"] = qual_ind_vec
			csv_q2["WQC"] = qual_cls_vec
			outputfname = ets[-1].get()
			if not outputfname:
				outputfname = "out.csv"
			csv_q2.to_csv(outputfname, index=False)

			# vis.q2(csv_q2)
		else:
			evals = [float(et.get()) for et in ets[:-1]]
			qual_ind = wqi.q2_main(evals)
			# print(qual_ind)
			if qual_ind>=0 and qual_ind<=1:
				wq_clss = classes2[4]
			elif qual_ind>1 and qual_ind<=2:
				wq_clss = classes2[3]
			elif qual_ind>2 and qual_ind<=4:
				wq_clss = classes2[2]
			elif qual_ind>4 and qual_ind<=8:
				wq_clss = classes2[1]
			elif qual_ind>8:
				wq_clss = classes2[0]
				
					
			wq = tk.Label(tab2,text=qual_ind, font=("Verdana",15))
			wq_lab = tk.Label(tab2,text="OIP", font=("Verdana",20))
			wq_class = tk.Label(tab2,text="WQC", font=("Verdana",20))
			wq_class_val = tk.Label(tab2,text=wq_clss, font=("Verdana",15))
			wq.place(x=700, y=300)
			wq_lab.place(x=700, y=250)
			wq_class.place(x=700, y=350)
			wq_class_val.place(x=700, y=400)
	
	def show_entry_fields1():

		evals = [float(et.get()) for et in ets[:-1]]
		qual_ind = wqi.q2_main(evals)
		# print(qual_ind)
		if qual_ind>=0 and qual_ind<=1:
			wq_clss = classes2[4]
		elif qual_ind>1 and qual_ind<=2:
			wq_clss = classes2[3]
		elif qual_ind>2 and qual_ind<=4:
			wq_clss = classes2[2]
		elif qual_ind>4 and qual_ind<=8:
			wq_clss = classes2[1]
		elif qual_ind>8:
			wq_clss = classes2[0]
			
				
		wq = tk.Label(tab2,text=qual_ind, font=("Verdana",15))
		wq_lab = tk.Label(tab2,text="OIP", font=("Verdana",20))
		wq_class = tk.Label(tab2,text="WQC", font=("Verdana",20))
		wq_class_val = tk.Label(tab2,text=wq_clss, font=("Verdana",15))
		wq.place(x=700, y=300)
		wq_lab.place(x=700, y=250)
		wq_class.place(x=700, y=350)
		wq_class_val.place(x=700, y=400)

	qt = tk.Button(tab2, text='QUIT', command=tab2.quit)
	qt.place(x=500, y=540)
	calc = tk.Button(tab2, text='CALCULATE', command=show_entry_fields)
	calc.place(x=350, y=540)
	calc1 = tk.Button(tab2, text='CALCULATE', command=show_entry_fields1)
	calc1.place(x=650, y=150)
	viz = tk.Button(tab2, text='VISUALIZE', command=lambda:get_vis_q2(tab4, csv_q2))
	viz.place(x=600, y=540)

def add_tab3(tab3, tab4):
	head = tk.Label(tab3, text="TASK 3", font=("Verdana", 20))
	head.place(x=400,y=10)

	def open_file():
		file = filedialog.askopenfilename(title = "choose your file",filetypes =[('csv files','*.csv')])
		global csv_q3
		csv_q3 = pd.read_csv(file)

	btn = Button(tab3, text ='Choose file', command = lambda:open_file()) 
	btn.place(x=420, y=320)
	out_name = tk.Label(tab3, text="Output File Name")
	out_name.place(x=200, y=420)
	ent = tk.Entry(tab3)
	ent.place(x=450, y=420) 

	# df = pd.DataFrame()
	# if csv_q3 is not None:
	# 	df = wqi.q3_main(csv_q3)
	# global csv_q3
	df_train = pd.read_csv('./timeseries_train.csv')
	df_name = df_train.groupby('Name').mean().reset_index()

	n = tk.StringVar() 
	
	st_name = tk.Label(tab3, text="Station Name")
	st = ttk.Combobox(tab3, text = "Station", width = 40, textvariable = n) 
	st_name.place(x = 200, y = 200)
	st.place(x=350, y=200)

	# # Adding combobox drop down list 
	st['values'] = df_name['Name'].tolist()

	def ok():
		val = n.get()
		dfC = df_train[df_train['Name'] == val]
		df_q3 = wqi.q3_main(dfC, df_train)

		return df_q3



	def show_entry_fields():
		global df_q3
		if csv_q3 is not None:
			df_q3 = wqi.q3_main(csv_q3, df_train)
			df_q3.to_csv(ent.get(),index=False)
		else:
			df_q3 = ok()
		
	qt = tk.Button(tab3, text='QUIT', command=tab3.quit)
	qt.place(x=450, y=500)
	calc = tk.Button(tab3, text='CALCULATE', command=show_entry_fields)
	calc.place(x=300, y=500)
	viz = tk.Button(tab3, text='VISUALIZE', command=lambda:get_vis_q3(tab4, df_q3))
	viz.place(x=550, y=500)

def get_vis(tab4, df):
	# print("hi")

	fig = plt.figure(figsize=(10,10))

	# tabControl.select(tab4)
	df_new = df[['Name', 'lat', 'long', 'WQI', 'WQC']]
	vis.q1(df_new)

	# print(df_new)
	# print(df.loc)
	df_final = df.loc[df.groupby(["Name"])["WQI"].idxmin()]
	# df_add = df.loc[df.groupby(["Name"])["WQI"].idxmin()]
	# df_final = df_new.append(df_add)
	# df_final = df_new.groupby(['Name'])['WQI'].idxmax().reset_index()

	# print(df_final)
	# fig, ax = plt.subplots()
	ind_img = mpimg.imread('./india-rivers-map.jpg')
	plt.imshow(ind_img,extent=[68.7, 96.25, 7.4, 37.6], alpha=0.75)
	colors = {'Excellent':'blue','Good':'c','Medium':'purple','Bad':'violet','Very Bad':'red'}
	classes = ["Very Bad", "Bad", "Medium", "Good", "Excellent"]
	labs=[]
	for clsa in df_final["WQC"]:
		labs.append(classes.index(clsa))
	latitudes = df['lat'].to_numpy()
	longitudes = df['long'].to_numpy()
	wqis = df['WQI'].to_numpy()
	wqc = df['WQC'].to_numpy()
	# for longi,lat in zip(df_final["long"], df_final["lat"]):
	# 	plt.scatter(longi, lat) 
	cols=[]
	for i in range(len(wqis)):
		cols.append(colors[wqc[i]])
	sc = plt.scatter(longitudes,latitudes,c=cols,s=100, alpha=0.75,cmap=plt.cm.coolwarm)
	plt.legend(*sc.legend_elements(),title="WQI", loc="lower right")
	plt.text(90,15+4,"Legend",fontsize=20)
	plt.text(90,14+4,"Blue: Excellent",fontsize=10)
	plt.text(90,13+4,"Cyan: Good",fontsize=10)
	plt.text(90,12+4,"Purple: Medium",fontsize=10)
	plt.text(90,11+4,"Violet: Bad",fontsize=10)
	plt.text(90,10+4,"Red: Very Bad",fontsize=10)
	plt.show()

	# scatter = ax.scatter(df_final["long"], df_final["lat"],c=labs,s=10)
	# print(*scatter.legend_elements()[0])
	# legend1 = ax.legend(*scatter.legend_elements(),
    #             loc="lower left", title="Classes")
	# ax.add_artist(legend1)


	# canvas = FigureCanvasTkAgg(fig, master=tab4)
	# canvas.draw()
	# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

	# toolbar = NavigationToolbar2Tk(canvas, tab4)
	# toolbar.update()
	# canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

def get_vis_q2(tab5, df):
	# tabControl.select(tab5)

    fig = plt.figure(figsize=(10,10))
    title = "Plot based on water quality"
    # plt.title(title)
    ind_img = mpimg.imread('./india-rivers-map.jpg')
    plt.imshow(ind_img,extent=[68.7, 96.25, 7.4, 37.6], alpha=0.75)
    latitudes = df['lats'].to_numpy()
    longitudes = df['longs'].to_numpy()
    station = df['STATION'].to_numpy()
    wqis = df['OIP'].to_numpy()
    wqc = df['WQC'].to_numpy()
    colors = {'Excellent':'blue','Acceptable':'c','Slightly polluted':'purple','Polluted':'violet','Heavily polluted':'red'}
    #colors = sb.heatmap(normalised)
    for i in range(len(wqis)):
        plt.scatter(longitudes[i],latitudes[i], color=colors[wqc[i]],s=100, alpha=0.75, label=station[i]+":"+str(wqc[i]))
    plt.legend(title="WQI", loc="lower right")
    plt.show()

def get_vis_q3(tab4, df):
	
	# print(df)
	fig = plt.figure(figsize=(10,10))
	df_new = df[['Station', 'Sample Date', 'WQI']]

	df_new['Sample Date'] = df_new['Sample Date'].str.split("-", n = 1, expand = True)[0]

	final = df_new.groupby('Sample Date').max().reset_index()

	# print(final)
	# ax = final.plot.bar(x="Sample Date", y="WQI", rot=0, figsize = (15, 15))
	plt.bar(x=final["Sample Date"],height=final["WQI"])
	plt.xlabel("Year")
	plt.ylabel("WQI")
	plt.show()
	

homepage.add_home(home)
add_tab1(tab1,tab4)
add_tab2(tab2,tab4)
add_tab3(tab3,tab4)
# get_vis(tab4)
root.mainloop()