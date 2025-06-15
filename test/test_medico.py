# test_medico.py
import unittest
from src.medico import Medico
from src.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def test_creacion_medico_valido(self):
        medico = Medico("MAT001", "Dra. López", "Clínico")
        self.assertEqual(medico.obtener_matricula(), "MAT001")
        self.assertIn("Dra. López", str(medico))

    def test_error_datos_vacios(self):
        with self.assertRaises(ValueError):
            Medico("", "","")

    def test_agregar_especialidad(self):
        medico = Medico("MAT002", "Dr. Ruiz","Pediatría")
        esp = Especialidad("Pediatría", ["lunes"])
        medico.agregar_especialidad(esp)
        self.assertIn("Pediatría", str(medico))

    def test_especialidad_para_dia_valido(self):
        medico = Medico("MAT003", "Dr. Diaz","Clínica")
        esp = Especialidad("Clínica", ["martes"])
        medico.agregar_especialidad(esp)
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Clínica")

    def test_especialidad_para_dia_invalido(self):
        medico = Medico("MAT004", "Dra. Alba","Cardiología")
        esp = Especialidad("Cardiología", ["lunes"])
        medico.agregar_especialidad(esp)
        self.assertIsNone(medico.obtener_especialidad_para_dia("viernes"))

    def test_crear_medico_datos_vacios(self):
        with self.assertRaises(ValueError):
            Medico("", "Dra. García","Cardiología")
        with self.assertRaises(ValueError):
            Medico("M001", "","Cardiología")

    def test_agregar_especialidad_invalida(self):
        medico = Medico("M001", "Dra. García", "Cardiología")
        with self.assertRaises(TypeError):
            medico.agregar_especialidad("no es especialidad")

    def test_agregar_especialidad_duplicada(self):
        medico = Medico("M001", "Dra. García","Cardiología")
        esp = Especialidad("Cardiología", ["lunes"])
        medico.agregar_especialidad(esp)
        medico.agregar_especialidad(esp)  # no debe duplicar
        self.assertEqual(str(medico).count("Cardiología"), 1)

    def test_especialidad_para_dia_existente(self):
        medico = Medico("M001", "Dra. García","Dermatología")
        esp = Especialidad("Dermatología", ["martes"])
        medico.agregar_especialidad(esp)
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Dermatología")

    def test_especialidad_para_dia_inexistente(self):
        medico = Medico("M001", "Dra. García","D3ernatología")
        esp = Especialidad("Dermatología", ["martes"])
        medico.agregar_especialidad(esp)
        self.assertIsNone(medico.obtener_especialidad_para_dia("viernes"))


if __name__ == '__main__':
    unittest.main()
