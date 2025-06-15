# medico.py
from src.especialidad import Especialidad


class Medico:
    def __init__(self, matricula: str, nombre: str,especialidad: str):
        if not matricula or not nombre:
            raise ValueError("La matrícula y el nombre son obligatorios")

        self.__matricula__ = matricula
        self.__nombre__ = nombre
        self.__especialidades__:list[Especialidad] = []

    def agregar_especialidad(self, especialidad: Especialidad):
        if not isinstance(especialidad, Especialidad):
            raise TypeError("Debe agregar una instancia de Especialidad")

        if especialidad in self.__especialidades__:
            return  # evitar duplicados

        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades = ", ".join(str(e) for e in self.__especialidades__)
        return f"{self.__nombre__} (Matrícula: {self.__matricula__})\nEspecialidades: {especialidades}"
