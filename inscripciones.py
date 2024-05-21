# !/usr/bin/python3

import sqlite3
import logging
import calendar
import typing
import re
import os

import tkinter as tk
import tkinter.ttk as ttk
from  tkinter import messagebox

logger = logging.getLogger(__name__)

class Inscripciones_2:
    # db constants
    db_path = "Inscripciones.db"
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    db_tables = {
        "careers": "Carreras",
        "students": "Alumnos",
        "courses": "Cursos",
        "records": "Inscritos"
    }

    # Schedule constants
    days_labels = {
        "M": "Lunes",
        "T": "Martes",
        "W": "Miércoles",
        "H": "Jueves",
        "F": "Viernes",
        "S": "Sábado",
        "U": "Domingo"
    }

    # Tk Constants
    btn_names = (
        "btnConsultar",
        "btnGuardar",
        "btnEditar",
        "btnEliminar",
    )

    current_action = ""
    available_actions = (
        "query",
        "save",
        "edit",
        "delete",
        "dialog-open"
    )

    
    def __init__(self, master=None):
        self.config_db()
        # Ventana principal
        self.win = tk.Tk(master)
        self.win.configure(
            background="#AED6F1",
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
        self.frm_1.after(0,self.inicial())
        self.frm_1.configure(
            background="#AED6F1",
            height=600,
            width=800
        )
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(
            background=None,
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
        self.num_InscripcionVar = tk.IntVar(value=self.numero_de_registro())
        self.num_Inscripcion = ttk.Label(self.frm_1, textvariable = self.num_InscripcionVar ,  name="num_inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=50, x=700, y=45)
        
        
        #Label Fecha
        
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:',foreground="#21618C")
        self.lblFecha.place(anchor="nw", x=630, y=80)

        #Entry Fecha
        self.fecha_value= tk.StringVar()
        self.fecha = ttk.Entry(self.frm_1, name="fecha",textvariable=self.fecha_value)
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        self.fecha.bind("<KeyRelease>", self.autocompletar_slash)

        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)

        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno", values=self.idcbox(),state="readonly")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.autocompletar_nombre )

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
        self.valor_id= tk.StringVar()
        self.id_Curso = ttk.Entry(self.frm_1, name="id_curso",textvariable=self.valor_id)
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=185)

        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)

        #Entry de Descripción del Curso 
        self.cmbx_Cursos = ttk.Combobox(self.frm_1,name="cmbx_cursos",values=self.cursosbox(),state="readonly")
        self.cmbx_Cursos.place(anchor="nw", width=300, x=325, y=185)
        self.cmbx_Cursos.bind("<<ComboboxSelected>>",self.autocompletar_datos_Curso)
        """
        self.nombre_del_curso= tk.StringVar()
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso",textvariable=self.nombre_del_curso)
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)
        """

        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Horario:')
        self.lblHorario.place(anchor="nw", x=635, y=185)

        #Entry del Horario
        self.schedule_variable = tk.StringVar()
        self.horario = ttk.Entry(
            self.frm_1,
            name="entry3",
            state="disabled",
            textvariable=self.schedule_variable
        )
        self.horario.configure(
            justify="left",
            width=166
        )
        self.horario.place(
            anchor="nw",
            width=100,
            x=690,
            y=185
        )
        self.horario.bind("<Button-1>", lambda event: self.open_schedule_dialog(self.schedule_variable))

        ''' Botones  de la Aplicación'''
        ## algo de color
        self.style= ttk.Style()
        self.style.configure('TButton', background='#85C1E9', foreground='black')

        #Boton Consultar
        self.btnConsultar= ttk.Button(self.frm_1, name=self.btn_names[0], command=self.abrir_consulta)
        self.btnConsultar.configure(text='Consultar')
        self.btnConsultar.place(anchor="nw",x=150,y=260)

        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name=self.btn_names[1] ,command=self.grabar_inscripcion)
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=250, y=260)
        
        #Botón Editar 
        self.btnEditar = ttk.Button(self.frm_1, name=self.btn_names[2], command = self.control_errores_edicion)
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=350, y=260)

        #Botón Eliminar
        self.btnEliminar = ttk.Button(
            self.frm_1, 
            name=self.btn_names[3],
            command=self.eliminar
        )
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=450, y=260)

        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name= "btnCancelar")
        self.btnCancelar.configure(text='Cancelar', command= self.cancel_Record)
        self.btnCancelar.place(anchor="nw", x=550, y=260)

        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=240)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView: ttk.Treeview = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #self.tView.bind("<ButtonRelease-1>", self.autocompletar_curso)
        #Columnas del Treeview
        tView_cols = ['No_Inscripción', 'Id_Alumno','Código_Curso', 'Horario', 'Fecha_Inscripción']
        self.tView.configure(
            columns=tView_cols,
            displaycolumns=tView_cols,
            selectmode='extended',
            padding=10
        )
        
        self.tView.column("#0", width=0, stretch="no")
        self.tView.column(tView_cols[0], anchor="w", width=50)
        self.tView.column(tView_cols[1], anchor="w", width=100)
        self.tView.column(tView_cols[2], anchor="w", width=100)
        self.tView.column(tView_cols[3], anchor="w", width=200)
        self.tView.column(tView_cols[4], anchor="w", width=100)
        #Cabeceras
        self.tView.heading("#0", text="")
        self.tView.heading(tView_cols[0], anchor="w", text="# Inscripción")
        self.tView.heading(tView_cols[1], anchor="w", text="Id Alumno")
        self.tView.heading(tView_cols[2], anchor="w", text="Código Curso")
        self.tView.heading(tView_cols[3], anchor="w", text="Horario")
        self.tView.heading(tView_cols[4], anchor="w", text="Fecha Inscripción")
        self.add_records_to_treeview()
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=290)
        self.tView.bind('<<TreeviewSelect>>',self.autocompletar_treeview)

        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h", command=self.tView.xview)
        self.scroll_H.configure(orient="horizontal")  
        self.scroll_H.place(anchor="s", height=15, width=774, x=400, y=590)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y",command=self.tView.yview)
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)
     
        # Configurar las barras de desplazamiento para el Treeview
        self.tView.configure(xscrollcommand=self.scroll_H.set, yscrollcommand=self.scroll_Y.set)

        # Main widget
        self.mainwindow = self.win  
 
    def run(self):
        self.mainwindow.mainloop()

    def eliminar(self):
        try:
            self.handle_delete_records()
            self.cancel_Record()
        except:
            messagebox.showerror("Error", "Por favor seleccione un dato en el treeview para eliminar")
        
        
    def inicial(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT MAX(No_Inscripción) FROM Inscritos")
        resultado = self.cursor.fetchone()
        self.cursor.close()
        if resultado[0] is not None:
            self.variable = int(resultado[0])
        else:
            self.variable = 0

    def centrarVentana(self,w_ventana,h_ventana):
        x_ventana = self.win.winfo_screenwidth() // 2 - w_ventana // 2
        y_ventana = self.win.winfo_screenheight() // 2 - h_ventana // 2
        centrado=str(w_ventana) + "x" + str(h_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        return centrado
    
    def validar_fecha(self):
        fecha_ingresada = self.fecha.get()
        formato_valido = re.match(r'\d{2}/\d{2}/\d{4}', fecha_ingresada)
        if formato_valido:
            dia, mes, anio = map(int, fecha_ingresada.split('/'))
            try:
                calendar.datetime.datetime(anio, mes, dia)
                return True
            except ValueError:
                return False
        else:
            return False
        
    def autocompletar_slash(self, event):
        fecha = self.fecha_value.get()
        if len(fecha) == 2 or len(fecha) == 5:
            if fecha[-1] != '/':
                self.fecha_value.set(fecha + '/')
                # Move cursor to the end of the entry
                self.fecha.icursor(len(self.fecha_value.get()))
                      
    def validate_hour (self, value):
        if re.fullmatch(r"\d{1,2}:\d\d", value) is None:
            return False
        
        return True

    def cancel_Record (self):
        # No action active 
        self.current_action = "" 

        # highlight all btns
        self.__highlight_btns(self.btn_names)

        # UnSelect all records in treeView
        self.tView.selection_remove(self.tView.selection())
        self.clear_Form()
        
        try:
            self.schedule_dialog.destroy()
        except:
            pass

        try:
            self.mini.destroy()
        except:
            pass
        try:
            self.schedule_dialog.destroy()
        except:
            pass
        try:
            self.ventanaConsulta.destroy()
        except:
            pass


    def clear_Form (self):
        self.num_InscripcionVar.set(self.numero_de_registro())
        self.fecha_value.set("")
        self.apellido_Alumno.set("")
        self.nombre_Alumno.set("")
        self.cmbx_Cursos.set("")
        self.valor_id.set("")
        self.schedule_variable.set("")
        self.cmbx_Id_Alumno.set("")
        return

    def numero_de_registro(self):   
        id_registro = self.variable + 1
        self.cursor.close()
        return id_registro 
    
    
    def no_registro_estudiante(self, student_id):    
        self.cursor = self.connection.cursor()  
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(student_id,))
        id = self.cursor.fetchone()
        self.cursor.close()
        if id is not None:
            return id[0]
        else:
            return self.numero_de_registro()
    
    def habilitar(self):
        
        self.__highlight_btns(self.btn_names)
    
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
                Descripción_Curso VARCHAR(128) NOT NULL,
                Num_Horas SMALLINT(2) NOT NULL,

                PRIMARY KEY (Código_Curso)
            );
            CREATE TABLE IF NOT EXISTS Inscritos (
                No_Inscripción INTEGER,
                Id_Alumno VARCHAR(32) NOT NULL,
                Código_Curso VARCHAR(16) NOT NULL,
                Horario VARCHAR(16) NOT NULL,
                Fecha_Inscripción DATE NOT NULL,

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
                    (Código_Curso, Descripción_Curso, Num_Horas)
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
                    ("78560195", "2933", "Martín", "Hernández", "2023/08/01", "Bogota", "1234567890"),
                    ("53990469", "2518", "Juan", "Morales", "2024/01/01", "Bogotá", "5432109876"),
                    ("17222022", "2879", "Andres", "hernandez", "2024/05/05", "Medellin", "0000000000"),
                    ("42742031", "2545", "Laura", "Moreno", "2023/08/01", "Fusagasuga", "1132432433"),
                    ("18273919", "2879", "Nicolas", "Corredor", "2023/08/01", "Bogotá", "1353515989"),
                    ("32458769", "2518", "María", "González", "2023/02/15", "Cali", "9876543210"),
                    ("56789012", "2933", "Ana", "Martínez", "2018/08/20", "Medellín", "6789012345"),
                    ("98765432", "2879", "Pedro", "López", "2021/08/10", "Bogotá", "4567890123"),
                    ("34567890", "2545", "Sofía", "Ramírez", "2022/08/25", "Barranquilla", "8901234567"),
                    ("89012345", "2518", "Carlos", "Gómez", "2020/08/05", "Cartagena", "7890123456"),
                    ("12345678", "2879", "Daniela", "Herrera", "2023/08/12", "Bucaramanga", "6789012345"),
                    ("45678901", "2933", "Diego", "Jiménez", "2021/08/30", "Cúcuta", "5678901234"),
                    ("78901234", "2545", "Valentina", "Díaz", "2018/08/08", "Santa Marta", "4567890123"),
                    ("90123456", "2879", "Lucas", "Sánchez", "2023/08/18", "Pereira", "3456789012"),
                    ("23456789", "2518", "Mariana", "Torres", "2019/08/02", "Manizales", "2345678901");

            ''')

            seed_done = True

        if seed_done:
            self.connection.commit()

        self.cursor.close()

    def __generate_columns_to_get_string (self, table_name: str, column_name_list: typing.Iterable[str]) -> str:
        column_name_str = ""

        if (len(column_name_list) <= 0):
            return "*" # ALL BY DEFAULT
        
        if (not self.__check_only_column_names_in_list(table_name, column_name_list)):
            table_name_str = self.db_tables[table_name]
            raise sqlite3.OperationalError(f'COLUMN NAMES TO GET NOT AVAILABLE IN {table_name_str} TABLE')

        for i, column_name in enumerate(column_name_list):
            if i != 0 and i != len(column_name_list):
                column_name_str += ', '

            column_name_str += column_name

        return column_name_str

    def __check_only_column_names_in_list (self, table_name: str, column_name_list: typing.Iterable[str]) -> bool:
        table_name_str = self.db_tables[table_name]

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT name FROM pragma_table_info(?) as table_info", (table_name_str, ))
        table_columns = [column_tuple[0] for column_tuple in self.cursor.fetchall()]

        for column_name in column_name_list:
            if (column_name not in table_columns):
                logger.warning(f"FILTER '{filter_key}' NOT IN {element_table_str} SCHEMA")
                return False

        return True

    def __get_element_by_id (self, element_table: str, element_id, id_config: dict, *columns_to_get: str) -> tuple():
        element_table_str = self.db_tables[element_table]
        columns_to_get_str = self.__generate_columns_to_get_string(element_table, columns_to_get)

        if id_config["min"] > len(element_id) and len(element_id) > id_config["max"]:
            raise sqlite3.OperationalError('ID LENGHT INCORRECT')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_to_get_str} FROM {element_table_str} WHERE {id_config['label']}=?", (element_id, ))
        element = self.cursor.fetchone()

        self.cursor.close()

        logger.log(100, f"FETCHED '{element_table_str}' ELEMENT WITH ID '{element_id}'")

        return element

    def __get_all_elements (self, element_table: str, *columns_to_get: str) -> list(tuple()):
        element_table_str = self.db_tables[element_table]
        columns_to_get_str = self.__generate_columns_to_get_string(element_table, columns_to_get)

        if element_table not in self.db_tables.keys():
            raise sqlite3.DataError(f"ELEMENT TABLE: {element_table} IS NOT A VALID TABLE")

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_to_get_str} FROM {element_table_str}")
        elements = self.cursor.fetchall()

        self.cursor.close()

        logger.log(100, f"FETCHED ALL '{element_table_str}' ELEMENTS")

        return elements

    def __get_elements_with_query (self, element_table: str, *columns_to_get: str, **filters) -> list(tuple()):
        element_table_str = self.db_tables[element_table]
        columns_to_get_str = self.__generate_columns_to_get_string(element_table, columns_to_get)
        query_values = []
        query_str = ''

        if len(filters.keys()) <= 0:
            raise sqlite3.OperationalError('NO FILTERS AVAILABLE')

        if not self.__check_only_column_names_in_list(element_table, filters.keys()):
            raise sqlite3.OperationalError(f'COLUMN NAMES TO FILTER NOT AVAILABLE IN {table_name_str} TABLE')
        
        for i, filter_key in enumerate(filters.keys()):
            if i != 0:
                query_str += " AND "

            filter_value = filters[filter_key]
            
            query_str += f"\"{filter_key}\"=?"
            query_values.append(filter_value)

        if not query_str:
            raise sqlite3.OperationalError('NO VALID FILTERS PASSED IN QUERY')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_to_get_str} FROM {element_table_str} WHERE {query_str}", query_values)
        elements = self.cursor.fetchall()

        self.cursor.close()

        # Part of this log is broken, but the change made is really more helpfull than this
        logger.log(100, f"FETCHED '{element_table_str}' ELEMENT USING '{query_str}' QUERY")
        
        return elements

    def __delete_element_by_id (self, element_table: str, element_id: str, id_config: dict) -> bool:
        element_table_str = self.db_tables[element_table]

        if id_config["min"] > len(str(element_id)) and len(str(element_id)) > id_config["max"]:
            raise sqlite3.OperationalError('ID LENGHT INCORRECT')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"DELETE FROM {element_table_str} WHERE {id_config['label']} = {element_id}")
        self.connection.commit()
        self.cursor.close()

        logger.log(100, f"DELETED '{element_table_str}' ELEMENT WITH ID '{element_id}'")
        return True

    def get_career_by_id (self, career_id: str, *columns_to_get: str) -> tuple([str, str, int]):
        career = self.__get_element_by_id(
            'careers',
            career_id,
            {
                "min": 4,
                "max": 16,
                "label": "Código_Carrera"
            },
            *columns_to_get
        )

        if not career:
            raise sqlite3.DataError(f"CAREER WITH ID '{career_id}' NOT FOUND")

        return career
                       
    def get_careers (self, filters: dict={}, *columns_to_get: str) -> list(tuple([str, str, int])):
        if (len(filters.keys()) == 0):
            careers = self.__get_all_elements('careers', *columns_to_get)

            if len(careers) <= 0:
                raise sqlite3.DataError('NO CAREERS AVAILABLE')

            return careers
        
        careers = self.__get_elements_with_query('careers', *columns_to_get, **filters)

        if len(careers) <= 0:
            raise sqlite3.DataError(f"NO CAREERS AVAILABLE WITH QUERY: {filters}")
        
        return careers

    def delete_career_by_id (self, career_id: str) -> bool:
        career_deleted = self.__delete_element_by_id(
            'careers',
            career_id,
            {
                "min": 4,
                "max": 16,
                "label": "Código_Carrera"
            }
        )

        if not career_deleted:
            raise sqlite3.DataError(f"ERROR DELETING CAREER WITH ID '{career_id}'")

        return True

    def get_student_by_id (self, student_id: str, *columns_to_get: str) -> tuple([str, str, str, str, str, str, str, str, str, str]):
        student = self.__get_element_by_id(
            'students',
            student_id,
            {
                "min": 16,
                "max": 16,
                "label": "id_alumno"
            },
            *columns_to_get 
        )

        if not student:
            raise sqlite3.dataerror(f"STUDENT WITH ID '{student_id}' NOT FOUND")

        return student

    def get_students (self, filters: dict={}, *columns_to_get: str) -> list(tuple([str, str, str, str, str, str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            students = self.__get_all_elements('students', *columns_to_get)

            if len(students) <= 0:
                raise sqlite3.DataError('NO STUDENTS AVAILABLE')

            return students

        students = self.__get_elements_with_query('students', *columns_to_get, **filters)

        if len(students) <= 0:
            raise sqlite3.DataError(f"NO STUDENTS AVAILABLE WITH QUERY: {filters}")

        return students

    def delete_student_by_id (self, student_id: str) -> bool:
        student_deleted = self.__delete_element_by_id(
            'students',
            student_id,
            {
                "min": 16,
                "max": 16,
                "label": "id_alumno"
            }
        )

        if not student_deleted:
            raise sqlite3.dataerror(f"ERROR DELETING STUDENT WITH ID: {student_id}")

        return True
    
    def get_course_by_id (self, course_id: str, *columns_to_get: str) -> tuple([str, str, str, int]):
        course = self.__get_element_by_id(
            'courses',
            course_id,
            {
                "min": 7,
                "max": 7,
                "label": "Código_Curso"
            },
            *columns_to_get
        )

        if not course:
            raise sqlite3.DataError(f"COURSE WITH ID '{course_id}' NOT FOUND")

        return course

    def get_courses (self, filters: dict={}, *columns_to_get: str) -> list(tuple([str, str, str, int])):
        if (len(filters.keys()) == 0):
            courses = self.__get_all_elements('courses', *columns_to_get)

            if len(courses) <= 0:
                raise sqlite3.DataError('NO COURSES AVAILABLE')

            return courses

        courses = self.__get_elements_with_query('courses', *columns_to_get, **filters)

        if len(courses) <= 0:
            raise sqlite3.DataError(f"NO COURSES AVAILABLE WITH QUERY: {filters}")

        return courses

    def delete_course_by_id (self, course_id: str) -> bool:
        course_deleted = self.__delete_element_by_id(
            'courses',
            course_id,
            {
                "min": 7,
                "max": 7,
                "label": "Código_Curso"
            }
        )

        if not course_deleted:
            raise sqlite3.DataError(f"ERROR DELETING COURSE WITH ID '{course_id}'")

        return True

    def get_record_by_id (self, record_id: str, *columns_to_get) -> tuple([str, str, str, str, str]):
        record = self.__get_element_by_id(
            'records',
            record_id,
            {
                "min": 16,
                "max": 16,
                "label": "No_Inscripción"
            },
            *columns_to_get
        )

        if not record:
            raise sqlite3.DataError(f"RECORD WITH ID '{record_id}' NOT FOUND")

        return record

    def get_records (self, filters: dict={}, *columns_to_get) -> list(tuple([str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            records = self.__get_all_elements('records', *columns_to_get)

            if len(records) <= 0:
                raise sqlite3.DataError('NO RECORDS AVAILABLE')

            return records

        records = self.__get_elements_with_query('records', *columns_to_get, **filters)

        if len(records) <= 0:
            raise sqlite3.DataError(f"NO RECORDS AVAILABLE WITH QUERY: {filters}")

        return records

    def delete_record_by_id (self, record_id: str) -> bool:
        record_deleted = self.__delete_element_by_id(
            'records',
            record_id,
            {
                "min": 16,
                "max": 16,
                "label": "No_Inscripción"
            }
        )

        if not record_deleted:
            raise sqlite3.DataError(f"ERROR DELETING RECORD WITH ID '{record_id}'")

        return record_deleted

    def set_inscripcion(self, record: int, student_id: str, course_code: str, inscripcion_date: str, course_schedule: str):
        self.cursor = self.connection.cursor()

        query = "INSERT INTO Inscritos (No_inscripción, Id_Alumno, Código_Curso, Horario, Fecha_Inscripción) VALUES (?, ?, ?, ?, ?)"
        new_record_data = (record, student_id, course_code, course_schedule, inscripcion_date)
        self.cursor.execute(query, new_record_data)

        self.connection.commit()
        self.cursor.close()
        return

    ## autocompleta el nombre yy el apellido esta conectado al combobox
    def autocompletar_nombre(self,event):
        student_id = self.cmbx_Id_Alumno.get()
        no_inscripcion = self.no_registro_estudiante(student_id)
        datos = self.get_student_by_id(student_id)
        nombres_Alu= datos[3]
        apellidos_Alu = datos[2]
        ##modificamos los entry de nombres y apellidos
        self.apellido_Alumno.set(nombres_Alu)
        self.nombre_Alumno.set(apellidos_Alu)
        self.num_InscripcionVar.set(no_inscripcion)

    def _format_record_schedule (self, record_tuple):
        """
            Procesa los días y horarios como strings con el siguiente formato:
                Para los días:
                    MTWHFSU
                    M -> Lunes
                    T -> Martes
                    W -> Miercoles
                    H -> Jueves
                    F -> Viernes
                    S -> Sábado
                    U -> Domingo
            Y sus horarios como 11-13 -> inicia a las 11 y termina a las 13 (Hora 24h)
            
            Ejemplo: 
                TH;11-13 -> Martes y Jueves de 11 a 13

            *Si se cuenta con que tenga clases en diferentes horas, ejemplo
            *martes de 7-9 y jueves de 11-13
            *ESTE FORMATO NO FUNCIONA, toca actualizarlo
        """
        record = list(record_tuple)
        days_raw, hours_raw = record[3].split(';') # 3rd index is 'Horario'
        days_str = ''
        hours_str = ''

        # processing days
        for i, day in enumerate(days_raw):
            if (day not in self.days_labels.keys()):
                raise KeyError("DAY NOT AVAILABLE")

            if (0 < i < len(days_raw) - 1):
                days_str += ', '
            elif (i == len(days_raw) - 1):
                days_str += ' y '

            days_str += self.days_labels[day]

        # processing horas
        start_hour, finish_hour = hours_raw.split("-")
        hours_str = start_hour + ' a ' + finish_hour

        record[3] = days_str + ' de ' + hours_str # 3rd index is 'Horario'
        return record

    def open_schedule_dialog (self, return_variable):
        """
            Abre un Toplevel donde se puede elegir el horario,
            se ingresa los días y horas del horario para poder generarlo.
            Lanza errores no-fatales al usuario si no se cuenta con días o horas validas.
            Retorna en 'return_variable' el resultado de la generación en formato de horario.
        """

        # Functions inside the schedule_dialog so the main class doesn't have to 
        # keep the dialog logic

        def get_days_schedule ():
            days_str = ""

            for i, day in enumerate(days_list):
                if not day["var"].get():
                    continue

                days_str += day["value"]

            if not days_str:
                messagebox.showerror("Error", "Tiene que elegir al menos un día para el horario")

            return days_str

        def get_hours_schedule ():
            hours_str = ""
            start_hour = start_hour_entry.get()
            end_hour = end_hour_entry.get()

            

            if not self.validate_hour(start_hour):
                messagebox.showerror("Error", "El formato de la fecha inicial del horario esta mal")
                return hours_str

            if not self.validate_hour(end_hour):
                messagebox.showerror("Error", "El formato de la fecha final del horario esta mal")
                return hours_str
            
            else:
                inicial = int(start_hour.replace(":", ""))
                final = int(end_hour.replace(":", ""))

                if int(start_hour[3:5]) > 59:
                    messagebox.showerror("Error", "La hora solo tiene 59 minutos")
                    return
                
                elif int(end_hour[3:5]) > 59:
                    messagebox.showerror("Error", "La hora solo tiene 59 minutos")
                    return

                elif inicial > 2359:
                    messagebox.showerror("Error", "La hora no puede ser mayor a 23:59")
                    return
    
                elif final > 2359:
                    messagebox.showerror("Error", "La hora no puede ser mayor a 23:59")
                    return
    
                elif inicial > final:
                    messagebox.showerror("Error", "La hora inicial no puede ser mayor a la hora final (hora militar)")
                    return
                
                elif inicial == final:
                    messagebox.showerror("Error", "La hora inicial no puede ser igual a la hora final")
                    return


            hours_str = start_hour + '-' + end_hour
            return hours_str

        def generate_schedule ():
            schedule_str = ""
            hours_str = ""
            days_str = ""

            days_str = get_days_schedule()
            if not days_str:
                return 

            hours_str = get_hours_schedule()
            if not hours_str:
                return

            schedule_str += days_str + ';' + hours_str
            return_variable.set(schedule_str)
            self.close_schedule_dialog()
            return

        if self.current_action == self.available_actions[4]:
            return

        self.current_action = self.available_actions[4]
        self.__highlight_btns([])
        
        self.schedule_dialog = tk.Toplevel(pady=32)
        self.schedule_dialog.geometry(self.centrarVentana(550,300))
        self.schedule_dialog.resizable(False,False)
        
        self.schedule_dialog.title("Generar Horario de Inscripción")
        self.schedule_dialog.protocol("WM_DELETE_WINDOW", self.close_schedule_dialog)

        days_list = [
            { "text": "Lunes", "value": "M", "var": tk.BooleanVar(self.schedule_dialog, name="monday", value=False)},
            { "text": "Martes", "value": "T", "var": tk.BooleanVar(self.schedule_dialog, name="tuesday", value=False)},
            { "text": "Miércoles", "value": "W", "var": tk.BooleanVar(self.schedule_dialog, name="wednesday", value=False)},
            { "text": "Jueves", "value": "H", "var": tk.BooleanVar(self.schedule_dialog, name="thursday", value=False)},
            { "text": "Viernes", "value": "F", "var": tk.BooleanVar(self.schedule_dialog, name="friday", value=False)},
            { "text": "Sábado", "value": "S", "var": tk.BooleanVar(self.schedule_dialog, name="saturday", value=False)},
            { "text": "Domingo", "value": "U", "var": tk.BooleanVar(self.schedule_dialog, name="sunday", value=False)},
        ]

        label_days = tk.Label(self.schedule_dialog, text="Días del horario")
        label_days.pack(
            anchor="w",
            ipadx=32,
            ipady=8
        )
        frame_days = tk.Frame(
            self.schedule_dialog,
            padx=32,
            pady=8
        )
        frame_days.pack(anchor="w")

        for day in days_list:
            dayCheck = ttk.Checkbutton(
                frame_days,
                text=day["text"],
                variable=day["var"]
            )
            dayCheck.pack(
                anchor="w",
                side="left",
                fill="none"
            )

        label_hours = tk.Label(self.schedule_dialog, text="Hora del horario")
        label_hours.pack(
            anchor="w",
            ipadx=32,
            ipady=8
        )
        frame_hours = tk.Frame(
            self.schedule_dialog,
            padx=32,
            pady=8
        )
        frame_hours.pack(anchor="center", side="top")

        start_hour_label = tk.Label(frame_hours, text="Inicio: ", justify="left")
        start_hour_label.pack(anchor="center", side="left")
        start_hour_entry = tk.Entry(frame_hours, width=5)
        start_hour_entry.pack(anchor="center", side="left", padx=8)

        end_hour_label = tk.Label(frame_hours, text="Fin: ", justify="left")
        end_hour_label.pack(anchor="center", side="left")
        end_hour_entry = tk.Entry(frame_hours, width=5)
        end_hour_entry.pack(anchor="center", side="left", padx=8)

        frame_generate_btns = tk.Frame(
            self.schedule_dialog,
            padx=64,
            pady=8
        )
        frame_generate_btns.pack(anchor="center", side="bottom")
        generate_btn = tk.Button(frame_generate_btns, text="Generar Horario", command=generate_schedule)
        generate_btn.pack(anchor="center", side="left", padx=16)
        cancel_btn = tk.Button(frame_generate_btns, text="Cancelar", command=self.close_schedule_dialog)
        cancel_btn.pack(anchor="center", side="left", padx=16)
        
        return

    def close_schedule_dialog (self):
        self.current_action = ""
        self.__highlight_btns(self.btn_names)

        self.schedule_dialog.destroy()
        del self.schedule_dialog
        return

    def idcbox (self):
        students_ids = self.get_students({}, "Id_Alumno")
        students_ids = [ids[0] for ids in students_ids ]
        return students_ids
    
    def cursosbox(self):
        courses_names = self.get_courses({}, 'Descripción_Curso')
        courses_names = [curso[0] for curso in courses_names]
        return courses_names

    def add_records_to_treeview (self, record_filter={}) -> None:
        treeview_records = self.tView.get_children()
        for record in treeview_records:
            self.tView.delete(record)
        
        try:
            records = self.get_records(filters=record_filter)

            for i, record in enumerate(records):
                record = self._format_record_schedule(record)

                self.tView.insert(
                    "",
                    'end',
                    values=record
                )
        except sqlite3.DataError as err:
            self.tView.insert(
                "",
                0,
                'end',
                text="Actualmente",
                values=("no"," hay", "ningún", "registro")
            )

        return
    
    def autocompletar_datos_Curso(self,event):
        course_name = self.cmbx_Cursos.get()
        course_data = self.get_courses({"Descripción_Curso": course_name}, "Código_Curso")[0]
        self.valor_id.set(course_data[0])
        return

    def __highlight_btns (self, buttons_to_highlight):
        for btn_name in self.btn_names:
            btn = self.frm_1.nametowidget(btn_name)
            btn["state"] = "disabled"

            if btn_name in buttons_to_highlight:
                btn["state"] = "normal"
        

    def __get_selected_records (self):
        rows_id = self.tView.selection()
        records_data = []

        for row in rows_id:
            records_data.append(self.tView.item(row)['values'])

        return records_data

    def grabar_inscripcion(self):
    
        id_estudiante = self.cmbx_Id_Alumno.get()
        if not id_estudiante:
            messagebox.showerror("Error","Por favor selecciona un ID de algún Alumno")
            return 
        cod_curso = self.valor_id.get()
        nom_curso = self.cmbx_Cursos.get()
        if not cod_curso or not nom_curso:
            messagebox.showerror("Error","Por favor selecciona un curso")
            return
        fecha = self.fecha_value.get()
        if not fecha:
            messagebox.showerror("Error","Digite una fecha")
            return
        if not self.validar_fecha():
            messagebox.showerror("Error", "Por favor digita correctamente la fecha del registro")
            return

        horario_curso = self.horario.get()
        if not horario_curso:
            messagebox.showerror("Error", "Por favor ingrese el horario del curso a inscribir")
            return
        
        registro = self.num_InscripcionVar.get()
        curso_Existe = self.revisar_curso(id_estudiante, cod_curso)
        if curso_Existe == True:
            messagebox.showerror("Error","El alumno ya esta tomando este curso")
            return
    

        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Id_Alumno FROM Inscritos")
        inscritos = self.cursor.fetchall()
        self.cursor.close()
        inscritos_ids = [inscrito[0] for inscrito in inscritos]
        print(inscritos_ids)
        if id_estudiante not in inscritos_ids:
            self.variable += 1

        self.set_inscripcion(registro, id_estudiante, cod_curso, fecha, horario_curso)
        self.add_records_to_treeview()    
      

        messagebox.showinfo("Completado","La inscripción se guardo con exito")

        return
    
    def autocompletar_treeview(self, event):
        try:
            elmo = self.__get_selected_records()[0]
            registro = elmo[0]
            id_estudiante = str(elmo[1])
            id_curso = str(elmo[2])
            fecha = str(elmo[4])
            curso = self.get_course_by_id(id_curso, 'Descripción_Curso')
            nombre = self.get_student_by_id(id_estudiante, 'Nombres')
            apellido = self.get_student_by_id(id_estudiante, 'Apellidos')
            self.cursor= self.connection.cursor()
            self.cursor.execute("SELECT Horario FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?", (id_estudiante, id_curso))
            horario = self.cursor.fetchone()[0]
            self.cursor.close()
    
            self.cmbx_Id_Alumno.set(id_estudiante)
            self.nombre_Alumno.set(nombre)
            self.apellido_Alumno.set(apellido)
            self.cmbx_Cursos.set(curso[0])
            self.schedule_variable.set(horario)
            self.valor_id.set(id_curso)
            self.fecha_value.set(fecha)
            self.num_InscripcionVar.set(registro)
        except:
            pass
    
    def control_errores_edicion(self):
            
        id_Alumno = self.cmbx_Id_Alumno.get() 
        id_Curso = self.valor_id.get()
        horario = self.horario.get()
        fecha = self.fecha_value.get()

        try:
            self.cursor= self.connection.cursor()
            self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?", (id_Alumno,))
            no_Registro = self.cursor.fetchone()[0]   
            self.cursor.close()
        
            try:
                existe = self.revisar_horario(id_Alumno, id_Curso, horario)
                if existe == True:
                    messagebox.showerror("Error", "Ese alumno ya esta viendo ese curso en ese horario.") 
                    return 
                else:
                    self.distinto_horario(id_Alumno, id_Curso, fecha, horario)
                    return         
            except:     
                pass
            if not id_Curso:
                messagebox.showerror("Error", "Por favor, seleccione un curso.")
            elif not id_Alumno:
                messagebox.showerror("Error", "Por favor, ingrese el Id del alumno.") 
            elif not horario:
                messagebox.showerror("Error", "Por favor, ingrese el horario.")
            elif not fecha:
                messagebox.showerror("Error", "Por favor, ingrese la fecha.") 
            else:
                self.opciones_edicion(no_Registro, id_Alumno, id_Curso, fecha, horario) 
        except:
            messagebox.showerror("Error", "Ese alumno aun no esta registrado") 

    def distinto_horario(self, id_Alumno, id_Curso, fecha, horario):
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Horario FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?", (id_Alumno, id_Curso))
        horario_Actual = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE Id_Alumno = ?", (id_Alumno,))
        materias = self.cursor.fetchall()
        self.cursor.close()
    
        for materia in materias:   
            if id_Curso == materia[0] and horario_Actual != horario:
               self.cursor= self.connection.cursor()
               self.cursor.execute("UPDATE Inscritos SET Fecha_Inscripción = ?, Horario = ? WHERE Id_Alumno = ? AND Horario = ? AND Código_Curso = ?",(fecha, horario, id_Alumno, horario_Actual, id_Curso))
               self.connection.commit()
               self.cursor.close()
               self.add_records_to_treeview()
               messagebox.showinfo("Exito", "Datos actualizados correctamente")   

    def opciones_edicion(self, No_inscripción: int, student_id: str, course_code: str, inscripcion_date: str, horario: str):

        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(student_id,))
        cantidad_Registro = len(self.cursor.fetchall())      
        self.connection.commit()
        self.cursor.close()  
        if cantidad_Registro > 1:
            self.ventana_varios_cursos(No_inscripción)
        else:  
            self.editar_inscripcion(No_inscripción, student_id, course_code, inscripcion_date, horario)
        

    def revisar_curso(self,student_id: int, course_code: str):
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE Id_Alumno = ?",(student_id,))
        cursos = self.cursor.fetchall()      
        self.cursor.close() 
        for curso in cursos:     
            if course_code in curso:
                return True
    
    def revisar_horario(self,student_id: int, course_code: str, horario: str):
        curso_Existe = self.revisar_curso(student_id,course_code)
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Horario FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?",(student_id, course_code))
        horario_Actual = self.cursor.fetchone()  
        self.cursor.close() 
        if horario_Actual[0] == horario and curso_Existe == True:
            return True
        
    def editar_inscripcion(self, No_inscripción: int, student_id: str, course_code: str, inscripcion_date: str, horario: str):
        self.cursor= self.connection.cursor()
        self.cursor.execute("UPDATE Inscritos SET Id_Alumno = ?, Código_Curso = ?, Fecha_Inscripción = ?, Horario = ? WHERE No_Inscripción = ?",(student_id, course_code, inscripcion_date, horario,No_inscripción)) 
        self.connection.commit()
        self.cursor.close()
        self.add_records_to_treeview()
        messagebox.showinfo("Exito", "Datos actualizados correctamente")    

    def editar_inscripción_cursos(self):
        id_Alumno = self.cmbx_Id_Alumno.get() 
        id_Curso = self.valor_id.get()
        horario = self.horario.get()
        fecha = self.fecha_value.get()
        curso_Actual = self.codigo.get()
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(id_Alumno,))
        no_Registro = self.cursor.fetchone()[0]       
        self.connection.commit()
        self.cursor.close()  
        
        self.cursor= self.connection.cursor()
        self.cursor.execute("UPDATE Inscritos SET Id_Alumno = ?, Código_Curso = ?, Fecha_Inscripción = ?, Horario = ? WHERE No_inscripción = ? AND Código_Curso = ?",(id_Alumno, id_Curso, fecha, horario, no_Registro, curso_Actual))
        self.connection.commit()
        self.cursor.close()
        self.add_records_to_treeview()  
        self.habilitar()
        messagebox.showinfo("Exito", "Datos actualizados correctamente")

    def habilitar(self):
        self.__highlight_btns(self.btn_names)
        self.mini.destroy()
        
    
    def ventana_varios_cursos(self,no_Registro):
        self.__highlight_btns([])  
        self.mini = tk.Toplevel()
        self.mini.resizable(False,False)
        self.mini.title("Edición de datos")
        self.mini.configure(background="#2271b3")
        self.mini.geometry(self.centrarVentana(425,115))
        self.mini.protocol("WM_DELETE_WINDOW", self.habilitar) 

        #Label Aviso
        self.lblinfo = ttk.Label(self.mini, name="lblinfo")
        self.lblinfo.configure(background="#bfcde6", text='Seleccione el curso que desea reemplazar')
        self.lblinfo.place(anchor="nw", x=97, y=12)

        #Label Codigo_curso
        self.lblcodigo = ttk.Label(self.mini, name="lblcodigo")
        self.lblcodigo.configure(background="#bfcde6", text='Código del curso:')
        self.lblcodigo.place(anchor="nw", x=20, y=45)

        #Entry Codigo_curso
        self.codigo= ttk.Combobox(self.mini, name="curse", values=self.codebox(no_Registro),state="readonly")
        self.codigo.place(anchor="nw", width=140, x=150, y=44)
        self.codigo.bind("<<ComboboxSelected>>", self.autocompletar_curso_mini)
        
        #Label Curso
        self.lblcurso = ttk.Label(self.mini, name="lblcurso")
        self.lblcurso.configure(background="#bfcde6", text='Nombre del codigo:')
        self.lblcurso.place(anchor="nw", x=20, y=75)

        #Entry Curso
        self.cursotxt = tk.StringVar()
        self.curso = ttk.Entry(self.mini, name="name", textvariable= self.cursotxt)
        self.curso.configure(justify="center")
        self.curso.place(anchor="nw", width=140, x=150, y=74)

        #Botones
        guardar = ttk.Button(self.mini, text="Guardar", command= self.editar_inscripción_cursos)
        guardar.place(anchor="nw", width=90, x=315, y=43)

        cerrar = ttk.Button(self.mini,text="Cerrar",command = self.habilitar)
        cerrar.place(anchor="nw", width=90, x=315,y=73)

    def autocompletar_curso_mini(self,event):
        self.cursor = self.connection.cursor()
        entry = self.codigo.get()
        self.cursor.execute("SELECT Descripción_Curso FROM Cursos WHERE Código_Curso = ?",(entry,))
        codigo = self.cursor.fetchone()
        self.cursor.close()
        curso = codigo[0]
        self.cursotxt.set(curso)
        return

    def codebox(self,no_Registro):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE No_inscripción = ?",(no_Registro,))
        codigos = self.cursor.fetchall()
        self.cursor.close()
        curso = [curso[0] for curso in codigos]
        return curso
        
    def handle_delete_records (self):
        
        records_selected = self.__get_selected_records()

        if self.current_action == self.available_actions[3] and len(records_selected) > 0:
            return self.delete_records_by_selection(records_selected, no_dialog=True)

        if len(records_selected) <= 0:
            return self.delete_records_by_action()
        else:
            return self.delete_records_by_selection(records_selected)
        

    def delete_records_by_selection (self, records_selected, no_dialog=False):
        if not no_dialog:
            dialog_msg = "¿Esta seguro de eliminar %s?"

            if len(records_selected) > 1:
                dialog_msg = dialog_msg % "los registros seleccionados"
            else:
                dialog_msg = dialog_msg % "el registro seleccionado"

            if not messagebox.askokcancel("Eliminar Inscripciones", dialog_msg):
                return

        for record in records_selected:
            self.delete_record_by_id(record[0])

        self.add_records_to_treeview()
        self.cancel_Record()
        return

    def delete_records_by_action (self):
        self.__highlight_btns((self.btn_names[3], self.btn_names[4]))
        self.current_action = self.available_actions[3]
        self.cancel_Record()
        
    def close_consulta(self):
        self.__highlight_btns(self.btn_names)
        self.ventanaConsulta.destroy()
        

    def abrir_consulta(self):
        self.__highlight_btns([])  
        self.ventanaConsulta = tk.Toplevel(self.win)
        self.ventanaConsulta.title("Consulta")
        self.ventanaConsulta.resizable(False, False)
        self.ventanaConsulta.geometry("300x300")  
        self.ventanaConsulta.update_idletasks()
        width = self.ventanaConsulta.winfo_width()
        height = self.ventanaConsulta.winfo_height()
        x = (self.win.winfo_screenwidth() - width) // 2
        y = (self.win.winfo_screenheight() - height) // 2
        self.ventanaConsulta.geometry(f"{width}x{height}+{x}+{y}")
        self.ventanaConsulta.protocol("WM_DELETE_WINDOW", self.close_consulta)

        self.frame_estudiante = tk.Frame(self.ventanaConsulta)
        self.frame_estudiante.pack(padx=10, pady=10)
        label_estudiante = tk.Label(self.frame_estudiante, text="Seleccionar estudiante:")
        label_estudiante.pack(side="left")
        self.combo_estudiantes = ttk.Combobox(self.frame_estudiante, values=self.idcbox(), state="readonly")
        self.combo_estudiantes.pack(side="left")

        self.frame_curso = tk.Frame(self.ventanaConsulta)
        self.frame_curso.pack(padx=10, pady=10)
        label_curso = tk.Label(self.frame_curso, text="Seleccionar curso:")
        label_curso.pack(side="left")
        self.combo_cursos = ttk.Combobox(self.frame_curso, values=self.cursosbox(), state="readonly")
        self.combo_cursos.pack(side="left")

        self.frame_treeview = tk.Frame(self.ventanaConsulta)
        self.frame_treeview.pack(padx=10, pady=10, fill="both", expand=True)
        self.treeview_consulta = ttk.Treeview(self.frame_treeview, columns=("columna1","columna2"), show="headings")
        self.treeview_consulta.heading("columna1", text="Datos de la Consulta")
        self.treeview_consulta.pack(side="left", fill="both", expand=True)
        self.combo_estudiantes.bind("<<ComboboxSelected>>", self.consultar_cursos_del_estudiante)
        self.combo_cursos.bind("<<ComboboxSelected>>", self.consultar_estudiantes_del_curso)

    def consultar_cursos_del_estudiante(self, event):
        self.treeview_consulta.delete(*self.treeview_consulta.get_children())  
        self.cursor = self.connection.cursor()
        id_Alumno = self.combo_estudiantes.get()
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE Id_Alumno = ?", (id_Alumno,))
        id_Cursos = self.cursor.fetchall()
        self.cursor.close()
        for id_Curso in id_Cursos:
            codigo_curso = id_Curso[0]  
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT Descripción_Curso FROM Cursos WHERE Código_Curso = ?", (codigo_curso,))
            descripcion_curso = self.cursor.fetchone()
            self.treeview_consulta.insert("", "end", values=descripcion_curso)
            self.cursor.close()

    def consultar_estudiantes_del_curso(self, event):
        self.treeview_consulta.delete(*self.treeview_consulta.get_children()) 
        self.cursor = self.connection.cursor()
        id_Curso = self.combo_cursos.get()
        self.cursor.execute("SELECT Código_Curso FROM Cursos WHERE Descripción_Curso = ?", (id_Curso,))
        codigo_curso = self.cursor.fetchone()[0]
        self.cursor.execute("Select Id_Alumno FROM Inscritos WHERE Código_Curso = ?", (codigo_curso,))
        id_Alumnos = self.cursor.fetchall()
        self.cursor.close()
        for id_Alumno in id_Alumnos:
            id_alumno = id_Alumno[0]  
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno = ?", (id_alumno,))
            alumnos = self.cursor.fetchone()
            self.treeview_consulta.insert("", "end", values=alumnos)
            self.cursor.close()


if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
    