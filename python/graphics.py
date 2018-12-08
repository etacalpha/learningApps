import tkinter


def parabola(page, size):
    for x in range(size):
        y = x * x / size
        plot(page, x, y)
        plot(page, -x, y)
        plot(page, x, -y)
        plot(page, -x, -y)


def circle(page, radius, g, h, color="red"):
    page.create_oval(g + radius,
                     h + radius,
                     g - radius,
                     h - radius,
                     outline=color,
                     width=2)


def drawAxes(page):
    page.update()
    x_origin = page.winfo_width() / 2
    y_origin = page.winfo_height() / 2
    page.configure(scrollregion=(-x_origin, -y_origin, x_origin, y_origin))
    # page.create_line(-x_origin, 0, x_origin, 0, fill="white")
    # page.create_line(0, y_origin, 0, -y_origin, fill="white")


def plot(page, x, y):
    page.create_line(x, -y, x + 1, -y + 1, fill="red")


mainWindow = tkinter.Tk()

mainWindow.title("Parabola")
mainWindow.geometry("640x480")

canvas = tkinter.Canvas(mainWindow, width=640, height=480)
canvas.grid(row=0, column=0)

drawAxes(canvas)

parabola(canvas, 100)
parabola(canvas, 200)

circle(canvas, 100, 100, 100, "purple")
circle(canvas, 100, 100, -100, "green")
circle(canvas, 100, -100, 100, "yellow")
circle(canvas, 100, -100, -100, "blue")
circle(canvas, 10, 30, 30, "orange")
circle(canvas, 10, 30, -30, "pink")
circle(canvas, 10, -30, 30, "white")
circle(canvas, 10, -30, -30, "brown")
circle(canvas, 30, 3, 0)

mainWindow.mainloop()
