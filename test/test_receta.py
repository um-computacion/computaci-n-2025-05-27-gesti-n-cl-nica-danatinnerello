# test_receta.py
import unittest
from src.paciente import Paciente
from src.medico import Medico
from src.receta import Receta

class TestReceta(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("12345678", "Juan Pérez", "01/01/1990")
        self.medico = Medico("MAT001", "Dra. Gómez","Nutricionista")

    def test_receta_valida(self):
        receta = Receta(self.paciente, self.medico, ["Ibuprofeno", "Paracetamol"])
        self.assertIn("Ibuprofeno", str(receta))
        self.assertIn("Dra. Gómez", str(receta))

    def test_error_medicamentos_vacios(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, [])

    def test_error_medicamento_invalido(self):
        with self.assertRaises(ValueError):
            Receta(self.paciente, self.medico, ["", " "])

    def test_error_paciente_invalido(self):
        with self.assertRaises(TypeError):
            Receta("no_paciente", self.medico, ["Ibuprofeno"])

    def test_error_medico_invalido(self):
        with self.assertRaises(TypeError):
            Receta(self.paciente, "no_medico", ["Ibuprofeno"])

if __name__ == '__main__':
    unittest.main()
