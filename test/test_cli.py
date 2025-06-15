import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.cli import CLI
from src.excepciones import *
from src.paciente import Paciente
from src.medico import Medico
from src.clinica import Clinica

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()

    @patch("builtins.input", side_effect=["12345678", "Juan Perez", "15/05/1990"])
    def test_agregar_paciente_valido(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            mock_print.assert_any_call("Paciente agregado exitosamente.")

    @patch("builtins.input", side_effect=["", "Juan Perez", "15/05/1990"])
    def test_agregar_paciente_dni_vacio(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            mock_print.assert_any_call("Error: DNI no puede estar vacío.")

    @patch("builtins.input", side_effect=["12345678", "Juan Perez", "31/02/2025"])
    def test_agregar_paciente_fecha_invalida(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            self.assertTrue(any("formato de fecha" in str(c[0][0]).lower() or "formato" in str(c[0][0]).lower()
                                for c in mock_print.call_args_list))

    @patch("builtins.input", side_effect=["M001", "Dra. García","Cardiología"])
    def test_agregar_medico_valido(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_medico()
            mock_print.assert_any_call("Médico agregado exitosamente.")

    @patch("builtins.input", side_effect=["", "Dra. García"])
    def test_agregar_medico_matricula_vacia(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_medico()
            mock_print.assert_any_call("Error: Matrícula no puede estar vacía.")

    @patch("builtins.input", side_effect=[
        "M001", "Cardiología", "lunes", "fin"
    ])
    def test_agregar_especialidad(self, mock_input):
        medico = MagicMock()
        self.cli.clinica.obtener_medico_por_matricula = MagicMock(return_value=medico)
        with patch("builtins.print") as mock_print:
            self.cli.agregar_especialidad()
            medico.agregar_especialidad.assert_called()
            mock_print.assert_any_call("Especialidad agregada")

    @patch("builtins.input", side_effect=[
        "12345678", "Juan Perez", "15/05/1990",  # paciente
        "M001", "Dra. García",                  # médico
        "M001", "Cardiología", "lunes", "fin",  # especialidad
        "12345678", "M001", "16/06/2025 10:00,lunes"  # turno
    ])
    def test_agendar_turno_valido(self, mock_input):
        with patch("builtins.print"):
            self.cli.agregar_paciente()
            self.cli.agregar_medico()
            self.cli.agregar_especialidad()
            self.cli.agendar_turno()

    @patch("builtins.input", side_effect=["12345678", "M001", "   "])
    def test_emitir_receta_sin_medicamentos(self, mock_input):
        self.cli.clinica.emitir_receta = MagicMock(side_effect=RecetaInvalidaError("Debe incluir medicamentos"))
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            mock_print.assert_any_call("Error: Debe incluir medicamentos")

    @patch("builtins.input", side_effect=["12345678"])
    def test_ver_historia_paciente_no_existe(self, mock_input):
        self.cli.clinica.obtener_historia_clinica = MagicMock(side_effect=PacienteNoExisteError("Historia clínica no encontrada"))
        with patch("builtins.print") as mock_print:
            self.cli.ver_historia()
            mock_print.assert_any_call("Error: Historia clínica no encontrada")

    @patch("builtins.print")
    def test_ver_pacientes(self, mock_print):
        paciente = Paciente("12345678", "Juan Perez", "15/05/1990")
        self.cli.clinica.obtener_pacientes = MagicMock(return_value=[paciente])
        self.cli.ver_pacientes()
        mock_print.assert_any_call(paciente)

    @patch("builtins.print")
    def test_ver_medicos(self, mock_print):
        medico = Medico("M001", "Dra. García","Cardiología")
        self.cli.clinica.obtener_medicos = MagicMock(return_value=[medico])
        self.cli.ver_medicos()
        mock_print.assert_any_call(medico)

    @patch("builtins.input", side_effect=["12345678", "M001", "   ,   ,  "])
    def test_emitir_receta_espacios_sin_meds(self, mock_input):
        self.cli.clinica.emitir_receta = MagicMock(side_effect=ValueError("Medicamentos vacíos"))
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            self.assertTrue(any("medicamento" in str(c[0][0]).lower() for c in mock_print.call_args_list))

    @patch("builtins.input", side_effect=["z", "0"])
    def test_opcion_invalida_en_menu(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch("builtins.print") as mock_print:
                self.cli.ejecutar()
                mock_print.assert_any_call("Opción no válida")
                mock_print.assert_any_call("Hasta luego")

    @patch("builtins.input", side_effect=["0"])
    def test_salir_menu(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch("builtins.print") as mock_print:
                self.cli.ejecutar()
                mock_print.assert_any_call("Hasta luego")

    @patch("builtins.input", side_effect=["12345678", "M001", "fecha mala"])
    def test_agendar_turno_fecha_invalida(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            self.assertTrue(any("formato" in str(c[0][0]).lower() or "error" in str(c[0][0]).lower()
                                for c in mock_print.call_args_list))

    @patch("builtins.input", side_effect=["12345678", "M001", "Paracetamol"])
    def test_emitir_receta_medico_inexistente(self, mock_input):
        self.cli.clinica.emitir_receta = MagicMock(side_effect=MedicoNoExisteError("Médico no encontrado"))
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            mock_print.assert_any_call("Error: Médico no encontrado")

    @patch("builtins.input", side_effect=["M001", "Cardiología", "mierkoles", "fin"])
    def test_agregar_especialidad_dia_invalido(self, mock_input):
        self.cli.clinica.obtener_medico_por_matricula = MagicMock(return_value=MagicMock())
        with patch("builtins.print") as mock_print:
            self.cli.agregar_especialidad()
            self.assertTrue(any("inválido" in str(c[0][0]).lower() for c in mock_print.call_args_list))

    @patch("builtins.input", side_effect=["NOEXISTE", "Cardiología", "lunes", "fin"])
    def test_agregar_especialidad_medico_no_existe(self, mock_input):
        self.cli.clinica.obtener_medico_por_matricula = MagicMock(side_effect=MedicoNoExisteError("Médico no encontrado"))
        with patch("builtins.print") as mock_print:
            self.cli.agregar_especialidad()
            mock_print.assert_any_call("Error: Médico no encontrado")

    @patch("builtins.print")
    def test_ver_pacientes_vacio(self, mock_print):
        self.cli.clinica.obtener_pacientes = MagicMock(return_value=[])
        self.cli.ver_pacientes()
        mock_print.assert_not_called()  # No hay pacientes

    @patch("builtins.print")
    def test_ver_medicos_vacio(self, mock_print):
        self.cli.clinica.obtener_medicos = MagicMock(return_value=[])
        self.cli.ver_medicos()
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_ver_turnos_vacio(self, mock_print):
        self.cli.clinica.obtener_turnos = MagicMock(return_value=[])
        self.cli.ver_turnos()
        mock_print.assert_not_called()

    @patch("builtins.input", side_effect=["5"])
    def test_ejecutar_error_inesperado(self, mock_input):
        self.cli.emitir_receta = MagicMock(side_effect=Exception("Explota"))
        with patch("builtins.print") as mock_print:
            with patch.object(self.cli, "mostrar_menu", side_effect=[None, None]):
                with patch("builtins.input", side_effect=["5", "0"]):
                    self.cli.ejecutar()
                    self.assertTrue(any("error inesperado" in str(c[0][0]).lower() for c in mock_print.call_args_list))


    @patch("builtins.input", side_effect=["12345678", "", "15/05/1990"])
    def test_agregar_paciente_nombre_vacio(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            mock_print.assert_any_call("Error: Nombre no puede estar vacío.")

    @patch("builtins.input", side_effect=["12345678", "Juan Perez", ""])
    def test_agregar_paciente_fecha_vacia(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            mock_print.assert_any_call("Error: Fecha de nacimiento no puede estar vacía.")

    @patch("builtins.input", side_effect=["M001", "", "Cardiología"])
    def test_agregar_medico_nombre_vacio(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_medico()
            mock_print.assert_any_call("Error: Nombre no puede estar vacío.")

    @patch("builtins.input", side_effect=["M001", "Dr. Lopez", ""])
    def test_agregar_medico_especialidad_vacia(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_medico()
            mock_print.assert_any_call("Error: Especialidad no puede estar vacía.")

    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "lunes"])
    def test_agendar_turno_turno_duplicado(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=TurnoDuplicadoError("Turno duplicado"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Turno duplicado")

    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "martes"])
    def test_agendar_turno_especialidad_no_disponible(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=EspecialidadNoDisponibleError("Especialidad no disponible"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Especialidad no disponible")

    @patch("builtins.input", side_effect=["12345678", "NOEXISTE", "16/06/2025 10:00", "lunes"])
    def test_agendar_turno_medico_inexistente(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=MedicoNoExisteError("Médico no encontrado"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Médico no encontrado")

    @patch("builtins.input", side_effect=["12345678", "M001", "Paracetamol, Ibuprofeno"])
    def test_emitir_receta_valida(self, mock_input):
        receta_mock = MagicMock()
        self.cli.clinica.emitir_receta = MagicMock(return_value=receta_mock)
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            mock_print.assert_any_call("Receta emitida")
            mock_print.assert_any_call(receta_mock)

    @patch("builtins.input", side_effect=["NOEXISTE", "M001", "Paracetamol"])
    def test_emitir_receta_paciente_inexistente(self, mock_input):
        self.cli.clinica.emitir_receta = MagicMock(side_effect=PacienteNoExisteError("Paciente no encontrado"))
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            mock_print.assert_any_call("Error: Paciente no encontrado")

    @patch("builtins.input", side_effect=["12345678"])
    def test_ver_historia_valida(self, mock_input):
        historia_mock = "Historia clínica del paciente"
        self.cli.clinica.obtener_historia_clinica = MagicMock(return_value=historia_mock)
        with patch("builtins.print") as mock_print:
            self.cli.ver_historia()
            mock_print.assert_any_call(historia_mock)

    @patch("builtins.print")
    def test_ver_turnos_con_datos(self, mock_print):
        turno_mock = MagicMock()
        self.cli.clinica.obtener_turnos = MagicMock(return_value=[turno_mock])
        self.cli.ver_turnos()
        mock_print.assert_any_call(turno_mock)

    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "lunes"])
    def test_agendar_turno_exitoso(self, mock_input):
        turno_mock = MagicMock()
        self.cli.clinica.agendar_turno = MagicMock(return_value=turno_mock)
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Turno agendado")
            mock_print.assert_any_call(turno_mock)

    def test_mostrar_menu(self):
        with patch("builtins.print") as mock_print:
            self.cli.mostrar_menu()
            # Verificar que se imprimieron todas las opciones del menú
            expected_calls = [
                "1) Agregar paciente",
                "2) Agregar médico", 
                "3) Agendar turno",
                "4) Agregar especialidad a médico",
                "5) Emitir receta",
                "6) Ver historia clínica",
                "7) Ver todos los turnos",
                "8) Ver todos los pacientes",
                "9) Ver todos los médicos",
                "0) Salir"
            ]
            for expected in expected_calls:
                mock_print.assert_any_call(expected)
  
    @patch("builtins.input", side_effect=["M001", "Cardiología", "lunes", "fin"])
    def test_agregar_especialidad_error_en_agregar_a_medico(self, mock_input):
        medico_mock = MagicMock()
        medico_mock.agregar_especialidad.side_effect = ValueError("Error al agregar especialidad")
        self.cli.clinica.obtener_medico_por_matricula = MagicMock(return_value=medico_mock)
        with patch("builtins.print") as mock_print:
            self.cli.agregar_especialidad()
            mock_print.assert_any_call("Error: Error al agregar especialidad")

    @patch("builtins.input", side_effect=["12345678", "M001", "Paracetamol"])
    def test_emitir_receta_value_error_general(self, mock_input):
        self.cli.clinica.emitir_receta = MagicMock(side_effect=ValueError("Error de validación"))
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            mock_print.assert_any_call("Error: Error de validación")

    @patch("builtins.input", side_effect=["   12345678   ", "   Juan Perez   ", "   15/05/1990   "])
    def test_agregar_paciente_con_espacios_extras(self, mock_input):
        # Test que los strips funcionan correctamente
        with patch("builtins.print") as mock_print:
            self.cli.agregar_paciente()
            mock_print.assert_any_call("Paciente agregado exitosamente.")

    @patch("builtins.input", side_effect=["   M001   ", "   Dr. Garcia   ", "   Cardiología   "])
    def test_agregar_medico_con_espacios_extras(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.cli.agregar_medico()
            mock_print.assert_any_call("Médico agregado exitosamente.")

    @patch("builtins.input", side_effect=["   M001   ", "   Cardiología   ", "   lunes   ", "fin"])
    def test_agregar_especialidad_con_espacios_extras(self, mock_input):
        medico_mock = MagicMock()
        self.cli.clinica.obtener_medico_por_matricula = MagicMock(return_value=medico_mock)
        with patch("builtins.print") as mock_print:
            self.cli.agregar_especialidad()
            mock_print.assert_any_call("Especialidad agregada")

    @patch("builtins.input", side_effect=["   12345678   ", "   M001   ", "   16/06/2025 10:00   ", "   lunes   "])
    def test_agendar_turno_con_espacios_extras(self, mock_input):
        turno_mock = MagicMock()
        self.cli.clinica.agendar_turno = MagicMock(return_value=turno_mock)
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Turno agendado")

    @patch("builtins.input", side_effect=["   12345678   ", "   M001   ", "   Paracetamol,Ibuprofeno   "])
    def test_emitir_receta_con_espacios_extras_y_medicamentos(self, mock_input):
        receta_mock = MagicMock()
        self.cli.clinica.emitir_receta = MagicMock(return_value=receta_mock)
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            # Verificar que se llamó con medicamentos correctamente procesados
            self.cli.clinica.emitir_receta.assert_called_with("12345678", "M001", ["Paracetamol", "Ibuprofeno"])

    @patch("builtins.input", side_effect=["   12345678   "])
    def test_ver_historia_con_espacios_extras(self, mock_input):
        historia_mock = "Historia del paciente"
        self.cli.clinica.obtener_historia_clinica = MagicMock(return_value=historia_mock)
        with patch("builtins.print") as mock_print:
            self.cli.ver_historia()
            mock_print.assert_any_call(historia_mock)


    # Test del procesamiento de medicamentos con diferentes formatos
    @patch("builtins.input", side_effect=["12345678", "M001", "Paracetamol, , Ibuprofeno, ,Aspirina"])
    def test_emitir_receta_medicamentos_con_vacios_intercalados(self, mock_input):
        receta_mock = MagicMock()
        self.cli.clinica.emitir_receta = MagicMock(return_value=receta_mock)
        with patch("builtins.print") as mock_print:
            self.cli.emitir_receta()
            # Verificar que los medicamentos vacíos se filtraron correctamente
            self.cli.clinica.emitir_receta.assert_called_with("12345678", "M001", ["Paracetamol", "Ibuprofeno", "Aspirina"])

    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "lunes"])
    def test_agendar_turno_paciente_no_existe_mensaje_especifico(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=PacienteNoExisteError("Paciente con DNI 12345678 no encontrado"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Paciente no encontradoPaciente con DNI 12345678 no encontrado")

    @patch("builtins.input", side_effect=["1", "0"])
    def test_ejecutar_opcion_1(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "agregar_paciente") as mock_agregar:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_agregar.assert_called_once()

    @patch("builtins.input", side_effect=["2", "0"])
    def test_ejecutar_opcion_2(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "agregar_medico") as mock_agregar:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_agregar.assert_called_once()

    @patch("builtins.input", side_effect=["3", "0"])
    def test_ejecutar_opcion_3(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "agendar_turno") as mock_agendar:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_agendar.assert_called_once()

    @patch("builtins.input", side_effect=["4", "0"])
    def test_ejecutar_opcion_4(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "agregar_especialidad") as mock_agregar:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_agregar.assert_called_once()

    @patch("builtins.input", side_effect=["5", "0"])
    def test_ejecutar_opcion_5(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "emitir_receta") as mock_emitir:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_emitir.assert_called_once()

    @patch("builtins.input", side_effect=["6", "0"])
    def test_ejecutar_opcion_6(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "ver_historia") as mock_ver:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_ver.assert_called_once()

    @patch("builtins.input", side_effect=["7", "0"])
    def test_ejecutar_opcion_7(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "ver_turnos") as mock_ver:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_ver.assert_called_once()

    @patch("builtins.input", side_effect=["8", "0"])
    def test_ejecutar_opcion_8(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "ver_pacientes") as mock_ver:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_ver.assert_called_once()

    @patch("builtins.input", side_effect=["9", "0"])
    def test_ejecutar_opcion_9(self, mock_input):
        with patch.object(self.cli, "mostrar_menu"):
            with patch.object(self.cli, "ver_medicos") as mock_ver:
                with patch("builtins.print"):
                    self.cli.ejecutar()
                    mock_ver.assert_called_once()

    def test_constructor_cli(self):
        cli = CLI()
        self.assertIsInstance(cli.clinica, Clinica)

    # Test para verificar que sys.path se modifica correctamente (líneas 2-3)
    def test_sys_path_modification(self):
        # Este test verifica que el módulo se importa correctamente
        # Las líneas 2-3 del archivo se ejecutan al importar
        import sys
        import os
        expected_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Verificar que el path fue agregado (las líneas ya se ejecutaron al importar)
        self.assertTrue(any(expected_path in path for path in sys.path))

  
    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "lunes"])
    def test_agendar_turno_turno_duplicado(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=TurnoDuplicadoError("Turno duplicado"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Turno duplicado")

    @patch("builtins.input", side_effect=["12345678", "M001", "16/06/2025 10:00", "martes"])
    def test_agendar_turno_especialidad_no_disponible(self, mock_input):
        self.cli.clinica.agendar_turno = MagicMock(side_effect=EspecialidadNoDisponibleError("Especialidad no disponible"))
        with patch("builtins.print") as mock_print:
            self.cli.agendar_turno()
            mock_print.assert_any_call("Error: Especialidad no disponible")
    
if __name__ == "__main__":
    unittest.main()
