from multiprocessing import Process
from tkinter import *
import tcp2tobii
  
def f1():
    tcp = tcp2tobii()
    tcp.run()
  
def f2():
    print(2)
  
def main():
    p1 = Process(target=f1)
    p1.start()
    p2 = Process(target=f2)
    p2.start()
    p1.join()
    p2.join()
  
if __name__ == '__main__':
    window = Tk()
    main()
    window.mainloop()