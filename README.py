# Function to install missing Packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "venv", package , '--user'])
# Trying to import all Pkgs required and install them if are not present in the local env
try:
    # Libraries Needed by the script
    import tkinter as tk
    from tkinter import ttk
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfile
    from tkinter import filedialog
    import pandas as pd
    from pathlib import Path
    import os
    from sas7bdat import SAS7BDAT
    import gc

    import warnings
    warnings.filterwarnings('ignore')
except:
    # Creating a list of required packages
    import requests   
    r = requests.get('https://raw.githubusercontent.com/DavideUCB/Library/main/requirement.txt')
    data=r.text
    pkgs_req = data.split("\n")# creating a list removing last empty string generated by last \n
    if '' in pkgs_req:
        pkgs_req.pop()
    import pkg_resources
    temp = [p for p in pkg_resources.working_set]# list with pkgs and path in the local env
    pkgs_installed=[]
    [pkgs_installed.append(str(p)) for p in temp]# Removing path 
    pkgs_installed=[r.replace(' ','==') for r in pkgs_installed]# #Replace empy space with '==' to match our check list
    import subprocess
    import sys
    for p in pkgs_req:
        if p in pkgs_installed:
            print(f"{p} already installed")
        elif p not in pkgs_installed:
            print(f"{p} is not installed in your env please wait for the installation")
            install(p)
    # Reimporting all libraries 
    import tkinter as tk
    from tkinter import ttk
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfile
    from tkinter import filedialog
    import pandas as pd
    from pathlib import Path
    import os
    from sas7bdat import SAS7BDAT
    import gc

    import warnings
    warnings.filterwarnings('ignore')

# functions for buttons and labels
def sas_location():
    global sas_location
    global label_old
    sas_location = askopenfilename(filetypes = (("sas7bdat files","*.sas7bdat"),("xpt files","*.xpt"),("all files","*.*")))
    if sas_location:     
        label_old=Label(gui_frame,text='File Selected: '+ os.path.basename(sas_location), fg='dark green', 
                        font=('Calibri', 10, 'bold'))
        label_old.pack()
            
def saving_location():
    global excel_location
    global label_save
    excel_location= asksaveasfile(mode='w', defaultextension=".xlsx")
    excel_location=excel_location.name
    if excel_location:
        label_save = Label(gui_frame, text= 'Output will be saved as: '+ os.path.basename(excel_location), fg='dark green', 
                           font=('Calibri', 10, 'bold'))
        label_save.pack()
    else:
        label_save = Label(gui_frame, text= 'Saving Location not provided!', fg='#5e366e', font=('Calibri', 10, 'bold'))
        label_save.pack()    
        
# functions for buttons and labels
def sas_Dir_location():
    global sas_dir_location
    global label_old
    sas_dir_location = filedialog.askdirectory()
    if sas_dir_location:     
        label_old=Label(gui_frame,text='Folder Selected: '+ os.path.basename(sas_dir_location), fg='dark green', 
                        font=('Calibri', 10, 'bold'))
        label_old.pack()

def saving_Dir_location():
    global excel_dir_location
    global label_save
    excel_dir_location= filedialog.askdirectory()

    if excel_dir_location:
        label_save = Label(gui_frame, text= 'Output will be saved as: '+ os.path.basename(excel_dir_location), fg='dark green', 
                           font=('Calibri', 10, 'bold'))
        label_save.pack()
    else:
        label_save = Label(gui_frame, text= 'Saving Location not provided!', fg='#5e366e', font=('Calibri', 10, 'bold'))
        label_save.pack()    
             
def convert_sas_excel():
    global label_progress
    global label_done
    
    label_progress = Label(gui_frame, text= 'Work in Progress ...', fg='#354b96', font=('Calibri', 10, 'bold'))
    label_progress.pack()

    with SAS7BDAT(sas_location) as file:
        df_sas = file.to_data_frame()
        
    df_sas.to_excel(excel_location, index = False)
    
    label_done = Label(gui_frame, text= 'Conversion is Done Successfully !', fg='#354b96', font=('Calibri', 11, 'bold'))
    label_done.pack() 


def convert_multiple_sas_excel():
    global label_progress
    global label_done

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(sas_dir_location):
        for file in f:
            if '.sas7bdat' in file:
                files.append(os.path.join(r, file))
    
    for f in files:
        with SAS7BDAT(f) as file:
            df_sas = file.to_data_frame()
            sav_fil_path = f.replace('.sas7bdat','.xlsx')
            
            # Clear the memory
            gc.collect()
            
            df_sas.to_excel(excel_dir_location+'/'+os.path.basename(sav_fil_path), index=False)
            
            label_progress = Label(gui_frame, text= f, fg='#354b96', font=('Calibri', 10, 'bold'))
            label_progress.pack()
            
    label_done = Label(gui_frame, text= 'Conversion is Done Successfully !', fg='#354b96', font=('Calibri', 11, 'bold'))
    label_done.pack() 

    
def convert_xpt_excel():
    global label_progress
    global label_done
    label_progress = Label(gui_frame, text= 'Work in Progress ...', fg='#354b96', font=('Calibri', 10, 'bold'))
    label_progress.pack()

    df_sas = pd.read_sas(sas_location,encoding="utf-8") #
    df_sas.to_excel(excel_location,index = False)
     
    label_done = Label(gui_frame, text= 'Conversion is Done Successfully !', fg='#354b96', font=('Calibri', 11, 'bold'))
    label_done.pack()     

def convert_multiple_xpt_excel():
    global label_progress
    global label_done
    
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(sas_dir_location):
        for file in f:
            if '.xpt' in file:
                files.append(file)

    for domain in files:
        print(domain)
        label_progress = Label(gui_frame, text= sas_dir_location +'/'+ domain, fg='#354b96', font=('Calibri', 10, 'bold'))
        label_progress.pack()
        df_sas = pd.read_sas(sas_dir_location +'/'+ domain ,encoding="utf-8")
        domain = domain.replace('.xpt','')
        df_sas.to_excel(excel_dir_location+'/'+ domain +'.xlsx',index = False)
        
     
    label_done = Label(gui_frame, text= 'Conversion is Done Successfully !', fg='#5e366e', font=('Calibri', 12, 'bold'))
    label_done.pack()     

def restart_program():
    global label_reset
    label_reset=Label(gui_frame,text="Please provide input/output location again",fg="#5e366e", font=('Calibri', 10, 'bold'))
    label_reset.pack()
    if label_old or label_save or label_progress or label_done:
        label_old.destroy()
        label_save.destroy()
        label_progress.destroy()
        label_done.destroy() 
          
###########################################################################################################

convertGUI = tk.Tk()
convertGUI.title("SAS Files Conversion to Excel Application")
convertGUI.geometry("680x280")  

style = ttk.Style(convertGUI)
style.configure('lefttab.TNotebook', tabposition='wn',background= "#354b96")


gui_frame=Frame(convertGUI)        

###########################################################################################################

# Tabs    
tab_parent = ttk.Notebook(convertGUI, style='lefttab.TNotebook')
tab1 = tk.Frame(tab_parent)
tab2 = tk.Frame(tab_parent)
tab3 = tk.Frame(tab_parent)
tab4 = tk.Frame(tab_parent)
tab5 = tk.Frame(tab_parent)

tab_parent.add(tab1, text="Info")
tab_parent.add(tab2, text="One SAS7BDAT to Excel")
tab_parent.add(tab3, text="Multiple SAS7BDAT to Excel")
tab_parent.add(tab4, text="One XPT to Excel")
tab_parent.add(tab5, text="Multiple XPT to Excel")

tab_parent.grid(row=0, column=0, sticky="wn")

###########################################################################################################

# buttons Tab1
firstLabelTabOne = tk.Label(tab1, 
            text="Using this App you can Convert SAS files (.sas7bdat and .xpt) to excel files with one click.\nYou can convert one SAS file to one Excel file or Multiple SAS files at a time.\nIn both Cases you need to select either the SAS file or the folder containing multiple files.", 
            font=('Calibri', 10))

firstLabelTabOne.grid(row=0, column=0, padx=15, pady=30)

# buttons Tab2
buttonSelectTab2 = tk.Button(tab2,text='Select .Sas7bdat File', width=25, font=('Calibri', 11),command=sas_location)
buttonSaveTab2 = tk.Button(tab2,text='Select Saving Location', width=25, font=('Calibri', 11),command=saving_location)
buttonRunTab2 = tk.Button(tab2,text="Run Program",fg="#bc2046", width=25, font=('Calibri', 11), command = convert_sas_excel)
buttonResetTab2 = tk.Button(tab2,text="Reset", width=25, font=('Calibri', 11), command=restart_program)

buttonSelectTab2.grid(row=0, column=0, padx=30, pady=30)
buttonSaveTab2.grid(row=0, column=1, padx=15, pady=15)
buttonRunTab2.grid(row=1, column=0, padx=15, pady=15)
buttonResetTab2.grid(row=1, column=1, padx=15, pady=15)

# buttons Tab3
buttonSelectTab3 = tk.Button(tab3,text='Select .Sas7bdat Folder', width=25, font=('Calibri', 11),command=sas_Dir_location)
buttonSaveTab3 = tk.Button(tab3,text='Select Saving Location', width=25, font=('Calibri', 11),command=saving_Dir_location)
buttonRunTab3 = tk.Button(tab3,text="Run Program", fg="#bc2046", width=25, font=('Calibri', 11),command = convert_multiple_sas_excel)
buttonResetTab3 = tk.Button(tab3,text="Reset", width=25, font=('Calibri', 11), command=restart_program)

buttonSelectTab3.grid(row=0, column=0, padx=30, pady=30)
buttonSaveTab3.grid(row=0, column=1, padx=15, pady=15)
buttonRunTab3.grid(row=1, column=0, padx=15, pady=15)
buttonResetTab3.grid(row=1, column=1, padx=15, pady=15)

# buttons Tab4
buttonSelectTab4 = tk.Button(tab4,text='Select .Xpt File', width=25, font=('Calibri', 11),command=sas_location)
buttonSaveTab4 = tk.Button(tab4,text='Select Saving Location', width=25, font=('Calibri', 11),command=saving_location)
buttonRunTab4 = tk.Button(tab4,text="Run Program", fg="#bc2046", width=25, font=('Calibri', 11),command = convert_xpt_excel)
buttonResetTab4 = tk.Button(tab4,text="Reset", width=25, font=('Calibri', 11), command=restart_program)

buttonSelectTab4.grid(row=0, column=0, padx=30, pady=30)
buttonSaveTab4.grid(row=0, column=1, padx=15, pady=15)
buttonRunTab4.grid(row=1, column=0, padx=15, pady=15)
buttonResetTab4.grid(row=1, column=1, padx=15, pady=15)

# buttons Tab5
buttonSelectTab5 = tk.Button(tab5,text='Select .Xpt Folder', width=25, font=('Calibri', 11),command=sas_Dir_location)
buttonSaveTab5 = tk.Button(tab5,text='Select Saving Location', width=25, font=('Calibri', 11),command=saving_Dir_location)
buttonRunTab5 = tk.Button(tab5,text="Run Program", fg="#bc2046", width=25, font=('Calibri', 11),command = convert_multiple_xpt_excel)
buttonResetTab5 = tk.Button(tab5,text="Reset", width=25, font=('Calibri', 11), command=restart_program)

buttonSelectTab5.grid(row=0, column=0, padx=30, pady=30)
buttonSaveTab5.grid(row=0, column=1, padx=15, pady=15)
buttonRunTab5.grid(row=1, column=0, padx=15, pady=15)
buttonResetTab5.grid(row=1, column=1, padx=15, pady=15)

###########################################################################################################

tab_parent.pack(expand=1, fill='both')

gui_frame.pack()

convertGUI.mainloop()
