# test_turno.py
import unittest
from datetime import datetime
from src.paciente import Paciente
from src.medico import Medico
from src.turno import Turno

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("12345678", "Juan Pérez", "01/01/1990")
        self.medico = Medico("MAT001", "Dra. Gómez","Nutricionista")
        self.fecha = datetime(2025, 6, 14, 10, 30)
        self.dia_semana = "sábado"

    def test_creacion_turno_valido(self):
        turno = Turno(self.paciente, self.medico, self.fecha, "Clínica",self.dia_semana)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha)
        self.assertIn("Clínica", str(turno))

    def test_error_paciente_invalido(self):
        with self.assertRaises(TypeError):
            Turno("no_paciente", self.medico, self.fecha, "Clínica",self.dia_semana)

    def test_error_medico_invalido(self):
        with self.assertRaises(TypeError):
            Turno(self.paciente, "no_medico", self.fecha, "Clínica",self.dia_semana)

    def test_error_fecha_invalida(self):
        with self.assertRaises(TypeError):
            Turno(self.paciente, self.medico, "14/06/2025", "Clínica",self.dia_semana)

    def test_error_especialidad_vacia(self):
        with self.assertRaises(ValueError):
            Turno(self.paciente, self.medico, self.fecha, "",self.dia_semana)

if __name__ == '__main__':
    unittest.main()
