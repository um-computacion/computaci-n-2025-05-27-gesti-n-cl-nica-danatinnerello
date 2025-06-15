# test_especialidad.py
import unittest
from src.especialidad import Especialidad

class TestEspecialidad(unittest.TestCase):

    def test_creacion_valida(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.assertEqual(esp.obtener_especialidad(), "Pediatría")
        self.assertTrue(esp.verificar_dia("lunes"))
        self.assertIn("lunes", str(esp))

    def test_error_dia_invalido(self):
        with self.assertRaises(ValueError):
            Especialidad("Traumatología", ["funday"])

    def test_error_datos_vacios(self):
        with self.assertRaises(ValueError):
            Especialidad("", [])

    def test_dia_no_disponible(self):
        esp = Especialidad("Clínica", ["martes"])
        self.assertFalse(esp.verificar_dia("jueves"))

    def test_str_representacion(self):
        esp = Especialidad("Cardiología", ["lunes", "viernes"])
        resultado = str(esp)
        self.assertIn("Cardiología", resultado)
        self.assertIn("lunes", resultado)

if __name__ == '__main__':
    unittest.main()
