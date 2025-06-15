
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico
from src.turno import Turno
from src.receta import Receta
from src.especialidad import Especialidad
from src.historia_clinica import HistoriaClinica
from src.excepciones import (
    PacienteYaExiste,
    MedicoYaExisteError,
    PacienteNoExisteError,
    MedicoNoExisteError,
    TurnoDuplicadoError,
    RecetaInvalidaError,
    EspecialidadNoDisponibleError
)

class Clinica:
    def __init__(self):
        self.__pacientes__: dict[str, Paciente] = {}
        self.__medicos__: dict[str, Medico] = {}
        self.__turnos__: list[Turno] = []
        self.__historias_clinicas__: dict[str, HistoriaClinica] = {}


    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        #Validacion de paciente
        if dni in self.__pacientes__:
            raise PacienteYaExiste("El paciente ya está registrado")
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()
        #validacion de medico
        if matricula in self.__medicos__:
            raise MedicoYaExisteError("El médico ya está registrado")
        self.__medicos__[matricula] = medico

    def obtener_pacientes(self):
        return list(self.__pacientes__.values())

    def obtener_medicos(self):
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str):
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("Médico no encontrado")
        return self.__medicos__[matricula]

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime, dia_semana: str):
        for turno in self.__turnos__:
            if turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora and turno.verificar_dia_semana(dia_semana):
                raise TurnoDuplicadoError("El turno ya está ocupado para ese médico")

    def agendar_turno(self, dni: Paciente , matricula: str, fecha_hora: datetime, dia_semana: str):
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError("Error: Paciente no encontrado")
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("Médico no encontrado")

        medico = self.__medicos__[matricula]
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        #valida que el medico atienda esa especialidad ese dia 
        if not especialidad:
            raise EspecialidadNoDisponibleError("El médico no atiende ese día")

        self.validar_turno_no_duplicado(matricula, fecha_hora, dia_semana)

        turno = Turno(self.__pacientes__[dni], medico, fecha_hora, especialidad, dia_semana)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)
        return turno

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list):
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError("Error: Paciente no encontrado")
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("Médico no encontrado")
        if not medicamentos:
            raise RecetaInvalidaError("Debe incluir medicamentos")

        receta = Receta(self.__pacientes__[dni], self.__medicos__[matricula], medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)
        return receta

    def obtener_historia_clinica(self, dni: str):
        if dni not in self.__historias_clinicas__:
            raise PacienteNoExisteError("Historia clínica no encontrada")
        return self.__historias_clinicas__[dni]

    def obtener_turnos(self):
        return list(self.__turnos__)

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]

