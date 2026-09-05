"""
Módulo de conexión a la base de datos
Encargado de gestionar la conexión con SQLite3
"""

import sqlite3


class ConexionBD:
    """
    Clase para manejar la conexión a la base de datos SQLite3.

    :param base_datos: Nombre del archivo de la base de datos.
    :type base_datos: str
    """

    def __init__(self, base_datos="autos_mercado.db"):
        """Constructor de la clase ConexionBD."""
        self.base_datos = base_datos
        self.conexion = None
        self.cursor = None

    def conectar(self):
        """
        Establece la conexión con la base de datos y crea el cursor.
        Captura excepciones en caso de fallo de conexión.
        """
        try:
            self.conexion = sqlite3.connect(self.base_datos)
            self.cursor = self.conexion.cursor()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def desconectar(self):
        """
        Guarda los cambios (commit) y cierra la conexión a la base de datos
        si es que se encuentra activa
        """
        if self.conexion:
            self.conexion.commit()
            self.conexion.close()