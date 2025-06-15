import unittest
from datetime import datetime
from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.excepciones import *
from src.receta import Receta  # Asegurate de tener este archivo
from src.turno import Turno

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("12345678", "Juan Perez", "15/05/1990")
        self.medico = Medico("M001", "Dra. García","Cardiología")
        self.especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])

    def test_agregar_paciente(self):
        self.clinica.agregar_paciente(self.paciente)
        self.assertIn(self.paciente, self.clinica.obtener_pacientes())

    def test_agregar_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(PacienteYaExiste):
            self.clinica.agregar_paciente(self.paciente)

    def test_agregar_medico(self):
        self.clinica.agregar_medico(self.medico)
        self.assertIn(self.medico, self.clinica.obtener_medicos())

    def test_agregar_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(MedicoYaExisteError):
            self.clinica.agregar_medico(self.medico)

    def test_agendar_turno_correcto(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime(2025, 6, 16, 10, 0)  # Lunes
        turno = self.clinica.agendar_turno("12345678", "M001", fecha, "lunes")
        self.assertEqual(turno.obtener_fecha_hora(), fecha)

    def test_agendar_turno_paciente_inexistente(self):
        self.clinica.agregar_medico(self.medico)
        self.medico.agregar_especialidad(self.especialidad)

        with self.assertRaises(PacienteNoExisteError):
            self.clinica.agendar_turno("99999999", "M001", datetime(2025, 6, 16, 10, 0), "lunes")

    def test_agendar_turno_medico_inexistente(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(MedicoNoExisteError):
            self.clinica.agendar_turno("12345678", "NOEXISTE", datetime(2025, 6, 16, 10, 0), "lunes")

    def test_agendar_turno_especialidad_no_disponible(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)  # no se le agregó especialidad

        with self.assertRaises(EspecialidadNoDisponibleError):
            self.clinica.agendar_turno("12345678", "M001", datetime(2025, 6, 16, 10, 0),    "lunes")

    def test_agendar_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno("12345678", "M001", fecha, "lunes")

        with self.assertRaises(TurnoDuplicadoError):
            self.clinica.agendar_turno("12345678", "M001", fecha, "lunes")

    def test_emitir_receta_correcta(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

        receta = self.clinica.emitir_receta("12345678", "M001", ["Paracetamol", "Ibuprofeno"])
        self.assertIn("Paracetamol", str(receta))

    def test_emitir_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

        with self.assertRaises(RecetaInvalidaError):
            self.clinica.emitir_receta("12345678", "M001", [])

    def test_obtener_historia_clinica(self):
        self.clinica.agregar_paciente(self.paciente)
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIn("Juan Perez", str(historia))

    def test_obtener_historia_clinica_inexistente(self):
        with self.assertRaises(PacienteNoExisteError):
            self.clinica.obtener_historia_clinica("99999999")

    def test_obtener_pacientes_vacio(self):
        self.assertEqual(self.clinica.obtener_pacientes(), [])

    def test_obtener_medicos_vacio(self):
        self.assertEqual(self.clinica.obtener_medicos(), [])

    def test_obtener_turnos_vacio(self):
        self.assertEqual(self.clinica.obtener_turnos(), [])

    def test_obtener_dia_semana_en_espanol(self):
        fecha = datetime(2025, 6, 16)  # Lunes
        dia = self.clinica.obtener_dia_semana_en_espanol(fecha)
        self.assertEqual(dia, "lunes")

    def test_agregar_especialidad_no_modifica_clinica(self):
        self.clinica.agregar_medico(self.medico)
        especialidad = Especialidad("Dermatología", ["martes"])
        self.medico.agregar_especialidad(especialidad)
        # La clínica no se ve afectada directamente (se guarda solo en médico)
        self.assertEqual(len(self.clinica.obtener_medicos()), 1)

    def test_receta_emitida_con_medico_y_paciente_correctos(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        receta = self.clinica.emitir_receta("12345678", "M001", ["Ibuprofeno"])
        self.assertIn("Ibuprofeno", str(receta))


if __name__ == '__main__':
    unittest.main()
