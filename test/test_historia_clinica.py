import unittest
from datetime import datetime
from src.historia_clinica import HistoriaClinica
from src.paciente import Paciente
from src.turno import Turno
from src.receta import Receta
from src.medico import Medico
from src.especialidad import Especialidad

class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("12345678", "Juan Perez", "15/05/1990")
        self.medico = Medico("M001", "Dra. García","Cardiología")
        self.especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.historia = HistoriaClinica(self.paciente)

    def test_historia_clinica_vacia(self):
        self.assertEqual(self.historia.obtener_turnos(), [])
        self.assertEqual(self.historia.obtener_recetas(), [])
        texto = str(self.historia)
        self.assertIn("Sin turnos registrados", texto)
        self.assertIn("Sin recetas registradas", texto)

    def test_agregar_y_obtener_turno(self):
        fecha = datetime(2025, 6, 16, 10, 30)
        turno = Turno(self.paciente, self.medico, fecha, "Cardiología", "lunes")
        self.historia.agregar_turno(turno)
        turnos = self.historia.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertIs(turnos[0], turno)
        self.assertIn("Turnos:", str(self.historia))

    def test_agregar_y_obtener_receta(self):
        receta = Receta(self.paciente, self.medico, ["Paracetamol", "Ibuprofeno"])
        self.historia.agregar_receta(receta)
        recetas = self.historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertIs(recetas[0], receta)
        self.assertIn("Recetas:", str(self.historia))

    def test_str_completo(self):
        # agrega turno y receta
        fecha = datetime(2025, 6, 16, 10, 30)
        turno = Turno(self.paciente, self.medico, fecha, "Cardiología", "lunes")
        receta = Receta(self.paciente, self.medico, ["Paracetamol"])
        self.historia.agregar_turno(turno)
        self.historia.agregar_receta(receta)

        resultado = str(self.historia)
        self.assertIn("Historia Clínica de Juan Perez", resultado)
        self.assertIn("Turnos:", resultado)
        self.assertIn("Recetas:", resultado)
        self.assertIn("Cardiología", resultado)
        self.assertIn("Paracetamol", resultado)


if __name__ == '__main__':
    unittest.main()
