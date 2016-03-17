##Columbia University Energy and Tribology Lab
##CETR Tribometer Data Plotter Program
##This program makes time-series plots of friction data from the CETR
##reciprocating tribometer. It does not trust the CETR friction
##coefficient calculation; instead, it calculates its own CoF.
##By Aleks Navratil
##Created 7 March 2013
##Updated 23 April 2013
print "Welcome to the Columbia ET+L Lab CETR Time Series Plotter\nNow Loading Plotting Libraries"

import numpy
import matplotlib.pyplot as plt
import pandas as pd
import os
import traceback
import Tkinter, tkFileDialog

def User_Chooses_Skiprows():
        User_Skiprow_Choice=18
        print "This program is presently configured to skip",User_Skiprow_Choice,"rows"
        print "This works well if you only textified step 2 of data on the CETR computer."
        print "If you want to skip some other number of rows, type it now. Otherwise, press enter."
        tempvar=raw_input("")
        if tempvar=="":
                print "OK. Skipping 18 rows."
                return User_Skiprow_Choice
        try:
                User_Skiprow_Choice=int(tempvar)
                return User_Skiprow_Choice
        except Exception:
                print "\nThat wasn't a number. Try again.\n"
                return User_Chooses_Skiprows()
                        
def Ask_If_Dario_Mode():
        tempvar=raw_input("\nDo you want to run in Dario mode? (Dario mode makes you choose the range of times you want plotted for each .csv file). Type 'y' or 'n'.\n")
        try:
                if tempvar=="y":
                        print "Note that this program calculates averages over the whole datafile, not just the window you choose."
                        return 1
                elif tempvar=="n":
                        return 0
                else:
                        Ask_If_Dario_Mode()
        except Exception:
                print "Error. Something went wrong. Not running in Dario mode.\n"
                return 0

def Load_Values(name_of_file_to_plot,directory_containing_file_to_plot):
        global Time_Values
        global CETR_Calculated_CoF
        global Manually_Calculated_CoF
        data = numpy.loadtxt(directory_containing_file_to_plot+os.path.sep+name_of_file_to_plot, delimiter = ",", skiprows = number_of_rows_to_skip, usecols = (0,1,8,10))
        Time_Values = data[:,2]
        CETR_Calculated_CoF = data[:,3]
        Manually_Calculated_CoF = abs(data[:,0]/data[:,1])


def Create_Plot(name_of_file_to_plot,directory_containing_file_to_plot):
        ##Do a few simple calculations that will get printed on the plot
        Rolling_Mean_of_Manual_CoF = pd.stats.moments.rolling_mean(Manually_Calculated_CoF,100)
        Average_Manually_Calculated_CoF = float(numpy.mean(Manually_Calculated_CoF))
        print "Average Manual CoF is",round(Average_Manually_Calculated_CoF,3),"\n"
        ##Start plotting commands here
        plt.plot(Time_Values,Manually_Calculated_CoF, label='Manual CoF')
        plt.plot(Time_Values,CETR_Calculated_CoF, label='CETR CoF')
        plt.plot(Time_Values,Rolling_Mean_of_Manual_CoF, label='Rolling Mean CoF')
        plt.xlim(left_limit,right_limit)##this is experimental.
        plt.grid()##Make gridlines
        plt.title(name_of_file_to_plot[0:-4])
        plt.xlabel("Time (Seconds)")
        plt.ylabel("CoF (Dimensionless)")
        plt.legend(loc='best')
        plt.figtext(0,.01, "Mean manual CoF is "+str(Average_Manually_Calculated_CoF))
##        plt.figure(figsize=(6,8), dpi=400)##also you can use (figsize=(8, 6), dpi=80) etc. figsize =(8,6) is in hundreds of pixels. 
        plt.savefig(directory_containing_file_to_plot+os.path.sep+name_of_file_to_plot[0:-4]+".png")
##        plt.clf()
        plt.close()

def User_Chooses_Plot_Limit(which_side):
        try:
                tempvar=round(abs(int(raw_input("\nWhat do you want the "+which_side+" time limit of your plot to be? Type a number in seconds and press enter.\n"))))
                return tempvar
        except ValueError:
                print "\nYou didn't type a number. Try again.\n"
                User_Chooses_Plot_Limit(which_side)

print "\nLibraries loaded. \nPress ctrl-c at any time to quit."
Directory_Caution_Message = "This program will find and plot all textified CETR .csv files in any directory you want. It recursively searches subdirectories.\n \n"
print Directory_Caution_Message
number_of_rows_to_skip=User_Chooses_Skiprows()                     
dario_mode=Ask_If_Dario_Mode()     

print "Use the popup window to pick a directory.\n"
root = Tkinter.Tk()
root.withdraw()
Directory_chosen_by_user = tkFileDialog.askdirectory(parent=root,initialdir="/media/AVN2109/CETR/Wear Evolution Tests",title='Pick a folder. All .csv files in the directory you choose (including subfolders) will be plotted.')

plot_counter=0
for directory,list_of_subdirectories,list_of_files in os.walk(Directory_chosen_by_user):
        for File in list_of_files:
                if File.endswith('.csv'):
                        print "\n\nNow plotting",directory+os.path.sep+File+'\n'
                        try:
                                Load_Values(File,directory)##get the data from file and examine it.
                                if  dario_mode==0:
                                        left_limit=0##The left and right limits control the time range of the data that is plotted. It defaults to the maximum available.
                                        right_limit=round(int((Time_Values[-1])))
                                elif dario_mode==1:
                                        left_limit=User_Chooses_Plot_Limit("left")
                                        right_limit=User_Chooses_Plot_Limit("right")
                                        if left_limit > right_limit:##Build in a little error checking to deter pranksters
                                                tmp = left_limit
                                                left_limit=right_limit
                                                right_limit=tmp
                                        if left_limit==right_limit:
                                                left_limit=0
                                                right_limit=round(int((Time_Values[-1])))                                                
                                Create_Plot(File,directory)
                                plot_counter+=1
                        except ValueError:
                                print "ERROR!\n\n"
                                print traceback.format_exc()
                                pass
                        except IndexError:
                                print "Error!\nThis probably means that you're not skipping enough rows or that you already ran the Excel plotting macro on it."
                                print "Fix this by re-copying the virgin datafile from the CETR machine and using that virgin file instead of the copy that Excel broke.\n\n"
                                print traceback.format_exc()
                                pass
                        except Exception:
                                print "Error! Something mysterious went wrong. Sorry. Skipping this file and trying to plot the next one.\n\n"
                                print traceback.format_exc()
                                pass
print "Plotting Finished.\n"
print "Plotted",plot_counter,"files"


