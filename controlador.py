"""
Módulo Controlador.
Actúa como intermediario entre la Vista y el Modelo,
aplicando las validaciones antes de interactuar con la base de datos.
"""

from modelo import GestorAutos
from validaciones import Validador, ErrorValidacion


class Controlador:
    """
    Clase que maneja la lógica de la aplicación y el flujo de datos
    """

    def __init__(self):
        """
        Constructor de la clase Controlador. Inicializa el modelo
        """
        self.modelo = GestorAutos()

    def procesar_alta(self, titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas):
        """
        Valida los datos y si son correctos, ordena al modelo guardar un nuevo vehículo

        :param titulo: ID único del vehículo.
        :type titulo: str
        :param descripcion: Breve descripción.
        :type descripcion: str
        :param marca: Marca del fabricante.
        :type marca: str
        :param modelo: Modelo del vehículo.
        :type modelo: str
        :param anio: Año de fabricación.
        :type anio: int
        :param kilometraje: Kilometraje actual.
        :type kilometraje: int
        :param traccion: Tipo de tracción.
        :type traccion: str
        :param precio_usd: Precio en dólares.
        :type precio_usd: float
        :param cilindrada: Cilindrada en litros.
        :type cilindrada: float
        :param valvulas: Cantidad de válvulas del motor.
        :type valvulas: int
        :return: Diccionario con el estado de la operación y un mensaje.
        :rtype: dict
        """
        try:
            # Pasamos por todas las validaciones
            Validador.validar_titulo(titulo)
            Validador.validar_anio(anio)
            Validador.validar_positivos(kilometraje, precio_usd)
            Validador.validar_cilindrada(cilindrada)
            Validador.validar_valvulas(valvulas)

            # Si pasó los filtros, mandamos a guardar
            exito = self.modelo.alta_auto(
                titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas
            )

            # Devolvemos un diccionario para la vista
            if exito:
                return {"estado": "agregado", "mensaje": "Vehículo agregado correctamente."}
            else:
                return {"estado": "error", "mensaje": "No se pudo guardar."}

        except ErrorValidacion as e:
            return {"estado": "error", "mensaje": str(e)}
        except Exception as e:
            return {"estado": "error", "mensaje": f"Error inesperado del sistema: {e}"}

    def procesar_consulta(self):
        """
        Solicita al modelo todos los registros guardados.

        :return: Diccionario con el estado y los datos recuperados.
        :rtype: dict
        """
        try:
            registros = self.modelo.consultar_autos()
            return {"estado": "exito", "datos": registros}
        except Exception as e:
            return {"estado": "error", "mensaje": f"Error al consultar la base de datos: {e}"}

    def procesar_baja(self, titulo):
        """
        Valida el ID y ordena al modelo borrar el registro correspondiente.

        :param titulo: ID único del vehículo a borrar.
        :type titulo: str
        :return: Diccionario con el estado de la operación y un mensaje.
        :rtype: dict
        """
        try:
            # Pasamos el ID por nuestra Regex antes de enviarlo a la base de datos
            Validador.validar_titulo(titulo)
            
            exito = self.modelo.borrar_auto(titulo)
            
            if exito:
                return {"estado": "exito", "mensaje": "Vehículo eliminado del dataset correctamente."}
            else:
                return {"estado": "error", "mensaje": "No se pudo eliminar. ¿Verificaste que el código exista?"}
                
        except ErrorValidacion as e:
            # Atrapamos el error si el usuario puso espacios o caracteres raros
            return {"estado": "error", "mensaje": str(e)}
        except Exception as e:
            return {"estado": "error", "mensaje": f"Error inesperado del sistema: {e}"}

    def procesar_modificacion(self, titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas):
        """
        Valida los datos nuevos y ordena al modelo actualizar el registro.

        :param titulo: ID único del vehículo a modificar.
        :type titulo: str
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
        :return: Diccionario con el estado de la operación y un mensaje.
        :rtype: dict
        """
        try:
            # Reutilizamos las validaciones
            Validador.validar_titulo(titulo)
            Validador.validar_anio(anio)
            Validador.validar_positivos(kilometraje, precio_usd)
            Validador.validar_cilindrada(cilindrada)
            Validador.validar_valvulas(valvulas)
            
            exito = self.modelo.modificar_auto(
                titulo, descripcion, marca, modelo, anio, kilometraje, traccion, precio_usd, cilindrada, valvulas
            )
            
            if exito:
                return {"estado": "exito", "mensaje": "Vehículo actualizado correctamente."}
            else:
                return {"estado": "error", "mensaje": "No se pudo modificar. ¿El código es correcto?"}
                
        except ErrorValidacion as e:
            return {"estado": "error", "mensaje": str(e)}
        except Exception as e:
            return {"estado": "error", "mensaje": f"Error inesperado: {e}"}