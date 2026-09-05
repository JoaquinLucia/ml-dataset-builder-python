"""
Módulo principal (Main).
Punto de entrada de la aplicación. Se encarga de inicializar
la interfaz gráfica y conectarla con el Controlador.
"""

import tkinter as tk
from controlador import Controlador
from vista import VistaApp


def iniciar_app():
    """
    Función principal que arranca la aplicación.
    Crea la ventana raíz de Tkinter, instancia el controlador,
    inicializa la vista pasándole el control y ejecuta el bucle principal.
    """
    root = tk.Tk()
    mi_controlador = Controlador()
    app = VistaApp(root, mi_controlador)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()  