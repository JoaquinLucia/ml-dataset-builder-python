"""
Módulo de validaciones.
Contiene las reglas para asegurar la integridad de los datos
antes de ser guardados en la base de datos.
"""

import re


class ErrorValidacion(Exception):
    """
    Excepción personalizada lanzada cuando un campo no cumple
    con las reglas establecidas
    """
    pass


class Validador:
    """
    Clase con metodos que validan el correcto ingreso de los valores para el negocio
    """

    @staticmethod
    def validar_titulo(titulo):
        """
        Valida que el título contenga únicamente caracteres alfanuméricos.

        :param titulo: El código o ID único del vehículo.
        :type titulo: str
        :raises ErrorValidacion: Si el título contiene espacios o caracteres especiales.
        :return: True si la validación es exitosa.
        :rtype: bool
        """
        patron = r"^[A-Za-z0-9]+$"
        if not re.match(patron, titulo):
            raise ErrorValidacion("El título es inválido. Solo caracteres alfanuméricos (letras y números), sin espacios.")
        return True

    @staticmethod
    def validar_anio(anio):
        """
        Valida que el año del vehículo se encuentre dentro de un rango lógico.

        :param anio: Año de fabricación del vehículo.
        :type anio: int
        :raises ErrorValidacion: Si el año es menor a 1930 o mayor a 2026.
        :return: True si la validación es exitosa.
        :rtype: bool
        """
        if not (1930 <= anio <= 2026):
            raise ErrorValidacion(f"El año {anio} es incorrecto. Debe estar entre 1930 y 2026.")
        return True

    @staticmethod
    def validar_positivos(kilometraje, precio):
        """
        Valida que los valores numéricos como kilometraje y precio no sean negativos.

        :param kilometraje: Kilómetros recorridos por el vehículo.
        :type kilometraje: int
        :param precio: Valor del vehículo en dólares.
        :type precio: float
        :raises ErrorValidacion: Si alguno de los valores es menor a cero.
        :return: True si la validación es exitosa.
        :rtype: bool
        """
        if kilometraje < 0:
            raise ErrorValidacion("El kilometraje no puede ser un valor negativo.")
        if precio < 0:
            raise ErrorValidacion("El precio no puede ser un valor negativo.")
        return True

    @staticmethod
    def validar_cilindrada(cilindrada):
        """
        Valida que la cilindrada esté expresada en litros (ej: 1.6 o 2.0)
        y no en centímetros cúbicos (ej: 1600).

        :param cilindrada: Cilindrada del motor.
        :type cilindrada: float
        :raises ErrorValidacion: Si el valor está fuera del rango lógico (0.5 a 15.0).
        :return: True si la validación es exitosa.
        :rtype: bool
        """
        if not (0.5 <= cilindrada <= 15.0):
            raise ErrorValidacion(f"La cilindrada {cilindrada} es inválida. Ingresala en litros (ej: 1.6), no en cm3.")
        return True

    @staticmethod
    def validar_valvulas(valvulas):
        """
        Valida que la cantidad de válvulas sea un número lógico para un motor
        y que sea un número par.

        :param valvulas: Cantidad total de válvulas del vehículo.
        :type valvulas: int
        :raises ErrorValidacion: Si el valor es inferior a 2, mayor a 64 o impar.
        :return: True si la validación es exitosa.
        :rtype: bool
        """
        if valvulas < 2 or valvulas > 64:
            raise ErrorValidacion(f"La cantidad de válvulas ({valvulas}) es incorrecta para un motor estándar.")
        
        # Verificamos que el número sea par
        if valvulas % 2 != 0:
            raise ErrorValidacion(f"La cantidad de válvulas ({valvulas}) debe ser un número par (ej: 8, 16, 20).")
            
        return True