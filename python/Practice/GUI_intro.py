import tkinter

# main Window = tkinter window factory object ( top window )
mainWindow = tkinter.Tk()

# Set name of window
mainWindow.title("Hello World")
# Set size of the window + from left + from top
mainWindow.geometry('900x700+500+150')

# adds label to main window with text 'Hello world'
label = tkinter.Label(mainWindow, text="Hello World!!")

# positions label at the top
# label.pack(side='top')
label.grid(row=0, column=0)

# create frames in the main window
frameLeft = tkinter.Frame(mainWindow)
frameRight = tkinter.Frame(mainWindow)

# position frames
# frameLeft.pack(side='left', anchor='n', fill=tkinter.Y, expand=False)
# frameRight.pack(side='right', anchor='n', fill=tkinter.Y, expand=True)
frameLeft.grid(row=1, column=1, sticky='ns')
frameRight.grid(row=1, column=2, sticky='new')  # Sticky acts like anchor

# create canvas in frameLeft
canvas = tkinter.Canvas(frameLeft, relief='raised', borderwidth=1)

# position canvas
# canvas.pack(side='left', anchor='n')
canvas.grid(row=1, column=0)

# crate buttons in frameRight
button1 = tkinter.Button(frameRight, text='button1')
button2 = tkinter.Button(frameRight, text='button2')
button3 = tkinter.Button(frameRight, text='button3')

# position buttons in frame
# button3.pack(side='top')
# button1.pack(side='top')
# button2.pack(side='top')
button3.grid(row=0, column=0)
button1.grid(row=1, column=0)
button2.grid(row=2, column=0, sticky='ew')

# configure columns
# main
mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=1)
mainWindow.columnconfigure(2, weight=1)

# frames
frameRight.columnconfigure(0, weight=1)

# configure frames
frameLeft.config(relief='sunken', borderwidth=1)
frameRight.config(relief='sunken', borderwidth=1)

# main method to run main window resolution
mainWindow.mainloop()
