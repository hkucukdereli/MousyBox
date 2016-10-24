from Tkinter import Tk
from tkFileDialog import askopenfilename,askdirectory

root = Tk()
root.withdraw() # keep the root window from appearing
filenames = askopenfilename(parent=root, filetypes = (("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")), multiple=True) # show an "Open" dialog box and return the path to the selected file
print(filenames)
