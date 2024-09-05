from tester.interface.testerGUI import TesterGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = TesterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()