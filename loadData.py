import os
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

    ## change the wd to dir containing the script
    curpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(curpath)

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
        Data frame that contains the raw data.

    trialNum: pandas data frame
        Data frame that contains the valid trial numbers.

    Trials_list: dict
        Dict that contains sorted trial data.
    """

    # load the data from csv
    data = pd.read_csv(fileName, delimiter= ",", names= ['Event', 'Value_1', 'Value_2'], skip_blank_lines= True, error_bad_lines= False)

    # groupd the data
    grouped = data.groupby('Event')

    trialNum = grouped.get_group('Trial#')
    trialNew = grouped.get_group('Trial_New')
    trialEnd = grouped.get_group('Trial_End').iloc[1:]
    trialEnd = trialEnd.append(data.tail(1))

    Trials_list = {}
    for ind, each in enumerate(trialNum['Value_1']):
        ind_head = trialNum.iloc[ind].name
        ind_tail = trialEnd.iloc[ind].name
        #Trials_list.append(data.iloc[ind_head : ind_tail].sort())
        Trials_list[int(each)] = data.iloc[ind_head : ind_tail].sort_values(by= 'Value_2')

    return data, trialNum, Trials_list

def getLicks(trialNum, Trials_list, th= 0):
    """
    Parameters
    ----------
    trialNum: pandas data frame
        Data frame that contains the valid trial numbers.

    Trials_list: dict
        Dict that contains sorted trial data.

    th: int
        Threshold value for digitizing tha lick values. Default is 0.

    Returns
    -------
    Licks: pandas data frame
        Data frame that contains the timestamps, raw and digitized lick values.
        Columns: LickTime, LickDigi, LickRaw
    """

    Licks = {}
    for ind, each in enumerate(trialNum['Value_1']):
        lick_times = np.array(Trials_list[int(each)][Trials_list[int(each)]['Event'] == 'Lick']['Value_2'])
        lick_values = np.array(Trials_list[int(each)][Trials_list[int(each)]['Event'] == 'Lick']['Value_1'])
        Licks[int(each)] = pd.DataFrame({'LickTime' : lick_times, 'LickRaw' : lick_values, 'LickDigi' : np.digitize(lick_values, bins= [th])})

    return Licks

def findLicks(trialNum, Licks):
    """
    Parameters
    ----------
    trialNum: pandas data frame
        Data frame that contains the valid trial numbers.

    Licks: pandas data frame
        lorem ipsum.

    Returns
    -------
    Licks: pandas data frame
        lorem ipsum.
        Columns: lorem ipsum
    """

    for ind, each in enumerate(trialNum['Value_1']):
        temp = np.array(Licks[int(each)]['LickDigi'].iloc[1:-1]) - np.array(Licks[int(each)]['LickDigi'].iloc[0:-2])
        temp = np.append(np.append(0, temp), 0)
        Licks[int(each)]['Stamps'] = temp
        #Licks[int(each)]['Stamps'] = Licks[int(each)]['LickTime'][Licks[int(each)]['LickDigi'] == 1]

    return Licks

def countLicks(trialNum, Licks, bins):
    """
    Parameters
    ----------
    trialNum: pandas data frame
        Data frame that contains the valid trial numbers.

    Licks: pandas data frame
        lorem ipsum.

    Returns
    -------
    Licks: pandas data frame
        lorem ipsum.
        Columns: lorem ipsum
    """

    bins = bins*1000
    lickCounts = pd.DataFrame()
    for ind, each in enumerate(trialNum['Value_1']):
        for bin in bins:
            licks = Licks[int(each)].iloc[bin:bin+1]
            tempCount = np.array(licks['LickTime'][lick['Stamps'] == 1])
            #tempCount = np.array(Licks[int(each)]['LickTime'][Licks[int(each)]['Stamps'] == 1])
            print len(tempCount)
            lickCounts[int(each)] = len(tempCount)

    return lickCounts

def getPokes(trialNum, Trials_list):
    """
    Parameters
    ----------
    trialNum: pandas data frame
        Data frame that contains the valid trial numbers.

    Trials_list: dict
        Dict that contains sorted trial data.

    Returns
    -------
    Licks: pandas data frame
        Data frame that contains the timestamps of start and end for each poke.
        Columns: PokeStart, PokeEnd
    """

    Pokes = {}
    for ind, each in enumerate(trialNum['Value_1']):
        poke_start = pd.DataFrame({'PokeStart' : np.array(Trials_list[int(each)][Trials_list[int(each)]['Event'] == 'Poke_Start']['Value_1'])})
        poke_end = pd.DataFrame({'PokeEnd' : np.array(Trials_list[int(each)][Trials_list[int(each)]['Event'] == 'Poke_End']['Value_1'])})
        Pokes[int(each)] = pd.concat([poke_start, poke_end], axis= 1)

    return Pokes

def plotLicks(trialNum, Licks):
    """
    """

    Licks
    for ind, each in enumerate(trialNum['Value_1']):
        lick_start = Licks[10]['LickTime'][Licks[10]['Stamps'] == 1]
        lick_end = Licks[10]['LickTime'][Licks[10]['Stamps'] == -1]

        #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 3), facecolor='w', dpi= 150)
        for lick_ind in Licks[int(each)].index:
            pass
            #if Licks[int(each)]['']


if __name__ == "__main__":
    #filenames = chooseFile()
    fname = "C:\Users\hakan\Documents\git_repos\MousyBox\\7792\\7792_Day09.csv"
    [data, trialNum, Trials_list] = loadData(fname)
    Licks = getLicks(trialNum, Trials_list, th= 50)
    Licks = findLicks(trialNum, Licks)
    lickCounts = countLicks(trialNum, Licks, [0, 5, 10, 15])

    print lickCounts

    print(Licks[10].head(5))

    for lick in Licks[10].index:
        if Licks[10]['Stamps'].iloc[lick] == 1:
<<<<<<< HEAD
            print Licks[10]['LickTime'].iloc[lick], Licks[10]['Stamps'].iloc[lick]
        elif Licks[10]['Stamps'].iloc[lick] == -1:
            print Licks[10]['LickTime'].iloc[lick], Licks[10]['Stamps'].iloc[lick]
=======
            pass
            #print Licks[10]['Stamps'].iloc[lick]
        elif Licks[10]['Stamps'].iloc[lick] == -1:
            pass
            #print Licks[10]['Stamps'].iloc[lick]
>>>>>>> b0506dd5e896c2bde5da753bcbebbf2d771162f4

    #plotLicks(trialNum, Licks)

    #print Licks[10].iloc[3970:4000]
    ##print Licks[10]['LickTime'][Licks[10]['Stamps'] == 1]
    ##print Licks[10]['LickTime'][Licks[10]['Stamps'] == -1]
    #Licks[int(each)]['Stamps'] = Licks[int(each)]['LickTime'][Licks[int(each)]['LickDigi'] == 1]

    #plt.scatter(Licks[10]['LickTime'][Licks[10]['Stamps'] == 1], Licks[10]['LickTime'][Licks[10]['Stamps'] == -1])
    #plt.show()

    #a=np.array(Licks[10]['LickDigi'].iloc[0:-2])
    #b=np.array(Licks[10]['LickDigi'].iloc[1:-1])
    #print a+b

    #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 3), facecolor='w', dpi= 150)
    #ax.plot(Licks[10].LickDigi*400-20)
    #ax.plot(LickStamps[10])
    #print LickStamps[10]['Gaussed'].iloc[0]
    #for row in LickEnd[10].index:
        #ax.scatter(row, LickStamps[10]['Gaussed'].loc[row])
    #ax.set_y#lim([-30, 100])
    #plt.show()
