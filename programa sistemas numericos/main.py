import tkinter as tk
from gui import ConverterApp

def main():
    """
    Función de entrada principal que inicializa Tkinter 
    y ejecuta el bucle de la aplicación.
    """
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
