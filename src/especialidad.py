# especialidad.py
class Especialidad:
    def __init__(self, tipo: str, dias: list):
        if not tipo or not dias:
            raise ValueError("La especialidad y los días de atención son obligatorios")

        dias_validos = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        for dia in dias:
            if dia.lower() not in dias_validos:
                raise ValueError(f"Día inválido: {dia}")

        self.__tipo__ = tipo
        self.__dias__ = [d.lower() for d in dias]

    def obtener_especialidad(self) -> str:
        return self.__tipo__

    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in self.__dias__

    def __str__(self):
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias_str})"
