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
    os.chdir("C:\Users\hakan\Dropbox\\for Hakan\Arduino\Cued Reward Scripts\mousybox\data")

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
    #fname = "C:\Users\hakan\Dropbox\\for Hakan\Arduino\Cued Reward Scripts\mousybox\data\8351@\8351_Day21_Reward10s.csv"
    fname = chooseFile()[0]
    [data, trialNum, Trials_list] = loadData(fname)
    Licks = getLicks(trialNum, Trials_list, th= 50)
    Licks = findLicks(trialNum, Licks)

    # temp modification to count the licks. only keeps the lick beginings
    for ind in np.arange(1, 41):
        Licks[ind].ix[Licks[ind].Stamps == -1, 'Stamps'] = 0

    Pokes = getPokes(trialNum, Trials_list)

    bins = np.arange(5000, 31000, 1000)
    binnedDF = pd.DataFrame(Licks[1].groupby(pd.cut(Licks[1].LickTime, bins)).sum().Stamps)
    for ind_ in np.arange(2, 41):
        groups = Licks[ind_].groupby(pd.cut(Licks[ind_].LickTime, bins))
        tempDF = pd.DataFrame(groups.sum().Stamps)
        binnedDF = binnedDF + tempDF
    # save the binned data to a csv
    binnedDF.to_csv(fname[:-4] + "_BinnedLicksSum.csv")
