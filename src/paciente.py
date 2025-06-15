# paciente.py
from datetime import datetime
from src.excepciones import FechaIncorrecta

class Paciente:
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        if not dni or not nombre or not fecha_nacimiento:
            raise ValueError("Todos los campos del paciente son obligatorios")

        try:
            datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            raise FechaIncorrecta("Formato de fecha incorrecto. Use DD/MM/AAAA")

        self.__dni__ = dni
        self.__nombre__ = nombre
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def obtener_fecha_nacimiento(self) -> str:
        return self.__fecha_nacimiento__
    
    
    def __str__(self) -> str:
        return f"{self.__nombre__} (DNI: {self.__dni__}, Nacimiento: {self.__fecha_nacimiento__})"
