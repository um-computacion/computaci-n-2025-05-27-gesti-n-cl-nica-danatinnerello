# turno.py
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str, dia_semana: str):
        if not isinstance(paciente, Paciente) or not isinstance(medico, Medico):
            raise TypeError("Debe pasar instancias válidas de Paciente y Medico")

        if not isinstance(fecha_hora, datetime):
            raise TypeError("La fecha y hora debe ser un objeto datetime")

        if not especialidad:
            raise ValueError("La especialidad es obligatoria")

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad
        self.__dia_semana__ = dia_semana

    def verificar_dia_semana(self, dia: str) -> bool:
        return self.__dia_semana__.lower() == dia.lower()
    
    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora__

    def __str__(self) -> str:
        return f"Turno: {self.__fecha_hora__.strftime('%d/%m/%Y %H:%M')} - {self.__especialidad__}\nPaciente: {self.__paciente__}\nMédico: {self.__medico__}/nDía: {self.__dia_semana__.capitalize()}"
