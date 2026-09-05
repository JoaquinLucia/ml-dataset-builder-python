"""
Módulo de la Interfaz Gráfica (Vista).
Se encarga de dibujar la ventana, capturar los datos del usuario
y enviarlos al controlador, cumpliendo con el patrón MVC.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class VistaApp:
    """
    Clase principal de la interfaz gráfica de usuario construida con Tkinter.
    """

    def __init__(self, ventana_principal, controlador):
        """
        Constructor de la Vista. Configura la ventana y dibuja los elementos.

        :param ventana_principal: Instancia raíz de Tkinter (tk.Tk()).
        :type ventana_principal: tk.Tk
        :param controlador: Instancia del Controlador para enviar/recibir datos.
        :type controlador: Controlador
        """
        self.ventana = ventana_principal
        self.controlador = controlador
        
        self.ventana.title("Sistema ABMC — Gestión de Mercado Automotor")
        self.ventana.geometry("900x650")
        self.ventana.config(padx=20, pady=10)

        # --- Título Principal ---
        ttk.Label(self.ventana, text="Ingreso de Datos al Dataset", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # --- Variables de Tkinter ---
        self.var_titulo = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_marca = tk.StringVar()
        self.var_modelo = tk.StringVar()
        self.var_anio = tk.StringVar()
        self.var_km = tk.StringVar()
        self.var_traccion = tk.StringVar(value="Trasera")
        self.var_precio = tk.StringVar()
        self.var_cilindrada = tk.StringVar()
        self.var_valvulas = tk.StringVar()

        # --- Creación del Formulario ---
        self.crear_campo("ID Único (Ej: PEUGEOT206XS):", self.var_titulo, 1)
        self.crear_campo("Descripción (Condiciones del auto, detalles etc):", self.var_desc, 2)
        self.crear_campo("Marca:", self.var_marca, 3)
        self.crear_campo("Modelo:", self.var_modelo, 4)
        self.crear_campo("Año (Sin puntos, ej 2015):", self.var_anio, 5)
        self.crear_campo("Kilometraje (Sin puntos, ej 100000):", self.var_km, 6)
        
        ttk.Label(self.ventana, text="Tracción:").grid(row=7, column=0, sticky="w", pady=5)
        combo_traccion = ttk.Combobox(self.ventana, textvariable=self.var_traccion, values=["Delantera", "Trasera", "Integral"], state="readonly")
        combo_traccion.grid(row=7, column=1, sticky="ew", pady=5)

        self.crear_campo("Precio ($USD):", self.var_precio, 8)
        self.crear_campo("Cilindrada (Ej: 1.6):", self.var_cilindrada, 9)
        self.crear_campo("Válvulas (Ej: 16):", self.var_valvulas, 10)

        # --- Botones del CRUD ---
        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row=11, column=0, columnspan=2, pady=15)

        ttk.Button(frame_botones, text="Guardar (Alta)", command=self.enviar_datos).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botones, text="Modificar", command=self.modificar_datos).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botones, text="Borrar (Baja)", command=self.borrar_datos).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botones, text="Limpiar Campos", command=self.limpiar_campos).pack(side=tk.LEFT, padx=10)

        #Treeview
        self.tree = ttk.Treeview(self.ventana, columns=("ID", "Titulo", "Marca", "Modelo", "Año", "KM", "Precio"), show='headings', height=10)
        
        self.tree.heading("ID", text="ID BD")
        self.tree.heading("Titulo", text="Código (ID Único)")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Año", text="Año")
        self.tree.heading("KM", text="KM")
        self.tree.heading("Precio", text="Precio (USD)")
        
        self.tree.column("ID", width=50)
        self.tree.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
        
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.actualizar_tabla()

    def crear_campo(self, texto_label, variable, fila):
        """
        Método auxiliar para generar etiquetas y campos de entrada

        :param texto_label: Texto que se mostrará al lado del campo.
        :type texto_label: str
        :param variable: Variable de Tkinter asociada al campo.
        :type variable: tk.StringVar
        :param fila: Fila del grid donde se posicionará.
        :type fila: int
        """
        ttk.Label(self.ventana, text=texto_label).grid(row=fila, column=0, sticky="w", pady=5)
        ttk.Entry(self.ventana, textvariable=variable).grid(row=fila, column=1, sticky="ew", pady=5)

    def obtener_datos_formulario(self):
        """
        Extrae y convierte los datos capturados en las variables de Tkinter.

        :return: Tupla con los datos convertidos a su tipo correspondiente, o None si hay error.
        :rtype: tuple or None
        """
        # 1. Frenamos el proceso si los campos de texto clave están vacíos
        if not self.var_titulo.get().strip() or not self.var_marca.get().strip() or not self.var_modelo.get().strip():
            messagebox.showerror("Error", "Faltan datos. El código, marca y modelo son obligatorios.")
            return None

        # 2. Si hay texto, intentamos convertir los números
        try:
            return (
                self.var_titulo.get(),
                self.var_desc.get(),
                self.var_marca.get(),
                self.var_modelo.get(),
                int(self.var_anio.get()),
                int(self.var_km.get()),
                self.var_traccion.get(),
                float(self.var_precio.get()),
                float(self.var_cilindrada.get()),
                int(self.var_valvulas.get())
            )
        except ValueError:
            messagebox.showerror("Error de Formato", "Año, Kilometraje, Precio, Cilindrada y Válvulas deben ser números válidos.")
            return None

    def enviar_datos(self):
        """Lógica para el botón Guardar (Alta de registro)."""
        datos = self.obtener_datos_formulario()
        if datos:
            respuesta = self.controlador.procesar_alta(*datos)
            self.manejar_respuesta(respuesta)

    def modificar_datos(self):
        """Lógica para el botón Modificar (Actualización de registro)."""
        datos = self.obtener_datos_formulario()
        if datos:
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de modificar el registro '{datos[0]}'?"):
                respuesta = self.controlador.procesar_modificacion(*datos)
                self.manejar_respuesta(respuesta)

    def borrar_datos(self):
        """Lógica para el botón Borrar (Baja de registro)."""
        titulo = self.var_titulo.get()
        if not titulo:
            messagebox.showwarning("Advertencia", "Por favor, ingresá o seleccioná el Código (ID Único) que querés borrar.")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de ELIMINAR el registro '{titulo}'?"):
            respuesta = self.controlador.procesar_baja(titulo)
            self.manejar_respuesta(respuesta)

    def manejar_respuesta(self, respuesta):
        """
        Muestra un cuadro de diálogo basado en la respuesta del controlador.

        :param respuesta: Diccionario con el estado ('exito' o 'error') y el mensaje.
        :type respuesta: dict
        """
        if respuesta["estado"] in ["exito", "agregado"]:
            messagebox.showinfo("Éxito", respuesta["mensaje"])
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", respuesta["mensaje"])

    def actualizar_tabla(self):
        """Pide los datos frescos al controlador y redibuja las filas en el Treeview."""
        for fila in self.tree.get_children():
            self.tree.delete(fila)
            
        respuesta = self.controlador.procesar_consulta()
        
        if respuesta["estado"] == "exito":
            for fila in respuesta["datos"]:
                # Mostramos ID, Titulo, Marca, Modelo, Año, KM y Precio
                valores_mostrar = (fila[0], fila[1], fila[3], fila[4], fila[5], fila[6], fila[8])
                self.tree.insert("", tk.END, values=valores_mostrar)

    def seleccionar_fila(self, event):
        """
        Evento que se dispara al hacer clic en una fila del Treeview.
        Carga el Código (ID Único) en el formulario para facilitar su edición o borrado.
        """
        item_seleccionado = self.tree.focus()
        if item_seleccionado:
            valores = self.tree.item(item_seleccionado, 'values')
            if valores:
                self.var_titulo.set(valores[1])
                
    def limpiar_campos(self):
        """Vacía todos los campos de texto del formulario y resetea opciones."""
        self.var_titulo.set("")
        self.var_desc.set("")
        self.var_marca.set("")
        self.var_modelo.set("")
        self.var_anio.set("")
        self.var_km.set("")
        self.var_precio.set("")
        self.var_cilindrada.set("")
        self.var_valvulas.set("")
        self.var_traccion.set("Trasera")