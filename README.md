# Proyecto Final Programación Orientada a Objetos Grupo 4 2024-1

## Integrantes del Grupo

- Martín Steven Hernández Ortiz (mahernandezor@unal.edu.co)
- Martin Jose Botina González (mbotina@unal.edu.co)
- Laura Alejandra Moreno (lamorenobo@unal.edu.co)
- Nicolás Arturo Corredor Bello (nicorredorb@unal.edu.co)

## Requerimientos Generales
1. Modificar y hacer funcionar un aplicativo gráfico en Python 3 que usa la librería Tkinter con
ttk y con la apariencia que se muestra en el mockup proporcionado (Anexo 1).
2. El propósito del programa es manejar la información de los cursos a los que se pueden
inscribir los estudiantes de una universidad o instituto.
3. El aplicativo debe ser de tipo CRUD (Create, Read, Update, Delete) lo que significa que debe
permitir:
    - Crear o insertar información.
    - Leer o consultar la información.
    - Actualizar o modificar la información. La única información modificable es la que aparece en la tabla Inscritos.
    - Eliminar o borrar la información. La única información que se puede eliminar es la que
aparece en la tabla Inscritos.
4. Es obligatorio el uso de la base de datos SQLite3 para la persistencia de los datos.
5. Se debe crear un base de datos llamada Inscripciones.db (Anexo 2).
6. Se deben crear cuatro tablas en la base de datos llamadas Alumnos, Carreras, Cursos e
Inscritos. La estructura de las tablas se anexa en este documento y es obligatorio definirlas
de la misma forma dentro del sistema que se desarrolle (Anexo 3). Todas las tablas se deben
poblar manualmente con datos para verificar el funcionamiento y la única tabla vacía y que
se va poblando con el programa es la tabla Inscritos.
7. Es obligatorio usar el programa llamado plantilla.py (Anexo 4) que se proporciona para
alcanzar los objetivos planteados.
8. El trabajo se debe realizar en grupo de acuerdo con los grupos ya definidos.
9. Solo un miembro del grupo realiza la sustentación, aunque en ese momento es obligatoria
la presencia de todos los integrantes del grupo.
10. En cada clase presencial o virtual se destinará tiempo para resolver posibles dudas o
inquietudes.
11. La entrega del proyecto se realiza a más tardar el día 20 de mayo del 2024 a las 11:59:59
p.m.
12. Las sustentaciones se realizarán los días 21 y 23 de mayo del 2024 en el horario de clase y
seleccionará de forma aleatoria el grupo para sustentar.
13. Por lo anterior la presencia en ambas sesiones es obligatoria.

## Requerimientos Especificos
1. Al ejecutar la aplicación la ventana debe tener un icono personalizado y un título como se
muestra en el mockup.
2. Al ejecutar el programa la ventana debe quedar centrada sin importar el tipo de pantalla.
3. El campo No.Inscripción es auto incremental y deberá mostrar el número de inscripción
disponible.
4. El formato de fecha debe ser dd/mm/aaaa. La fecha que se solicita deber ser validada como
fecha cierta, es decir, no pueden existir fechas como 29 de febrero sin validar que el año sea
bisiesto. De igual forma se debe validar la cantidad de días que le corresponde a cada mes.
5. El combo box de identificación de los estudiantes debe ser cargado en tiempo de ejecución
con las identificaciones de todos los estudiantes almacenados en la tabla Estudiantes.
6. Los campos Nombres y Apellidos se deben llenar en forma automática tan pronto se
selecciona una identificación de estudiantes.
7. Los botones que se definen dentro del Mockup deben ser funcionales:
Botón Consultar: se considera libre de acción, lo que implica que cada grupo lo puede usar
para consultar información como estimen conveniente. Los datos de la consulta se deben
mostrar mediante el uso del treeView que aparece en la pantalla, en forma de grilla.
Botón Grabar: debe servir para grabar la información suministrada en las tablas de la base
de datos. Mediante el uso de una ventana emergente se de confirmar el éxito o fracaso de
la acción
Botón Editar: debe servir para modificar los datos almacenados en la base de datos y debe
permitir seleccionar una tupla de la grilla de datos (componente TreeView) para que se
puedan modificar en los campos de captura definidos en el mockup de la aplicación.
Mediante el uso de una ventana emergente se de confirmar el éxito o fracaso de la acción.
Botón Eliminar: deber servir para eliminar datos de forma individual o debe permitir
eliminar a un inscrito y todos sus cursos, confirmando en ambos casos su eliminación a
través de una ventana emergente que muestre el éxito o fracaso de la acción.
Botón Cancelar: debe servir para cancelar cualquier acción en curso y debe limpiar todos los
campos de captura mostrándolos vacíos en la pantalla.
Nota importante:
En el mockup el treeView es una muestra de lo que puede ser.
8. Las operaciones sobre la base de datos se deben realizar mediante sentencias SQL.

## Restricciones 
1. La estructura de directorios debe ser: Un directoria principal llamado Inscripciones
2. En el sub directorio db debe de estar la base de datos llamada Inscripciones.db
3. En el sub directorio img debe está el icono de la aplicación
4. En el directorio Inscripciones debe estar la plantilla modificada con el nombre final de
Inscripciones.py
5. La entrega del programa debe hacerse en formato comprimido tipo ZIP y no se admite
ningún otro formato como RAR, TAR, TARGZ o cualquier otro
6. No pueden crearse programas adicionales o módulos para ser importados, sólo debe existir un único
programa llamado Inscripciones.py
