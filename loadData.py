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
    trials_ind: list
        List that contains the indeces for every trial start.

    trials_list: list
        List that contains the data frames with individual trial data.
    """

    # load the data from csv
    data = pd.read_csv(fileName, delimiter= ",", names= ['Event', 'Value_1', 'Value_2'], skiprows= 2, skip_blank_lines= True, error_bad_lines= False)

    # first get the list of valid trials and the number of trials
    trialNum_list = data.loc[data.Event == 'Trial#']['Value_1']
    trialNum = len(trialNum_list)

    # get the indeces for each trial
    trials_ind = np.array([])
    for i in  trialNum_list:
        iti = data.loc[(data.loc[data.Event == 'Trial#']).loc[data.Value_1 == i].index[0]+1]['Value_1']
        temp = (data.loc[data.Event == 'Trial#']).loc[data.Value_1 == i].index[0]
        (data.loc[data.Event == 'Trial#']).loc[data.Value_1 == i].index[0]
        trials_ind = np.append(trials_ind, temp)

    trials_list = []
    for i in range(0, len(trials_ind)):
        if i < trialNum-1:
            temp = (data.loc[trials_ind[i]:trials_ind[i+1]-1])
        else:
            temp = (data.loc[trials_ind[i]:len(data)-1])
        trials_list.append(temp)

    return trials_list, trials_ind, trialNum_list, trialNum

if __name__ == "__main__":
    #filenames = chooseFile()
    [trials_list, trials_ind, trialNum_list, trialNum] = loadData("C:\Users\hakan\Documents\git repos\MousyBox\\7792\\7792_Day09.csv")
    #print(trials_list)

    #data = pd.read_csv("C:\Users\hakan\Documents\git repos\MousyBox\\7792\\7792_Day09.csv", delimiter= ",", names= ['Event', 'Value_1', 'Value_2'], skiprows= 2, skip_blank_lines= True, error_bad_lines= False)
    #print data
