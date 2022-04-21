from tkinter import *

def write_a_slogan():
    print("COMMAND")
    
def app():
    ws = Tk()
    ws.title("Python Guides")
    ws.geometry("200x200")
    pawin = PanedWindow(orient ='vertical')
    frame = Frame(ws)
    frame.pack()

    but = Button(frame, 
                    text="Exit", 
                    fg="blue",
                    command=quit)
    but.pack(side=LEFT)
    slog = Button(frame,
                    text="command",
                    fg="red",
                    command=write_a_slogan)
    slog.pack(side=LEFT)
    ws.mainloop()

if __name__ == "__main__":
    app()