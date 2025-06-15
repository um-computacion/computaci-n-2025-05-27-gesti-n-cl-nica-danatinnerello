# cli.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from datetime import datetime
from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.excepciones import *

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        print("\n--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            try:
                match opcion:
                    case "1": self.agregar_paciente()
                    case "2": self.agregar_medico()
                    case "3": self.agendar_turno()
                    case "4": self.agregar_especialidad()
                    case "5": self.emitir_receta()
                    case "6": self.ver_historia()
                    case "7": self.ver_turnos()
                    case "8": self.ver_pacientes()
                    case "9": self.ver_medicos()
                    case "0": print("Hasta luego"); break
                    case _: print("Opción no válida")
            except Exception as e:
                print(f"Error inesperado: {e}")

    def agregar_paciente(self):
        try:
            dni = input("DNI: ").strip()
            if not dni:
                print("Error: DNI no puede estar vacío.")
                return
            nombre = input("Nombre Completo: ").strip()
            if not nombre:
                print("Error: Nombre no puede estar vacío.")
                return
            fecha = input("Fecha nacimiento (DD/MM/AAAA): ").strip()
            if not fecha:
                print("Error: Fecha de nacimiento no puede estar vacía.")
                return
            paciente = Paciente(dni, nombre, fecha)
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado exitosamente.")
        except PacienteNoExisteError as e:
            print(f"Error: Paciente no encontrado {e}")
        except (FechaIncorrecta) as e:
            print(f"Error: {e}")

    def agregar_medico(self):
        try:
            matricula = input("Matrícula: ").strip()
            if not matricula:
                print("Error: Matrícula no puede estar vacía.")
                return
            nombre = input("Nombre: ").strip()
            if not nombre:
                print("Error: Nombre no puede estar vacío.")
                return
            especialidad = input("Especialidad: ").strip()
            if not especialidad:    
                print("Error: Especialidad no puede estar vacía.")
                return
            medico = Medico(matricula, nombre,especialidad)

            self.clinica.agregar_medico(medico)
            print("Médico agregado exitosamente.")
        except MedicoYaExisteError as e:
            print(f"Error: {e}")

    def agregar_especialidad(self):
        try:
            matricula = input("Matrícula del médico: ").strip()
            tipo = input("Especialidad: ").strip()

            dias = []
            print("Ingrese días (escriba 'fin' para terminar):")
            while True:
                dia = input("Día: ").strip().lower()
                if dia == "fin": break
                if dia: dias.append(dia)
            especialidad = Especialidad(tipo, dias)
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            medico.agregar_especialidad(especialidad)
            print("Especialidad agregada")
        except (ValueError, MedicoNoExisteError) as e:
            print(f"Error: {e}")

    def agendar_turno(self):
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matrícula del médico: ").strip()
            fecha_str = input("Fecha y hora (DD/MM/AAAA HH:MM): ").strip()
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            dia_semana = input("Ingrese dia de la semana: ")
            turno = self.clinica.agendar_turno(dni, matricula, fecha, dia_semana)
            print("Turno agendado")
            print(turno)
        except PacienteNoExisteError as e:
            print(f"Error: Paciente no encontrado{e}")
        except (MedicoNoExisteError, EspecialidadNoDisponibleError, TurnoDuplicadoError, ValueError) as e:
            print(f"Error: {e}")

    def emitir_receta(self):
        try:
            dni = input("DNI del paciente: ").strip()
            matricula = input("Médico que receta (matrícula): ").strip()
            meds_str = input("Medicamentos (separados por coma): ").strip()
            medicamentos = [m.strip() for m in meds_str.split(",") if m.strip()]

            receta = self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida")
            print(receta)
        except (PacienteNoExisteError, MedicoNoExisteError, RecetaInvalidaError, ValueError) as e:
            print(f"Error: {e}")

    def ver_historia(self):
        try:
            dni = input("DNI del paciente: ").strip()
            historia = self.clinica.obtener_historia_clinica(dni)
            print(historia)
        except PacienteNoExisteError as e:
            print(f"Error: {e}")

    def ver_turnos(self):
        for t in self.clinica.obtener_turnos():
            print(t)

    def ver_pacientes(self):
        for p in self.clinica.obtener_pacientes():
            print(p)

    def ver_medicos(self):
        for m in self.clinica.obtener_medicos():
            print(m)


if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()
