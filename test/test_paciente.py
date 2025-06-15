# test_paciente.py
import unittest
from datetime import datetime
from src.paciente import Paciente
from src.excepciones import FechaIncorrecta

class TestPaciente(unittest.TestCase):

    def test_creacion_paciente_valido(self):
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertIn("Juan Pérez", str(paciente))

    def test_error_fecha_invalida(self):
        with self.assertRaises(FechaIncorrecta):
            Paciente("12345678", "Juan Pérez", "1990-01-01")

    def test_error_campos_vacios(self):
        with self.assertRaises(ValueError):
            Paciente("", "", "")

    def test_str_representacion(self):
        paciente = Paciente("12345678", "Ana Torres", "02/02/1985")
        resultado = str(paciente)
        self.assertIn("Ana Torres", resultado)
        self.assertIn("12345678", resultado)

if __name__ == '__main__':
    unittest.main()
