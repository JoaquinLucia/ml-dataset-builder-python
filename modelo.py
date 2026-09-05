"""
Módulo de gestión de datos (Modelo).
Contiene la clase GestorAutos que maneja las operaciones CRUD
(Crear, Leer, Actualizar, Borrar) conectándose a la base de datos SQLite3.
"""

from conexion import ConexionBD


class GestorAutos:
    """
    Clase que representa el modelo de datos para los vehículos.
    Maneja la creación de la tabla y las transacciones.
    """

    def __init__(self):
        """Inicializa la base y crea la tabla."""
        self.db = ConexionBD()
        self.crear_tabla()

    def crear_tabla(self):
        """
        Crea la tabla 'registro_autos' si no existe, definiendo
        la estructura y tipos de datos de todas las columnas.
        """
        self.db.conectar()
        sql = """
            CREATE TABLE IF NOT EXISTS registro_autos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL UNIQUE,
                descripcion TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                kilometraje INTEGER NOT NULL,
                traccion TEXT NOT NULL,
                precio_usd REAL NOT NULL,
                cilindrada REAL NOT NULL,
                valvulas INTEGER NOT NULL
            )
        """
        try:
            self.db.cursor.execute(sql)
            self.db.conexion.commit()
        except Exception as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.db.desconectar()

    def alta_auto(self, titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas):
        """
        Inserta un nuevo vehículo en la base de datos.

        :param titulo: ID único alfanumérico del vehículo.
        :type titulo: str
        :param descripcion: Breve detalle del estado del auto.
        :type descripcion: str
        :param marca: Marca del fabricante.
        :type marca: str
        :param modelo: Modelo específico.
        :type modelo: str
        :param anio: Año de fabricación.
        :type anio: int
        :param kilometraje: Kilómetros recorridos.
        :type kilometraje: int
        :param traccion: Tipo de tracción (Delantera, Trasera, Integral).
        :type traccion: str
        :param precio_usd: Valor del vehículo en dólares.
        :type precio_usd: float
        :param cilindrada: Capacidad del motor en litros.
        :type cilindrada: float
        :param valvulas: Cantidad total de válvulas del motor.
        :type valvulas: int
        :return: True si se guardó correctamente, False en caso de error.
        :rtype: bool
        """
        self.db.conectar()
        sql = """
            INSERT INTO registro_autos 
            (titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.db.cursor.execute(sql, (titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas))
            self.db.conexion.commit()
            print(f"Vehículo '{titulo}' guardado en el dataset con éxito.")
            return True
        except Exception as e:
            print(f"Error al guardar el vehículo: {e}")
            return False
        finally:
            self.db.desconectar()
    
    def consultar_autos(self):
        """
        Consulta y devuelve todos los registros guardados en la tabla.

        :return: Lista de tuplas con los datos de cada vehículo.
        :rtype: list
        """
        self.db.conectar()
        sql = "SELECT * FROM registro_autos"
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return registros
        except Exception as e:
            print(f"Error al consultar la base de datos: {e}")
            return []
        finally:
            self.db.desconectar()

    def borrar_auto(self, titulo):
        """
        Elimina un vehículo de la base de datos usando su ID único (título).

        :param titulo: ID único del vehículo a eliminar.
        :type titulo: str
        :return: True si se eliminó correctamente, False en caso de error.
        :rtype: bool
        """
        self.db.conectar()
        sql = "DELETE FROM registro_autos WHERE titulo = ?"
        try:
            self.db.cursor.execute(sql, (titulo,))
            self.db.conexion.commit()
            print(f"Vehículo '{titulo}' eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al intentar borrar el vehículo: {e}")
            return False
        finally:
            self.db.desconectar()

    def modificar_auto(self, titulo_buscar, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas):
        """
        Modifica los datos de un vehículo existente filtrando por su ID único.

        :param titulo_buscar: El ID único del vehículo que se desea actualizar.
        :type titulo_buscar: str
        :param descripcion: Nueva descripción.
        :type descripcion: str
        :param marca: Nueva marca.
        :type marca: str
        :param modelo: Nuevo modelo.
        :type modelo: str
        :param anio: Nuevo año.
        :type anio: int
        :param kilometraje: Nuevo kilometraje.
        :type kilometraje: int
        :param traccion: Nueva tracción.
        :type traccion: str
        :param precio_usd: Nuevo precio.
        :type precio_usd: float
        :param cilindrada: Nueva cilindrada.
        :type cilindrada: float
        :param valvulas: Nueva cantidad de válvulas.
        :type valvulas: int
        :return: True si se actualizó correctamente, False en caso de error.
        :rtype: bool
        """
        self.db.conectar()
        sql = """
            UPDATE registro_autos 
            SET descripcion=?, marca=?, modelo=?, anio=?, kilometraje=?, traccion=?, precio_usd=?, cilindrada=?, valvulas=?
            WHERE titulo=?
        """
        try:
            self.db.cursor.execute(sql, (descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas, titulo_buscar))
            self.db.conexion.commit()
            print(f"Vehículo '{titulo_buscar}' actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al modificar el vehículo: {e}")
            return False
        finally:
            self.db.desconectar()