# SISTEMA DE GESTION PARA UNA CLINICA 

#Como ejecutar el sistema?
'''
Para ejecutar el sistema, asegúrate de tener Python instalado en tu máquina. Luego, sigue estos pasos:
1. Clona el repositorio o descarga los archivos del proyecto.
2. Abre una terminal y navega hasta el directorio donde se encuentran los archivos.
     ej: (yo) /home/dana/computaci-n-2025-05-27-gesti-n-cl-nica-danatinnerello
     Para ingresar al directorio, puedes usar el comando `cd` seguido de la ruta del directorio.
3. Ejecuta el archivo principal del sistema con el siguiente comando:
    ```bash
    python src/cli.py   
    o depende la version de python que tengas instalada, puede ser:
    ```bash
    python3 src/cli.py
    o si tienes un entorno virtual configurado, asegúrate de activarlo antes de ejecutar el comando.
4. Sigue las instrucciones en pantalla para interactuar con el sistema.
     '''

#Como ejecutar los tests?

'''
Para ejecutar los tests del sistema, asegúrate de tener Python instalado y sigue estos pasos:
1. Clona el repositorio o descarga los archivos del proyecto.
2. Abre una terminal y navega hasta el directorio donde se encuentran los archivos.
     ej: (yo) /home/dana/computaci-n-2025-05-27-gesti-n-cl-nica-danatinnerello
     Para ingresar al directorio, puedes usar el comando `cd` seguido de la ruta del directorio.
3. Asegúrate de tener `unittest` instalado. Si no lo tienes, puedes instalarlo con el siguiente comando:
    ```bash
    pip install unittest
    ```
4. Ejecuta los tests con el siguiente comando:
    ```bash
    python -m unittest (para ejecutar todos los tests)
    --o si quieres ejecutar un test en particular:    
    python -m unittest tests.test_nombre_del_test
    ```
5. Revisa los resultados de los tests en la terminal. Si todos los tests pasan, verás un mensaje indicando que todo está correcto.
6. Si algún test falla, revisa el mensaje de error para identificar el problema y corregirlo en el código.
'''
# Explicacion del diseño general del sistema
"""
El sistema de gestión para una clínica está diseñado para facilitar la administración de pacientes, médicos, turnos y recetas. A continuación se detalla el diseño general del sistema:
El sistema está compuesto por varias clases principales:
- **Clinica**: Clase principal que gestiona pacientes, médicos, turnos y recetas. Proporciona métodos para agregar pacientes y médicos, agendar turnos, emitir recetas y obtener historias clínicas.
- **Paciente**: Representa a un paciente con atributos como DNI, nombre completo y una historia clínica asociada. Permite agregar turnos y recetas a la historia clínica.
- **Medico**: Representa a un médico con atributos como matrícula, nombre completo y especialidades. Permite agregar especialidades y verificar si un médico atiende en un día específico.
- **Especialidad**: Representa una especialidad médica con un nombre y los días de la semana en que el médico atiende esa especialidad.
- **Turno**: Representa un turno agendado con un paciente, un médico, una fecha y hora, una especialidad y el día de la semana.
- **Receta**: Representa una receta médica emitida por un médico para un paciente, incluyendo una lista de medicamentos.
- **HistoriaClinica**: Representa la historia clínica de un paciente, que incluye turnos y recetas asociados.
- **Excepciones**: Se definen varias excepciones personalizadas para manejar errores específicos, como `PacienteYaExisteError`, `MedicoYaExisteError`, `TurnoDuplicadoError`, entre otras.
El sistema utiliza un enfoque orientado a objetos para encapsular la lógica de negocio y los datos relacionados con la clínica. Cada clase tiene sus propios métodos y atributos, lo que permite una fácil extensión y mantenimiento del código.
El sistema también incluye un CLI (Command Line Interface) que permite a los usuarios interactuar con la clínica a través de una interfaz de línea de comandos. El CLI proporciona un menú con opciones para agregar pacientes y médicos, agendar turnos, emitir recetas y ver historias clínicas, turnos, pacientes y médicos registrados.
El sistema está diseñado para ser modular y escalable, lo que permite agregar nuevas funcionalidades en el futuro sin afectar la estructura existente. Además, se implementan validaciones para garantizar la integridad de los datos y evitar duplicados en pacientes y médicos.
El sistema contiene tests unitarios para verificar el correcto funcionamiento de las clases y métodos, asegurando que se cumplan los requisitos funcionales y no funcionales del sistema.
"""