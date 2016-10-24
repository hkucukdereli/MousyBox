import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Tkinter import Tk
from tkFileDialog import askopenfilename,askdirectory

def chooseFile():
    """
    Parameters
    ----------
    None
        No parameters are specified.

    Returns
    -------
    filenames: tuple
        A tuple that contains the list of files to be loaded.
    """

    root = Tk()
    root.withdraw()
    filenames = askopenfilename(parent= root, filetypes = (("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")), multiple= True)
    if len(filenames) == 1:
        print len(filenames), " file is loaded."
    elif len(filenames) > 1:
        print len(filenames), " files are loaded."
    else:
        print "No files are loaded."

    return filenames

def loadData(fileName):
    """
    Parameters
    ----------
    fileName: string
        Input file name as a legal string.

    Returns
    -------
    data: pandas data frame
        All the data from the file.

    """

    # load the data from csv
    data = pd.read_excel(fileName, header= 0, skiprows= 33, convert_float= True, na_values= '-')
    data = data.drop(0)

    return data

if __name__ == "__main__":
    #filenames = chooseFile()
    data = loadData("C:\Users\hakan\Documents\git repos\MousyBox\\tracks.xlsx")

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), facecolor='w', dpi= 150)
    ax.scatter(data['X center'], data['Y center'], color= 'gray', linewidth= 0, s= 5)
    #data.plot(kind= 'scatter', x= 'X center', y = 'Y center', color= 'gray', linewidth= 0)
    ax.scatter(data['X center'].mean(), data['Y center'].mean(), color= 'red', linewidth= 0, s= 25)
    plt.tight_layout()
    plt.show()
