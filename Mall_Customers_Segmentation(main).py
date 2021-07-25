import tkinter as tk
from tkinter import filedialog
from tkinter.constants import LEFT
from matplotlib import markers
import pandas as pd
from pandas import *
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 1000, height = 300,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Mall Customer Segmentation')
label1.config(font=('helvetica', 24))
canvas1.create_window(500, 40, window=label1)

label2 = tk.Label(root, text='No file chosen.')
label2.config(font=('helvetica', 8))
canvas1.create_window(500, 130, window=label2)

def getFile ():
    
    global df
    import_file_path = filedialog.askopenfilename()
    label2.config(text=import_file_path)
    df = pd.read_csv (import_file_path)

    def getElbow():
        global df
        global X
        X = df.loc[:,["Age", "Annual Income (k$)", "Spending Score (1-100)"]]
        inertia = []
        k = range(1,20)
        for i in k:
            means_k = KMeans(n_clusters=i, random_state=0)
            means_k.fit(X)
            inertia.append(means_k.inertia_)
        fig1 = plt.Figure(figsize=(4,4))
        ax1 = fig1.add_subplot(111)

        ax1.plot(k , inertia , 'bo-')
        ax1.set_xlabel('Number of Clusters')  
        ax1.set_ylabel('Inertia')

        plot1 = FigureCanvasTkAgg(fig1, root) 
        plot1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH,expand=1)

        label3 = tk.Label(root, text='Type Number of Clusters (elbow point):')
        label3.config(font=('helvetica', 8))
        canvas1.create_window(500, 230, window=label3)

        entry1 = tk.Entry (root) 
        canvas1.create_window(500, 250, window=entry1)

        def getKMeans ():
            global df
            global X
            global numberOfClusters
            numberOfClusters = int(entry1.get())

            means_k = KMeans(n_clusters=numberOfClusters, random_state=0)
            means_k.fit(X)
            labels = means_k.labels_
            centroids = means_k.cluster_centers_

            x= X['Spending Score (1-100)']
            y= X['Annual Income (k$)']
            z= X['Age']
            
            fig2 = plt.Figure(figsize=(5,5))
            ax2 = fig2.add_subplot(111, projection='3d')
            cmap = ListedColormap(sns.color_palette("bright",numberOfClusters))

            labels = means_k.labels_

            sc = ax2.scatter(x, y, z,marker='o',c=labels,s=75,alpha=1,cmap=cmap)
            ax2.set_xlabel("Spending Score")
            ax2.set_ylabel("Annual Income")
            ax2.set_zlabel("Age")
            ax2.set_title("Cluster of Customers") 

            ax2.legend(*sc.legend_elements(),bbox_to_anchor=(0,1),loc="upper right", title="Clusters")

            scatter1 = FigureCanvasTkAgg(fig2, root) 
            scatter1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH,expand=1)
        
        processButton = tk.Button(text=' Process k-Means ', command=getKMeans, bg='brown', fg='white', font=('helvetica', 10, 'bold'))
        canvas1.create_window(500, 280, window=processButton)

    elbowbutton = tk.Button(text=" Generate Elbow ", command=getElbow, bg='blue', fg='white', font=('helvetica', 10, 'bold'))
    canvas1.create_window(500, 180, window=elbowbutton)

    
browseButtonCsv = tk.Button(text=" Import Csv File ", command=getFile, bg='green', fg='white', font=('helvetica', 10, 'bold'))
canvas1.create_window(500, 100, window=browseButtonCsv)

root.mainloop()