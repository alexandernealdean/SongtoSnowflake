import os
import subprocess
import turtle
import canvasvg
import tkinter
from tkinter import filedialog
from tkinter import *

####FILE SELECT BUTTON####
def fileSelect():
      inName = filedialog.askopenfilename()
      screen.withdraw()
      fileChooser(inName)
      screen.deiconify()
      var.set(1)

####DRAW FUNC####
def draw(f, file, ct):
    ang = float(360)
    followline = 0.0
    for x in range(5):  # initialize turtle objects
        f[x].hideturtle()
        f[x].pendown()
        f[x].hideturtle()
        f[x].pen(pencolor="light blue", pensize=1)
        f[x].speed(0)

    with open(file, "r") as doc:
        for line in doc:
            if line == "inf":
                continue
            freq = float(line) - followline  # frequencies for next angle measurements
            for x in range(5):
                f[x].left(freq * ang)
            for x in range(5):
                f[x].forward(5)  # each frequency is given one pixel of output
            turtle.update()
            followline = float(line)

    doc.close()
    canvasvg.saveall("canvas.svg", turtle.getcanvas(), tounicode=None)

####EXTRA MAIN CODE####
def drawSetup(readin):
    #readin = input("File name?\n")
    turtle.bgcolor("white")

    turtle.setup(900, 900)
    
    deg = 72

    f = []
    for x in range(5):
        f.append(turtle.Turtle())
        if x != 0:
            f[x].left(deg * x)

    fi = []
    canvasvg.warnings(canvasvg.NONE)
    draw(f, readin, 1)
    
    turtle.exitonclick()
    turtle.done()


####FILE SELECTION BACK-END####
def fileChooser(inName):

    command = "ffmpeg -i " + inName + " -filter:a \"astats=metadata=1:reset=1,ametadata=mode=print:key=lavfi.astats.Overall.RMS_level:file=stats.txt\" -f null -"#command to convert mp3 to stats.txt
    os.system(command)

    f2= open("C:\\Users\\Alex\\source\\repos\\PythonApplication1\\PythonApplication1\\Frequencies.txt","w+")#declare output file
    word = "inf"#variable to remove "inf" values

    with open("stats.txt", "r+") as f:
        for line in f:
            if not word in f.readline():
                f.readline()# skip to next line
                f.read(32) # read 32 chars from first line
                f2.write(f.readline())#write to output file
    drawSetup("C:\\Users\\Alex\\source\\repos\\PythonApplication1\\PythonApplication1\\Frequencies.txt")

####MAIN####
screen = Tk()
var = tkinter.IntVar()
screen.geometry("600x100")
screen.title("MP3 to Snowflake") 


heading = Label(text = "Choose an mp3 to convert to snowflake:", fg = "blue",font = ("Arial", "20"))
btnChooseFile= Button(screen,padx = 25, pady = 8, text="Select File", fg = "blue", command=fileSelect)
heading.pack()
btnChooseFile.pack()

btnChooseFile.wait_variable(var)

