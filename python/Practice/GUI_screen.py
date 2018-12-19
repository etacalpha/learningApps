import tkinter
import os


# ****************MAIN WINDOW SETUP**************
mainWindow = tkinter.Tk()
mainWindow.title("Grid Demo")
mainWindow.geometry('900x700+500+150')
mainWindow['padx'] = 20

mainWindow.columnconfigure(0, weight=100)
mainWindow.columnconfigure(1, weight=100)
mainWindow.columnconfigure(2, weight=1000)
mainWindow.columnconfigure(3, weight=600)
mainWindow.columnconfigure(4, weight=1000)
mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=10)
mainWindow.rowconfigure(2, weight=1)
mainWindow.rowconfigure(3, weight=3)
mainWindow.rowconfigure(4, weight=3)

# ***********SUB WINDOWS***************
# Label
label = tkinter.Label(mainWindow, text="Tkinter Grid Demo")
label.grid(row=0, column=0, columnspan=3)


# file list
fileList = tkinter.Listbox(mainWindow)
fileList.grid(row=1, column=0, sticky='nsew', rowspan=2)
fileList.config(border=2, relief='sunken')
for zone in os.listdir('/usr/bin'):
    fileList.insert(tkinter.END, zone)
# scroll bar
listScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=fileList.yview, background='white')
listScroll.grid(row=1, column=1, sticky='nsw', rowspan=2)
fileList['yscrollcommand'] = listScroll.set


# frame for the time spinners
timeFrame = tkinter.LabelFrame(mainWindow, text='Time')
timeFrame.grid(row=3, column=0, sticky='new')
# Time Labels
tkinter.LabelFrame(timeFrame, text=':').grid(row=0, column=1)
tkinter.LabelFrame(timeFrame, text=':').grid(row=0, column=3)
# Time Spinners
hourSpinner = tkinter.Spinbox(timeFrame, width=2, values=tuple(range(0, 24)))
minuteSpinner = tkinter.Spinbox(timeFrame, width=2, from_=0, to=59)
secondSpinner = tkinter.Spinbox(timeFrame, width=2, from_=0, to=59)
hourSpinner.grid(row=0, column=0)
minuteSpinner.grid(row=0, column=2)
secondSpinner.grid(row=0, column=4)
timeFrame['padx'] = 36

# frame for Date Spinners
dateFrame = tkinter.Frame(mainWindow)
dateFrame.grid(row=4, column=0, sticky='ew')
# Date Labels
dayLabel = tkinter.Label(dateFrame, text='Day')
monthLabel = tkinter.Label(dateFrame, text='Month')
yearLabel = tkinter.Label(dateFrame, text='Year')
dayLabel.grid(row=0, column=0, sticky='w')
monthLabel.grid(row=0, column=1, sticky='w')
yearLabel.grid(row=0, column=2, sticky='w')
# date Spinners
daySpin = tkinter.Spinbox(dateFrame, width=5, from_=1, to=31)
monthSpin = tkinter.Spinbox(dateFrame, width=5, values=("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))
yearSpin = tkinter.Spinbox(dateFrame, width=5, from_=2000, to=2099)
daySpin.grid(row=1, column=0)
monthSpin.grid(row=1, column=1)
yearSpin.grid(row=1, column=2)


# frame for radio buttons
optionFrame = tkinter.LabelFrame(mainWindow, text='File Details')
optionFrame.grid(row=1, column=2, sticky="ne")
# Radio Buttons
rbValue = tkinter.IntVar()
rbValue.set(1)
radio1 = tkinter.Radiobutton(optionFrame, text='File Name', value=1, variable=rbValue)
radio2 = tkinter.Radiobutton(optionFrame, text='Path', value=2, variable=rbValue)
radio3 = tkinter.Radiobutton(optionFrame, text='Time Stamp', value=3, variable=rbValue)
radio1.grid(row=0, column=0, sticky='w')
radio2.grid(row=1, column=0, sticky='w')
radio3.grid(row=2, column=0, sticky='w')


# Results
resultLabel = tkinter.Label(mainWindow, text='Result')
resultLabel.grid(row=2, column=2, sticky='nw')
result = tkinter.Entry(mainWindow)
result.grid(row=2, column=2, sticky='sw')

# Buttons
okButton = tkinter.Button(mainWindow, text='OK')
cancelButton = tkinter.Button(mainWindow, text='Cancel', command=mainWindow.destroy)
okButton.grid(row=4, column=3, sticky='e')
cancelButton.grid(row=4, column=4, sticky='w')


# *****************MAIN METHOD****************
mainWindow.mainloop()
