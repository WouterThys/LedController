from Tkinter import *

from Manager import Manager


def main():
    root = Tk()
    Manager(root)
    root.configure(bg="White")
    root.mainloop()

if __name__ == '__main__':
    main()
