# receta.py
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        if not isinstance(paciente, Paciente) or not isinstance(medico, Medico):
            raise TypeError("Paciente y médico deben ser objetos válidos")

        if not medicamentos or not all(isinstance(m, str) and m.strip() for m in medicamentos):
            raise ValueError("Debe incluir al menos un medicamento válido")

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = datetime.now()

    def __str__(self) -> str:
        meds = ", ".join(self.__medicamentos__)
        fecha_str = self.__fecha__.strftime("%d/%m/%Y")
        return f"Receta emitida el {fecha_str} para {self.__paciente__}\nMédico: {self.__medico__}\nMedicamentos: {meds}"
    
    