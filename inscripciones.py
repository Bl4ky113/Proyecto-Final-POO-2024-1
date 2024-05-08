# !/usr/bin/python3

import sqlite3
import logging
import re
import os

import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)

class Inscripciones_2:
    # db variables
    db_path = "Inscripciones.db"
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    db_tables = {
        "careers": "Carreras",
        "students": "Alumnos",
        "courses": "Cursos",
        "records": "Inscritos"
    }

    def __init__(self, master=None):
        self.config_db()
        # Ventana principal
        self.win = tk.Tk(master)
        self.win.configure(
            background="#f7f9fd",
            height=600,
            width=800
        )

        '''
        con abspath() se calcula la ruta absoluta del archivo
        con dirname() se obtiene la ruta del directorio inscripciones
        con join() une los parametros como una ruta
        '''
        file_path = os.path.dirname(os.path.abspath(__file__))
        imagen_path = os.path.join(file_path,'img','icono.png')
        self.win.iconphoto(True,tk.PhotoImage(file=imagen_path))

        self.win.geometry(self.centrarVentana(800,600))
        
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")

        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(
            background="#f7f9fd",
            height=600,
            width=800
        )
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(
            background="#f7f9fd",
            font="{Arial} 11 {bold}",
            justify="left",
            state="normal",
            takefocus=False,
            text='No.Inscripción'
        )

        # Label No. Inscripción
        self.lblNoInscripcion.place(
            anchor="nw",
            x=680,
            y=20
        )

        #Entry No. Inscripción
        self.num_Inscripcion = ttk.Entry(self.frm_1, name="num_inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)

        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha")
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)

        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)

        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno", values=self.idcbox(),state="readonly")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.autocompletar )
        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)

        #Entry Alumno
        self.nombre_Alumno= tk.StringVar()
        self.nombres = ttk.Entry(self.frm_1, name="nombres",textvariable=self.nombre_Alumno)
        self.nombres.place(anchor="nw", width=200, x=100, y=130)

        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)

        #Entry Apellidos
        self.apellido_Alumno = tk.StringVar()
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos", textvariable=self.apellido_Alumno)
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)

        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=185)

        #Entry Curso
        self.id_Curso = ttk.Entry(self.frm_1, name="id_curso")
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=185)

        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)

        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)

        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)

        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        ''' Botones  de la Aplicación'''
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=260)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)

        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=260)

        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=260)

        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")

        #Columnas del Treeview
        self.tView_cols = ['tV_descripción']
        self.tView_dcols = ['tV_descripción']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)

        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Descripción')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)

        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h")
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y")
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

        # Main widget
        self.mainwindow = self.win
 
    def run(self):
        self.mainwindow.mainloop()

    def centrarVentana(self,w_ventana,h_ventana):
        x_ventana = self.win.winfo_screenwidth() // 2 - w_ventana // 2
        y_ventana = self.win.winfo_screenheight() // 2 - h_ventana // 2
        centrado=str(w_ventana) + "x" + str(h_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)

        return centrado

    def config_db (self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.create_tables()
        return

    def create_tables (self):
        seed_done = False

        self.cursor = self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Carreras (
                Código_Carrera VARCHAR(16) NOT NULL,
                Descripción VARCHAR(128) NOT NULL,
                Num_Semestres SMALLINT(2) NOT NULL,

                PRIMARY KEY (Código_Carrera)
            );
            CREATE TABLE IF NOT EXISTS Alumnos (
                Id_Alumno VARCHAR(32) NOT NULL,
                Id_Carrera VARCHAR(16) NOT NULL,
                Nombres VARCHAR(64),
                Apellidos VARCHAR(64),
                Fecha_Ingreso DATE NOT NULL,
                Ciudad VARCHAR(64),
                Departamento VARCHAR(64),
                Dirección VARCHAR(64),
                Telef_Cel VARCHAR(16),
                Telef_Fijo VARCHAR(16),

                PRIMARY KEY (Id_Alumno),
                FOREIGN KEY (Id_Carrera) REFERENCES Carreras(Código_Carrera)
            );
            CREATE TABLE IF NOT EXISTS Cursos (
                Código_Curso VARCHAR(16) NOT NULL,
                Nombre_Curso VARCHAR(32) NOT NULL,
                Descripción_Curso VARCHAR(128),
                Num_Horas SMALLINT(2) NOT NULL,

                PRIMARY KEY (Código_Curso)
            );
            CREATE TABLE IF NOT EXISTS Inscritos (
                No_Inscripción INTEGER AUTO_INCREMENT,
                Id_Alumno VARCHAR(32) NOT NULL,
                Código_Curso VARCHAR(16) NOT NULL,
                Fecha_Inscripción DATE NOT NULL,

                PRIMARY KEY (No_Inscripción),
                FOREIGN KEY (Id_Alumno) REFERENCES Alumnos(Id_Alumno),
                FOREIGN KEY (Código_Curso) REFERENCES Cursos(Código_Curso)
            );
        ''')

        self.cursor.execute('SELECT COUNT(*) FROM Carreras;')
        
        if self.cursor.fetchone()[0] <= 0:
            logger.log(100, "SEEDING DATA TO DB AT: Carreras")
            self.cursor.execute('''
                INSERT INTO Carreras
                    (Código_Carrera, Descripción, Num_Semestres)
                VALUES
                    ("2933", "Ciencias de la Computación", 9),
                    ("2514", "Estadística", 9),
                    ("2518", "Matemáticas", 9),
                    ("2519", "Química", 10),
                    ("2516", "Física", 10),
                    ("2879", "Ingeniería de Sistemas y Computación", 10),
                    ("2544", "Ingeniería Eléctrica", 10),
                    ("2545", "Ingeniería Electrónica", 10),
                    ("2546", "Ingeniería Industrial", 10),
                    ("2547", "Ingeniería Mecánica", 10);
            ''')

            seed_done = True

        self.cursor.execute('SELECT COUNT(*) FROM Cursos')

        if self.cursor.fetchone()[0] <= 0:
            logger.log(100, "SEEDING DATA TO DB AT: Cursos")
            self.cursor.execute('''
                INSERT INTO Cursos
                    (Código_Curso, Nombre_Curso, Num_Horas)
                VALUES
                    ("2015168", "Fundamentos de Matemáticas", 72),
                    ("2015181", "Sistemas Númericos", 72),
                    ("2016377", "Cálculo Diferencial en una Variable", 72),
                    ("2015556", "Cálculo Integral en una Variable", 72),
                    ("2015162", "Cálculo Vectorial", 72),
                    ("2015555", "Álgebra Lineal Básica", 72),
                    ("2026573", "Introducción a las Ciencias de la Computación y a la Programación", 56),
                    ("2016375", "Programación Orientada a Objetos", 56),
                    ("2016699", "Estructuras de Datos", 56),
                    ("2016696", "Álgoritmos", 56),
                    ("2016698", "Elementos de Computadores", 56),
                    ("2016707", "Sistemas Operativos", 56);
            ''')

            seed_done = True

        self.cursor.execute('SELECT COUNT(*) FROM Alumnos')

        if self.cursor.fetchone()[0] <= 0:
            logger.log(100, "SEEDING DATA TO DB AT: Alumnos")
            self.cursor.execute('''
                INSERT INTO Alumnos
                    (Id_Alumno, Id_Carrera, Nombres, Apellidos, Fecha_Ingreso, Ciudad, Telef_Cel)
                VALUES
                    ("7856019526884687", "2933", "Martín", "Hernández", "2023-08-01", "Bogota", "1234567890"),
                    ("5399046924785948", "2518", "Friend", "Fellow", "2024-01-01", "Bogotá", "5432109876"),
                    ("1722202291005220", "2879", "Someone", "Subject", "2024-05-05", "Nowhere", "0000000000"),
                    ("4274203119662378", "2545", "Laura", "Moreno", "2023-08-01", "Fusagasuga", "1132432433");
            ''')

            seed_done = True

        if seed_done:
            self.connection.commit()

        self.cursor.close()

    def __get_element_by_id (self, element_table: str, element_id, id_config: dict) -> tuple():
        self.cursor = self.connection.cursor()
        element_table_str = self.db_tables[element_table]

        if element_table not in self.db_tables.keys():
            raise sqlite3.DataError(f"ELEMENT TABLE: {element_table} NOT AVAILABLE")

        if id_config["min"] > len(element_id) and len(element_id) > id_config["max"]:
            raise sqlite3.OperationalError('ID LENGHT INCORRECT')
        
        self.cursor.execute(f"SELECT * FROM {element_table_str} WHERE {id_config['label']}={element_id}")
        element = self.cursor.fetchone()

        self.cursor.close()

        logger.log(100, f"FETCHED '{element_table_str}' ELEMENT WITH ID '{element_id}'")

        return element

    def __get_all_elements (self, element_table: str) -> list(tuple()):
        self.cursor = self.connection.cursor()
        element_table_str = self.db_tables[element_table]

        if element_table not in self.db_tables.keys():
            raise sqlite3.DataError(f"ELEMENT TABLE: {element_table} IS NOT A VALID TABLE")

        self.cursor.execute(f"SELECT * FROM {element_table_str}")
        elements = self.cursor.fetchall()

        self.cursor.close()

        logger.log(100, f"FETCHED ALL '{element_table_str}' ELEMENTS")

        return elements

    def __get_elements_with_query (self, element_table, **filters) -> list(tuple()):
        self.cursor = self.connection.cursor()
        element_table_str = self.db_tables[element_table]
        query_str = ''

        if len(filters.keys()) <= 0:
            raise sqlite3.OperationalError('NO FILTERS AVAILABLE')

        self.cursor.execute(f"SELECT name FROM pragma_table_info(\"{element_table_str}\") AS table_info")
        table_columns = [column_tuple[0] for column_tuple in self.cursor.fetchall()]
        
        for i, filter_key in enumerate(filters.keys()):
            if (filter_key not in table_columns):
                logger.warning(f"FILTER '{filter_key}' NOT IN {element_table_str} SCHEMA")
                continue

            if i != 0:
                query_str += " AND "

            filter_value = filters[filter_key]
            
            query_str += f"\"{filter_key}\"=\"{filter_value}\""

        if not query_str:
            raise sqlite3.OperationalError('NO VALID FILTERS PASSED IN QUERY')

        self.cursor.execute(f"SELECT * FROM {element_table_str} WHERE {query_str}")
        elements = self.cursor.fetchall()

        self.cursor.close()

        logger.log(100, f"FETCHED '{element_table_str}' ELEMENT USING '{query_str}' QUERY")
        
        return elements

    def get_career_by_id (self, career_id: str) -> tuple([str, str, int]):
        career = self.__get_element_by_id(
            'careers',
            career_id,
            {
                "min": 4,
                "max": 16,
                "label": "Código_Carrera"
            }
        )

        if not career:
            raise sqlite3.DataError(f"CAREER WITH ID: {career_id} NOT FOUND")

        return career
                       
    def get_careers (self, filters: dict={}) -> list(tuple([str, str, int])):
        if (len(filters.keys()) == 0):
            careers = self.__get_all_elements('careers')

            if len(careers) <= 0:
                raise sqlite3.DataError('NO CAREERS AVAILABLE')

            return careers
        
        careers = self.__get_elements_with_query('careers', **filters)

        if len(careers) <= 0:
            raise sqlite3.DataError(f"NO CAREERS AVAILABLE WITH QUERY: {filters}")
        
        return careers

    def get_student_by_id (self, student_id: str) -> tuple([str, str, str, str, str, str, str, str, str, str]):
        student = self.__get_element_by_id(
            'students',
            student_id,
            {
                "min": 16,
                "max": 16,
                "label": "Id_Alumno"
            }
        )

        if not student:
            raise sqlite3.DataError(f"STUDENT WITH ID: {student_id} NOT FOUND")

        return student

    def get_students (self, filters: dict={}) -> list(tuple([str, str, str, str, str, str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            students = self.__get_all_elements('students')

            if len(students) <= 0:
                raise sqlite3.DataError('NO STUDENTS AVAILABLE')

            return students

        students = self.__get_elements_with_query('students', **filters)

        if len(students) <= 0:
            raise sqlite3.DataError(f"NO STUDENTS AVAILABLE WITH QUERY: {filters}")

        return students

    def get_course_by_id (self, course_id: str) -> tuple([str, str, str, int]):
        course = self.__get_element_by_id(
            'courses',
            course_id,
            {
                "min": 7,
                "max": 7,
                "label": "Código_Curso"
            }
        )

        if not course:
            raise sqlite3.DataError(f"COURSE WITH ID: {course_id} NOT FOUND")

        return course

    def get_courses (self, filters: dict={}) -> list(tuple([str, str, str, int])):
        if (len(filters.keys()) == 0):
            courses = self.__get_all_elements('courses')

            if len(courses) <= 0:
                raise sqlite3.DataError('NO COURSES AVAILABLE')

            return courses

        courses = self.__get_elements_with_query('courses', **filters)

        if len(courses) <= 0:
            raise sqlite3.DataError(f"NO COURSES AVAILABLE WITH QUERY: {filters}")

        return courses

    def get_record_by_id (self, record_id: str) -> tuple([str, str, str, str, str, str, str, str, str, str]):
        record = self.__get_element_by_id(
            'records',
            record_id,
            {
                "min": 16,
                "max": 16,
                "label": "Id_Alumno"
            }
        )

        if not record:
            raise sqlite3.DataError(f"RECORD WITH ID: {record_id} NOT FOUND")

        return record

    def get_records (self, filters: dict={}) -> list(tuple([str, str, str, str, str, str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            records = self.__get_all_elements('records')

            if len(records) <= 0:
                raise sqlite3.DataError('NO RECORDS AVAILABLE')

            return records

        records = self.__get_elements_with_query('records', **filters)

        if len(records) <= 0:
            raise sqlite3.DataError(f"NO RECORDS AVAILABLE WITH QUERY: {filters}")

        return records


    ## autocompleta el nombre yy el apellido esta conectado al combobox
    def autocompletar(self,event):
        student_id = self.cmbx_Id_Alumno.get()

        datos = self.get_student_by_id(student_id)
        nombres_Alu= datos[2]
        apellidos_Alu = datos[3]
        ##modificamos los entry de nombres y apellidos
        self.apellido_Alumno.set(apellidos_Alu)
        self.nombre_Alumno.set(nombres_Alu)

        return 
        

    def idcbox(self):
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SELECT Id_Alumno FROM Alumnos")
            elements = self.cursor.fetchall()
            self.cursor.close()   
            return elements  
    

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
    
