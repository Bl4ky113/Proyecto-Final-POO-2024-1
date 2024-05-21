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
    db_Path = "./db/Inscripciones.db"
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    db_Tables = {
        "careers": "Carreras",
        "students": "Alumnos",
        "courses": "Cursos",
        "records": "Inscritos"
    }

    # Schedule constants
    days_Labels = {
        "M": "Lunes",
        "T": "Martes",
        "W": "Miércoles",
        "H": "Jueves",
        "F": "Viernes",
        "S": "Sábado",
        "U": "Domingo"
    }

    # Tk Constants
    btn_Names = (
        "btnConsultar",
        "btnGuardar",
        "btnEditar",
        "btnEliminar",
    )

    current_Action = ""
    available_Actions = (
        "query",
        "save",
        "edit",
        "delete",
        "dialog-open"
    )

    
    def __init__(self, master=None):
        self.config_Db()
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
        file_Path = os.path.dirname(os.path.abspath(__file__))
        imagen_Path = os.path.join(file_Path,'img','icono.png')
        self.win.iconphoto(True,tk.PhotoImage(file=imagen_Path))

        self.win.geometry(self.centrar_Ventana(800,600))
        
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
        self.lbl__No_Inscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lbl__No_Inscripcion.configure(
            background=None,
            font="{Arial} 11 {bold}",
            justify="left",
            state="normal",
            takefocus=False,
            text='No.Inscripción'
        )

        # Label No. Inscripción
        self.lbl__No_Inscripcion.place(
            anchor="nw",
            x=680,
            y=20
        )

        #Entry No. Inscripción
        self.num_Inscripcion_Var = tk.IntVar(value=self.numero_De_Registro())
        self.num_Inscripcion = ttk.Label(self.frm_1, textvariable = self.num_Inscripcion_Var ,  name="num_Inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=50, x=700, y=45)
        
        
        #Label Fecha
        
        self.lbl_Fecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lbl_Fecha.configure(background="#f7f9fd", text='Fecha:',foreground="#21618C")
        self.lbl_Fecha.place(anchor="nw", x=630, y=80)

        #Entry Fecha
        self.fecha_Value= tk.StringVar()
        self.fecha = ttk.Entry(self.frm_1, name="fecha",textvariable=self.fecha_Value)
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        self.fecha.bind("<KeyRelease>", self.autocompletar_Slash)

        #Label Alumno
        self.lbl_IdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lbl_IdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lbl_IdAlumno.place(anchor="nw", x=20, y=80)

        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_Id_alumno", values=self.idcbox(),state="readonly")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.autocompletar_Nombre )

        #Label Alumno
        self.lbl_Nombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lbl_Nombres.configure(text='Nombre(s):')
        self.lbl_Nombres.place(anchor="nw", x=20, y=130)

        #Entry Alumno
        self.nombre_Alumno= tk.StringVar()
        self.nombres = ttk.Entry(self.frm_1, name="nombres",textvariable=self.nombre_Alumno)
        self.nombres.place(anchor="nw", width=200, x=100, y=130)

        #Label Apellidos
        self.lbl_Apellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lbl_Apellidos.configure(text='Apellido(s):')
        self.lbl_Apellidos.place(anchor="nw", x=400, y=130)

        #Entry Apellidos
        self.apellido_Alumno = tk.StringVar()
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos", textvariable=self.apellido_Alumno)
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)

        #Label Curso
        self.lbl_IdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lbl_IdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lbl_IdCurso.place(anchor="nw", x=20, y=185)

        #Entry Curso
        self.valor_Id= tk.StringVar()
        self.id_Curso = ttk.Entry(self.frm_1, name="id_Curso",textvariable=self.valor_Id)
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=185)

        #Label Descripción del Curso
        self.lbl_DscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lbl_DscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lbl_DscCurso.place(anchor="nw", x=275, y=185)

        #Entry de Descripción del Curso 
        self.cmbx_Cursos = ttk.Combobox(self.frm_1,name="cmbx_Cursos",values=self.cursosbox(),state="readonly")
        self.cmbx_Cursos.place(anchor="nw", width=300, x=325, y=185)
        self.cmbx_Cursos.bind("<<ComboboxSelected>>",self.autocompletar_Datos_Curso)

        #Label Horario
        self.lbl_Horario = ttk.Label(self.frm_1, name="label3")
        self.lbl_Horario.configure(background="#f7f9fd",state="normal",text='Horario:')
        self.lbl_Horario.place(anchor="nw", x=635, y=185)

        #Entry del Horario
        self.schedule_Variable = tk.StringVar()
        self.horario = ttk.Entry(
            self.frm_1,
            name="entry3",
            state="disabled",
            textvariable=self.schedule_Variable
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
        self.horario.bind("<Button-1>", lambda event: self.open_Schedule_Dialog(self.schedule_Variable))

        ''' Botones  de la Aplicación'''
        ## algo de color
        self.style= ttk.Style()
        self.style.configure('TButton', background='#85C1E9', foreground='black')

        #Boton Consultar
        self.btnConsultar= ttk.Button(self.frm_1, name=self.btn_Names[0], command=self.abrir_Consulta)
        self.btnConsultar.configure(text='Consultar')
        self.btnConsultar.place(anchor="nw",x=150,y=260)

        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name=self.btn_Names[1] ,command=self.grabar_Inscripcion)
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=250, y=260)
        
        #Botón Editar 
        self.btnEditar = ttk.Button(self.frm_1, name=self.btn_Names[2], command = self.control_Errores_Edicion)
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=350, y=260)

        #Botón Eliminar
        self.btnEliminar = ttk.Button(
            self.frm_1, 
            name=self.btn_Names[3],
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
        #self.tView.bind("<ButtonRelease-1>", self.autocompletar_Curso)
        #Columnas del Treeview
        tView_Cols = ['No_Inscripción', 'Id_Alumno','Código_Curso', 'Horario', 'Fecha_Inscripción']
        self.tView.configure(
            columns=tView_Cols,
            displaycolumns=tView_Cols,
            selectmode='extended',
            padding=10
        )
        
        self.tView.column("#0", width=0, stretch="no")
        self.tView.column(tView_Cols[0], anchor="w", width=50)
        self.tView.column(tView_Cols[1], anchor="w", width=100)
        self.tView.column(tView_Cols[2], anchor="w", width=100)
        self.tView.column(tView_Cols[3], anchor="w", width=200)
        self.tView.column(tView_Cols[4], anchor="w", width=100)
        #Cabeceras
        self.tView.heading("#0", text="")
        self.tView.heading(tView_Cols[0], anchor="w", text="# Inscripción")
        self.tView.heading(tView_Cols[1], anchor="w", text="Id Alumno")
        self.tView.heading(tView_Cols[2], anchor="w", text="Código Curso")
        self.tView.heading(tView_Cols[3], anchor="w", text="Horario")
        self.tView.heading(tView_Cols[4], anchor="w", text="Fecha Inscripción")
        self.add_Records_To_Treeview()
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=290)
        self.tView.bind('<<TreeviewSelect>>',self.autocompletar_Treeview)

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
            self.handle_Delete_Records()
            self.cancel_Record()
        except:
            messagebox.showerror("Error", "Por favor, seleccione un dato en el Treeview para eliminar.")
        
        
    def inicial(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT MAX(No_Inscripción) FROM Inscritos")
        resultado = self.cursor.fetchone()
        self.cursor.close()
        if resultado[0] is not None:
            self.variable = int(resultado[0])
        else:
            self.variable = 0

    def centrar_Ventana(self,w_Ventana,h_Ventana):
        x_Ventana = self.win.winfo_screenwidth() // 2 - w_Ventana // 2
        y_Ventana = self.win.winfo_screenheight() // 2 - h_Ventana // 2
        centrado=str(w_Ventana) + "x" + str(h_Ventana) + "+" + str(x_Ventana) + "+" + str(y_Ventana)
        return centrado
    
    def validar_Fecha(self):
        fecha_Ingresada = self.fecha.get()
        formato_Valido = re.match(r'\d{2}/\d{2}/\d{4}', fecha_Ingresada)
        if formato_Valido:
            dia, mes, anio = map(int, fecha_Ingresada.split('/'))
            try:
                calendar.datetime.datetime(anio, mes, dia)
                return True
            except ValueError:
                return False
        else:
            return False
        
    def autocompletar_Slash(self, event):
        fecha = self.fecha_Value.get()
        if len(fecha) == 2 or len(fecha) == 5:
            if fecha[-1] != '/':
                self.fecha_Value.set(fecha + '/')
                # Move cursor to the end of the entry
                self.fecha.icursor(len(self.fecha_Value.get()))
                      
    def validate_Hour (self, value):
        if re.fullmatch(r"\d{1,2}:\d\d", value) is None:
            return False
        
        return True

    def cancel_Record (self):
        # No action active 
        self.current_Action = "" 

        # highlight all btns
        self.__hightlight_Btns(self.btn_Names)

        # UnSelect all records in treeView
        self.tView.selection_remove(self.tView.selection())
        self.clear_Form()
        
        try:
            self.schedule_Dialog.destroy()
        except:
            pass

        try:
            self.mini.destroy()
        except:
            pass
        try:
            self.schedule_Dialog.destroy()
        except:
            pass
        try:
            self.ventana_Consulta.destroy()
        except:
            pass


    def clear_Form (self):
        self.num_Inscripcion_Var.set(self.numero_De_Registro())
        self.fecha_Value.set("")
        self.apellido_Alumno.set("")
        self.nombre_Alumno.set("")
        self.cmbx_Cursos.set("")
        self.valor_Id.set("")
        self.schedule_Variable.set("")
        self.cmbx_Id_Alumno.set("")
        return

    def numero_De_Registro(self):   
        id_Registro = self.variable + 1
        self.cursor.close()
        return id_Registro 
    
    
    def no_Registro_Estudiante(self, student_Id):    
        self.cursor = self.connection.cursor()  
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(student_Id,))
        id = self.cursor.fetchone()
        self.cursor.close()
        if id is not None:
            return id[0]
        else:
            return self.numero_De_Registro()
    
    def habilitar(self):
        self.__hightlight_Btns(self.btn_Names)
    
    def config_Db (self):
        self.connection = sqlite3.connect(self.db_Path)
        self.cursor = self.connection.cursor()

        self.create_Tables()
        return

    def create_Tables (self):
        seed_Done = False

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

            seed_Done = True

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
                    ("2016696", "Algoritmos", 56),
                    ("2016698", "Elementos de Computadores", 56),
                    ("2016707", "Sistemas Operativos", 56);
            ''')

            seed_Done = True

        self.cursor.execute('SELECT COUNT(*) FROM Alumnos')

        if self.cursor.fetchone()[0] <= 0:
            logger.log(100, "SEEDING DATA TO DB AT: Alumnos")
            self.cursor.execute('''
                INSERT INTO Alumnos
                    (Id_Alumno, Id_Carrera, Nombres, Apellidos, Fecha_Ingreso, Ciudad, Telef_Cel)
                VALUES
                    ("78560195", "2933", "Martín", "Hernández", "2023/08/01", "Bogotá", "1234567890"),
                    ("53990469", "2518", "Juan", "Morales", "2024/01/01", "Bogotá", "5432109876"),
                    ("17222022", "2879", "Andres", "hernandez", "2024/05/05", "Medellín", "0000000000"),
                    ("42742031", "2545", "Laura", "Moreno", "2023/08/01", "Fusagasugá", "1132432433"),
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

            seed_Done = True

        if seed_Done:
            self.connection.commit()

        self.cursor.close()

    def __generate_Columns_To_Get_String (self, table_Name: str, column_Name_List: typing.Iterable[str]) -> str:
        column_Name_Str = ""

        if (len(column_Name_List) <= 0):
            return "*" # ALL BY DEFAULT
        
        if (not self.__check_Only_Column_Names_In_List(table_Name, column_Name_List)):
            table_Name_Str = self.db_Tables[table_Name]
            raise sqlite3.OperationalError(f'COLUMN NAMES TO GET NOT AVAILABLE IN {table_Name_Str} TABLE')

        for i, column_Name in enumerate(column_Name_List):
            if i != 0 and i != len(column_Name_List):
                column_Name_Str += ', '

            column_Name_Str += column_Name

        return column_Name_Str

    def __check_Only_Column_Names_In_List (self, table_Name: str, column_Name_List: typing.Iterable[str]) -> bool:
        table_Name_Str = self.db_Tables[table_Name]

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT name FROM pragma_table_Info(?) as table_Info", (table_Name_Str, ))
        table_Columns = [column_Tuple[0] for column_Tuple in self.cursor.fetchall()]

        for column_Name in column_Name_List:
            if (column_Name not in table_Columns):
                logger.warning(f"FILTER '{column_Name}' NOT IN {table_Name_Str} SCHEMA")
                return False

        return True

    def __get_Element_By_Id (self, element_Table: str, element_Id, id_Config: dict, *columns_To_Get: str) -> tuple():
        element_Table_Str = self.db_Tables[element_Table]
        columns_To_Get_Str = self.__generate_Columns_To_Get_String(element_Table, columns_To_Get)

        if id_Config["min"] > len(element_Id) and len(element_Id) > id_Config["max"]:
            raise sqlite3.OperationalError('ID LENGHT INCORRECT')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_To_Get_Str} FROM {element_Table_Str} WHERE {id_Config['label']}=?", (element_Id, ))
        element = self.cursor.fetchone()

        self.cursor.close()

        logger.log(100, f"FETCHED '{element_Table_Str}' ELEMENT WITH ID '{element_Id}'")

        return element

    def __get_All_Elements (self, element_Table: str, *columns_To_Get: str) -> list(tuple()):
        element_Table_Str = self.db_Tables[element_Table]
        columns_To_Get_Str = self.__generate_Columns_To_Get_String(element_Table, columns_To_Get)

        if element_Table not in self.db_Tables.keys():
            raise sqlite3.DataError(f"ELEMENT TABLE: {element_Table} IS NOT A VALID TABLE")

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_To_Get_Str} FROM {element_Table_Str}")
        elements = self.cursor.fetchall()

        self.cursor.close()

        logger.log(100, f"FETCHED ALL '{element_Table_Str}' ELEMENTS")

        return elements

    def __get_Elements_With_Query (self, element_Table: str, *columns_To_Get: str, **filters) -> list(tuple()):
        element_Table_Str = self.db_Tables[element_Table]
        columns_To_Get_Str = self.__generate_Columns_To_Get_String(element_Table, columns_To_Get)
        query_Values = []
        query_Str = ''

        if len(filters.keys()) <= 0:
            raise sqlite3.OperationalError('NO FILTERS AVAILABLE')

        if not self.__check_Only_Column_Names_In_List(element_Table, filters.keys()):
            raise sqlite3.OperationalError(f'COLUMN NAMES TO FILTER NOT AVAILABLE IN {table_Name_Str} TABLE')
        
        for i, filter_Key in enumerate(filters.keys()):
            if i != 0:
                query_Str += " AND "

            filter_Value = filters[filter_Key]
            
            query_Str += f"\"{filter_Key}\"=?"
            query_Values.append(filter_Value)

        if not query_Str:
            raise sqlite3.OperationalError('NO VALID FILTERS PASSED IN QUERY')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT {columns_To_Get_Str} FROM {element_Table_Str} WHERE {query_Str}", query_Values)
        elements = self.cursor.fetchall()

        self.cursor.close()

        # Part of this log is broken, but the change made is really more helpfull than this
        logger.log(100, f"FETCHED '{element_Table_Str}' ELEMENT USING '{query_Str}' QUERY")
        
        return elements

    def __Delete_Element_By_Id (self, element_Table: str, element_Id: str, id_Config: dict) -> bool:
        element_Table_Str = self.db_Tables[element_Table]

        if id_Config["min"] > len(str(element_Id)) and len(str(element_Id)) > id_Config["max"]:
            raise sqlite3.OperationalError('ID LENGHT INCORRECT')

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"DELETE FROM {element_Table_Str} WHERE {id_Config['label']} = {element_Id}")
        self.connection.commit()
        self.cursor.close()

        logger.log(100, f"DELETED '{element_Table_Str}' ELEMENT WITH ID '{element_Id}'")
        return True

    def get_Career_By_Id (self, career_Id: str, *columns_To_Get: str) -> tuple([str, str, int]):
        career = self.__get_Element_By_Id(
            'careers',
            career_Id,
            {
                "min": 4,
                "max": 16,
                "label": "Código_Carrera"
            },
            *columns_To_Get
        )

        if not career:
            raise sqlite3.DataError(f"CAREER WITH ID '{career_Id}' NOT FOUND")

        return career
                       
    def get_Careers (self, filters: dict={}, *columns_To_Get: str) -> list(tuple([str, str, int])):
        if (len(filters.keys()) == 0):
            careers = self.__get_All_Elements('careers', *columns_To_Get)

            if len(careers) <= 0:
                raise sqlite3.DataError('NO CAREERS AVAILABLE')

            return careers
        
        careers = self.__get_Elements_With_Query('careers', *columns_To_Get, **filters)

        if len(careers) <= 0:
            raise sqlite3.DataError(f"NO CAREERS AVAILABLE WITH QUERY: {filters}")
        
        return careers

    def delete_Career_By_Id (self, career_Id: str) -> bool:
        career_Deleted = self.__Delete_Element_By_Id(
            'careers',
            career_Id,
            {
                "min": 4,
                "max": 16,
                "label": "Código_Carrera"
            }
        )

        if not career_Deleted:
            raise sqlite3.DataError(f"ERROR DELETING CAREER WITH ID '{career_Id}'")

        return True

    def get_Student_By_Id (self, student_Id: str, *columns_To_Get: str) -> tuple([str, str, str, str, str, str, str, str, str, str]):
        student = self.__get_Element_By_Id(
            'students',
            student_Id,
            {
                "min": 16,
                "max": 16,
                "label": "id_Alumno"
            },
            *columns_To_Get 
        )

        if not student:
            raise sqlite3.dataerror(f"STUDENT WITH ID '{student_Id}' NOT FOUND")

        return student

    def get_Students (self, filters: dict={}, *columns_To_Get: str) -> list(tuple([str, str, str, str, str, str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            students = self.__get_All_Elements('students', *columns_To_Get)

            if len(students) <= 0:
                raise sqlite3.DataError('NO STUDENTS AVAILABLE')

            return students

        students = self.__get_Elements_With_Query('students', *columns_To_Get, **filters)

        if len(students) <= 0:
            raise sqlite3.DataError(f"NO STUDENTS AVAILABLE WITH QUERY: {filters}")

        return students

    def delete_Student_By_Id (self, student_Id: str) -> bool:
        student_Deleted = self.__Delete_Element_By_Id(
            'students',
            student_Id,
            {
                "min": 16,
                "max": 16,
                "label": "id_Alumno"
            }
        )

        if not student_Deleted:
            raise sqlite3.dataerror(f"ERROR DELETING STUDENT WITH ID: {student_Id}")

        return True
    
    def get_Course_By_Id (self, course_Id: str, *columns_To_Get: str) -> tuple([str, str, str, int]):
        course = self.__get_Element_By_Id(
            'courses',
            course_Id,
            {
                "min": 7,
                "max": 7,
                "label": "Código_Curso"
            },
            *columns_To_Get
        )

        if not course:
            raise sqlite3.DataError(f"COURSE WITH ID '{course_Id}' NOT FOUND")

        return course

    def get_Courses (self, filters: dict={}, *columns_To_Get: str) -> list(tuple([str, str, str, int])):
        if (len(filters.keys()) == 0):
            courses = self.__get_All_Elements('courses', *columns_To_Get)

            if len(courses) <= 0:
                raise sqlite3.DataError('NO COURSES AVAILABLE')

            return courses

        courses = self.__get_Elements_With_Query('courses', *columns_To_Get, **filters)

        if len(courses) <= 0:
            raise sqlite3.DataError(f"NO COURSES AVAILABLE WITH QUERY: {filters}")

        return courses

    def delete_Course_By_Id (self, course_Id: str) -> bool:
        course_Deleted = self.__Delete_Element_By_Id(
            'courses',
            course_Id,
            {
                "min": 7,
                "max": 7,
                "label": "Código_Curso"
            }
        )

        if not course_Deleted:
            raise sqlite3.DataError(f"ERROR DELETING COURSE WITH ID '{course_Id}'")

        return True

    def get_Record_By_Id (self, record_Id: str, *columns_To_Get) -> tuple([str, str, str, str, str]):
        record = self.__get_Element_By_Id(
            'records',
            record_Id,
            {
                "min": 16,
                "max": 16,
                "label": "No_Inscripción"
            },
            *columns_To_Get
        )

        if not record:
            raise sqlite3.DataError(f"RECORD WITH ID '{record_Id}' NOT FOUND")

        return record

    def get_Records (self, filters: dict={}, *columns_To_Get) -> list(tuple([str, str, str, str, str])):
        if (len(filters.keys()) == 0):
            records = self.__get_All_Elements('records', *columns_To_Get)

            if len(records) <= 0:
                raise sqlite3.DataError('NO RECORDS AVAILABLE')

            return records

        records = self.__get_Elements_With_Query('records', *columns_To_Get, **filters)

        if len(records) <= 0:
            raise sqlite3.DataError(f"NO RECORDS AVAILABLE WITH QUERY: {filters}")

        return records

    def delete_Record_By_Id (self, record_Id: str) -> bool:
        record_Deleted = self.__Delete_Element_By_Id(
            'records',
            record_Id,
            {
                "min": 16,
                "max": 16,
                "label": "No_Inscripción"
            }
        )

        if not record_Deleted:
            raise sqlite3.DataError(f"ERROR DELETING RECORD WITH ID '{record_Id}'")

        return record_Deleted

    def set_Inscripcion(self, record: int, student_Id: str, course_Code: str, inscripcion_Date: str, course_Schedule: str):
        self.cursor = self.connection.cursor()

        query = "INSERT INTO Inscritos (No_Inscripción, Id_Alumno, Código_Curso, Horario, Fecha_Inscripción) VALUES (?, ?, ?, ?, ?)"
        new_Record_Data = (record, student_Id, course_Code, course_Schedule, inscripcion_Date)
        self.cursor.execute(query, new_Record_Data)

        self.connection.commit()
        self.cursor.close()
        return

    ## autocompleta el nombre yy el apellido esta conectado al combobox
    def autocompletar_Nombre(self,event):
        student_Id = self.cmbx_Id_Alumno.get()
        no_Inscripcion = self.no_Registro_Estudiante(student_Id)
        datos = self.get_Student_By_Id(student_Id)
        nombres_Alu= datos[3]
        apellidos_Alu = datos[2]
        ##modificamos los entry de nombres y apellidos
        self.apellido_Alumno.set(nombres_Alu)
        self.nombre_Alumno.set(apellidos_Alu)
        self.num_Inscripcion_Var.set(no_Inscripcion)

    def _format_Record_Schedule (self, record_Tuple):
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
        record = list(record_Tuple)
        days_Raw, hours_Raw = record[3].split(';') # 3rd index is 'Horario'
        days_Str = ''
        hours_Str = ''

        # processing days
        for i, day in enumerate(days_Raw):
            if (day not in self.days_Labels.keys()):
                raise KeyError("DAY NOT AVAILABLE")

            if (0 < i < len(days_Raw) - 1):
                days_Str += ', '
            elif (i == len(days_Raw) - 1):
                days_Str += ' y '

            days_Str += self.days_Labels[day]

        # processing horas
        start_Hour, finish_Hour = hours_Raw.split("-")
        hours_Str = start_Hour + ' a ' + finish_Hour

        record[3] = days_Str + ' de ' + hours_Str # 3rd index is 'Horario'
        return record

    def open_Schedule_Dialog (self, return_Variable):
        """
            Abre un Toplevel donde se puede elegir el horario,
            se ingresa los días y horas del horario para poder generarlo.
            Lanza errores no-fatales al usuario si no se cuenta con días o horas validas.
            Retorna en 'return_Variable' el resultado de la generación en formato de horario.
        """

        # Functions inside the schedule_Dialog so the main class doesn't have to 
        # keep the dialog logic

        def get_Days_Schedule ():
            days_Str = ""

            for i, day in enumerate(days_List):
                if not day["var"].get():
                    continue

                days_Str += day["value"]

            if not days_Str:
                messagebox.showerror("Error", "Tiene que elegir al menos un día para el horario.")

            return days_Str

        def get_Hours_Schedule ():
            hours_Str = ""
            start_Hour = start_Hour_Entry.get()
            end_Hour = end_Hour_Entry.get()

            if not self.validate_Hour(start_Hour):
                messagebox.showerror("Error", "El formato de la fecha inicial del horario esta mal.")
                return hours_Str

            if not self.validate_Hour(end_Hour):
                messagebox.showerror("Error", "El formato de la fecha final del horario esta mal.")
                return hours_Str
            
            else:
                inicial = int(start_Hour.replace(":", ""))
                final = int(end_Hour.replace(":", ""))

                if int(start_Hour[3:5]) > 59:
                    messagebox.showerror("Error", "La hora solo tiene 59 minutos.")
                    return
                
                elif int(end_Hour[3:5]) > 59:
                    messagebox.showerror("Error", "La hora solo tiene 59 minutos.")
                    return

                elif inicial > 2359:
                    messagebox.showerror("Error", "La hora inicial no puede ser mayor a 23:59.")
                    return
    
                elif final > 2359:
                    messagebox.showerror("Error", "La hora final no puede ser mayor a 23:59.")
                    return
    
                elif inicial > final:
                    messagebox.showerror("Error", "La hora inicial no puede ser mayor a la hora final (hora militar).")
                    return
                
                elif inicial == final:
                    messagebox.showerror("Error", "La hora inicial no puede ser igual a la hora final.")
                    return


            hours_Str = start_Hour + '-' + end_Hour
            return hours_Str

        def generate_Schedule ():
            schedule_Str = ""
            hours_Str = ""
            days_Str = ""

            days_Str = get_Days_Schedule()
            if not days_Str:
                return 

            hours_Str = get_Hours_Schedule()
            if not hours_Str:
                return

            schedule_Str += days_Str + ';' + hours_Str
            return_Variable.set(schedule_Str)
            self.close_Schedule_Dialog()
            return

        if self.current_Action == self.available_Actions[4]:
            return

        self.current_Action = self.available_Actions[4]
        self.__hightlight_Btns([])
        
        self.schedule_Dialog = tk.Toplevel(pady=32)
        self.schedule_Dialog.geometry(self.centrar_Ventana(550,300))
        self.schedule_Dialog.resizable(False,False)
        
        self.schedule_Dialog.title("Generar Horario de Inscripción")
        self.schedule_Dialog.protocol("WM_DELETE_WINDOW", self.close_Schedule_Dialog)

        days_List = [
            { "text": "Lunes", "value": "M", "var": tk.BooleanVar(self.schedule_Dialog, name="monday", value=False)},
            { "text": "Martes", "value": "T", "var": tk.BooleanVar(self.schedule_Dialog, name="tuesday", value=False)},
            { "text": "Miércoles", "value": "W", "var": tk.BooleanVar(self.schedule_Dialog, name="wednesday", value=False)},
            { "text": "Jueves", "value": "H", "var": tk.BooleanVar(self.schedule_Dialog, name="thursday", value=False)},
            { "text": "Viernes", "value": "F", "var": tk.BooleanVar(self.schedule_Dialog, name="friday", value=False)},
            { "text": "Sábado", "value": "S", "var": tk.BooleanVar(self.schedule_Dialog, name="saturday", value=False)},
            { "text": "Domingo", "value": "U", "var": tk.BooleanVar(self.schedule_Dialog, name="sunday", value=False)},
        ]

        label_Days = tk.Label(self.schedule_Dialog, text="Días del horario:")
        label_Days.pack(
            anchor="w",
            ipadx=32,
            ipady=8
        )
        frame_Days = tk.Frame(
            self.schedule_Dialog,
            padx=32,
            pady=8
        )
        frame_Days.pack(anchor="w")

        for day in days_List:
            day_Check = ttk.Checkbutton(
                frame_Days,
                text=day["text"],
                variable=day["var"]
            )
            day_Check.pack(
                anchor="w",
                side="left",
                fill="none"
            )

        label_Hours = tk.Label(self.schedule_Dialog, text="Hora del horario:")
        label_Hours.pack(
            anchor="w",
            ipadx=32,
            ipady=8
        )
        frame_Hours = tk.Frame(
            self.schedule_Dialog,
            padx=32,
            pady=8
        )
        frame_Hours.pack(anchor="center", side="top")

        start_Hour_Label = tk.Label(frame_Hours, text="Inicio: ", justify="left")
        start_Hour_Label.pack(anchor="center", side="left")
        start_Hour_Entry = tk.Entry(frame_Hours, width=5)
        start_Hour_Entry.pack(anchor="center", side="left", padx=8)

        end_Hour_Label = tk.Label(frame_Hours, text="Fin: ", justify="left")
        end_Hour_Label.pack(anchor="center", side="left")
        end_Hour_Entry = tk.Entry(frame_Hours, width=5)
        end_Hour_Entry.pack(anchor="center", side="left", padx=8)

        frame_Generate_Btns = tk.Frame(
            self.schedule_Dialog,
            padx=64,
            pady=8
        )
        frame_Generate_Btns.pack(anchor="center", side="bottom")
        generate_Btn = tk.Button(frame_Generate_Btns, text="Generar Horario", command=generate_Schedule)
        generate_Btn.pack(anchor="center", side="left", padx=16)
        cancel_Btn = tk.Button(frame_Generate_Btns, text="Cancelar", command=self.close_Schedule_Dialog)
        cancel_Btn.pack(anchor="center", side="left", padx=16)
        
        return

    def close_Schedule_Dialog (self):
        self.current_Action = ""
        self.__hightlight_Btns(self.btn_Names)

        self.schedule_Dialog.destroy()
        del self.schedule_Dialog
        return

    def idcbox (self):
        students_Ids = self.get_Students({}, "Id_Alumno")
        students_Ids = [ids[0] for ids in students_Ids ]
        return students_Ids
    
    def cursosbox(self):
        courses_Names = self.get_Courses({}, 'Descripción_Curso')
        courses_Names = [curso[0] for curso in courses_Names]
        return courses_Names

    def add_Records_To_Treeview (self, record_Filter={}) -> None:
        treeview_Records = self.tView.get_children()
        for record in treeview_Records:
            self.tView.delete(record)
        
        try:
            records = self.get_Records(filters=record_Filter)

            for i, record in enumerate(records):
                record = self._format_Record_Schedule(record)

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
                values=("Actualmente", "no"," hay", "ningún", "registro")
            )

        return
    
    def autocompletar_Datos_Curso(self,event):
        course_Name = self.cmbx_Cursos.get()
        course_Data = self.get_Courses({"Descripción_Curso": course_Name}, "Código_Curso")[0]
        self.valor_Id.set(course_Data[0])
        return

    def __hightlight_Btns (self, buttons_To_Highlight):
        for btn_Name in self.btn_Names:
            btn = self.frm_1.nametowidget(btn_Name)
            btn["state"] = "disabled"

            if btn_Name in buttons_To_Highlight:
                btn["state"] = "normal"
        

    def __get_Selected_Records (self):
        rows_Id = self.tView.selection()
        records_Data = []

        for row in rows_Id:
            records_Data.append(self.tView.item(row)['values'])

        return records_Data

    def grabar_Inscripcion(self):
    
        id_Estudiante = self.cmbx_Id_Alumno.get()
        if not id_Estudiante:
            messagebox.showerror("Error","Por favor, selecciona un ID de algún Alumno.")
            return 
        cod_Curso = self.valor_Id.get()
        nom_Curso = self.cmbx_Cursos.get()
        if not cod_Curso or not nom_Curso:
            messagebox.showerror("Error","Por favor, selecciona un curso.")
            return
        fecha = self.fecha_Value.get()
        if not fecha:
            messagebox.showerror("Error","Digite una fecha")
            return

        if not self.validar_Fecha():
            messagebox.showerror("Error", "Por favor, digita correctamente la fecha del registro.")
            return

        horario_Curso = self.horario.get()
        if not horario_Curso:
            messagebox.showerror("Error", "Por favor, ingrese el horario del curso a inscribir.")
            return
        
        registro = self.num_Inscripcion_Var.get()
        curso_Existe = self.revisar_Curso(id_Estudiante, cod_Curso)
        if curso_Existe == True:
            messagebox.showerror("Error","El alumno ya está tomando este curso.")
            return
    

        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Id_Alumno FROM Inscritos")
        inscritos = self.cursor.fetchall()
        self.cursor.close()
        inscritos_Ids = [inscrito[0] for inscrito in inscritos]
        if id_Estudiante not in inscritos_Ids:
            self.variable += 1

        self.set_Inscripcion(registro, id_Estudiante, cod_Curso, fecha, horario_Curso)
        self.add_Records_To_Treeview()    
      

        messagebox.showinfo("Completado","La inscripción se guardó con éxito.")

        return
    
    def autocompletar_Treeview(self, event):
        try:
            elmo = self.__get_Selected_Records()[0]
            registro = elmo[0]
            id_Estudiante = str(elmo[1])
            id_Curso = str(elmo[2])
            fecha = str(elmo[4])
            curso = self.get_Course_By_Id(id_Curso, 'Descripción_Curso')
            nombre = self.get_Student_By_Id(id_Estudiante, 'Nombres')
            apellido = self.get_Student_By_Id(id_Estudiante, 'Apellidos')
            self.cursor= self.connection.cursor()
            self.cursor.execute("SELECT Horario FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?", (id_Estudiante, id_Curso))
            horario = self.cursor.fetchone()[0]
            self.cursor.close()
    
            self.cmbx_Id_Alumno.set(id_Estudiante)
            self.nombre_Alumno.set(nombre)
            self.apellido_Alumno.set(apellido)
            self.cmbx_Cursos.set(curso[0])
            self.schedule_Variable.set(horario)
            self.valor_Id.set(id_Curso)
            self.fecha_Value.set(fecha)
            self.num_Inscripcion_Var.set(registro)
        except:
            pass
    
    def control_Errores_Edicion(self):
            
        id_Alumno = self.cmbx_Id_Alumno.get() 
        id_Curso = self.valor_Id.get()
        horario = self.horario.get()
        fecha = self.fecha_Value.get()

        try:
            self.cursor= self.connection.cursor()
            self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?", (id_Alumno,))
            no_Registro = self.cursor.fetchone()[0]   
            self.cursor.close()
        
            try:
                existe = self.revisar_Horario(id_Alumno, id_Curso, horario)
                if existe == True:
                    messagebox.showerror("Error", "Ese alumno ya está viendo ese curso en ese horario.") 
                    return 
                else:
                    self.distinto_Horario(id_Alumno, id_Curso, fecha, horario)
                    return         
            except:     
                pass
            if not id_Curso:
                messagebox.showerror("Error", "Por favor, seleccione un curso.")
            elif not id_Alumno:
                messagebox.showerror("Error", "Por favor, ingrese el ID del alumno.") 
            elif not horario:
                messagebox.showerror("Error", "Por favor, ingrese el horario.")
            elif not fecha:
                messagebox.showerror("Error", "Por favor, ingrese la fecha.") 
            else:
                self.opciones_Edicion(no_Registro, id_Alumno, id_Curso, fecha, horario) 
        except:
            messagebox.showerror("Error", "Ese alumno aun no esta registrado") 

    def distinto_Horario(self, id_Alumno, id_Curso, fecha, horario):
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
               self.add_Records_To_Treeview()
               messagebox.showinfo("Éxito", "Datos actualizados correctamente.")   

    def opciones_Edicion(self, No_Inscripcion: int, student_Id: str, course_Code: str, inscripcion_Date: str, horario: str):

        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(student_Id,))
        cantidad_Registro = len(self.cursor.fetchall())      
        self.connection.commit()
        self.cursor.close()  
        if cantidad_Registro > 1:
            self.ventana_Varios_Cursos(No_Inscripcion)
        else:  
            self.editar_Inscripcion(No_Inscripcion, student_Id, course_Code, inscripcion_Date, horario)
        

    def revisar_Curso(self,student_Id: int, course_Code: str):
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE Id_Alumno = ?",(student_Id,))
        cursos = self.cursor.fetchall()      
        self.cursor.close() 
        for curso in cursos:     
            if course_Code in curso:
                return True
    
    def revisar_Horario(self,student_Id: int, course_Code: str, horario: str):
        curso_Existe = self.revisar_Curso(student_Id,course_Code)
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT Horario FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?",(student_Id, course_Code))
        horario_Actual = self.cursor.fetchone()  
        self.cursor.close() 
        if horario_Actual[0] == horario and curso_Existe == True:
            return True
        
    def editar_Inscripcion(self, No_Inscripcion: int, student_Id: str, course_Code: str, inscripcion_Date: str, horario: str):
        self.cursor= self.connection.cursor()
        self.cursor.execute("UPDATE Inscritos SET Id_Alumno = ?, Código_Curso = ?, Fecha_Inscripción = ?, Horario = ? WHERE No_Inscripción = ?",(student_Id, course_Code, inscripcion_Date, horario,No_Inscripcion)) 
        self.connection.commit()
        self.cursor.close()
        self.add_Records_To_Treeview()
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")    

    def editar_Inscripcion_Cursos(self):
        id_Alumno = self.cmbx_Id_Alumno.get() 
        id_Curso = self.valor_Id.get()
        horario = self.horario.get()
        fecha = self.fecha_Value.get()
        curso_Actual = self.codigo.get()
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?",(id_Alumno,))
        no_Registro = self.cursor.fetchone()[0]       
        self.connection.commit()
        self.cursor.close()  
        
        self.cursor= self.connection.cursor()
        self.cursor.execute("UPDATE Inscritos SET Id_Alumno = ?, Código_Curso = ?, Fecha_Inscripción = ?, Horario = ? WHERE No_Inscripcion = ? AND Código_Curso = ?",(id_Alumno, id_Curso, fecha, horario, no_Registro, curso_Actual))
        self.connection.commit()
        self.cursor.close()
        self.add_Records_To_Treeview()  
        self.habilitar()
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")

    def habilitar(self):
        self.__hightlight_Btns(self.btn_Names)
        self.mini.destroy()
        
    
    def ventana_Varios_Cursos(self,no_Registro):
        self.__hightlight_Btns([])  
        self.mini = tk.Toplevel()
        self.mini.resizable(False,False)
        self.mini.title("Edición de datos")
        self.mini.configure(background="#2271b3")
        self.mini.geometry(self.centrar_Ventana(425,115))
        self.mini.protocol("WM_DELETE_WINDOW", self.habilitar) 

        #Label Aviso
        self.lbl_Info = ttk.Label(self.mini, name="lblinfo")
        self.lbl_Info.configure(background="#bfcde6", text='Seleccione el curso que desea reemplazar:')
        self.lbl_Info.place(anchor="nw", x=97, y=12)

        #Label Codigo_Curso
        self.lbl_Codigo = ttk.Label(self.mini, name="lblcodigo")
        self.lbl_Codigo.configure(background="#bfcde6", text='Código del curso:')
        self.lbl_Codigo.place(anchor="nw", x=20, y=45)

        #Entry Codigo_Curso
        self.codigo= ttk.Combobox(self.mini, name="curse", values=self.codebox(no_Registro),state="readonly")
        self.codigo.place(anchor="nw", width=140, x=150, y=44)
        self.codigo.bind("<<ComboboxSelected>>", self.autocompletar_Curso_Mini)
        
        #Label Curso
        self.lbl_Curso = ttk.Label(self.mini, name="lblcurso")
        self.lbl_Curso.configure(background="#bfcde6", text='Nombre del curso:')
        self.lbl_Curso.place(anchor="nw", x=20, y=75)

        #Entry Curso
        self.cursotxt = tk.StringVar()
        self.curso = ttk.Entry(self.mini, name="name", textvariable= self.cursotxt)
        self.curso.configure(justify="center")
        self.curso.place(anchor="nw", width=140, x=150, y=74)

        #Botones
        guardar = ttk.Button(self.mini, text="Guardar", command= self.editar_Inscripcion_Cursos)
        guardar.place(anchor="nw", width=90, x=315, y=43)

        cerrar = ttk.Button(self.mini,text="Cerrar",command = self.habilitar)
        cerrar.place(anchor="nw", width=90, x=315,y=73)

    def autocompletar_Curso_Mini(self,event):
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
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE No_Inscripcion = ?",(no_Registro,))
        codigos = self.cursor.fetchall()
        self.cursor.close()
        curso = [curso[0] for curso in codigos]
        return curso
        
    def handle_Delete_Records (self):
        
        records_Selected = self.__get_Selected_Records()

        if self.current_Action == self.available_Actions[3] and len(records_Selected) > 0:
            return self.delete_Records_By_Selection(records_Selected, no_Dialog=True)

        if len(records_Selected) <= 0:
            return self.delete_Records_By_Action()
        else:
            return self.delete_Records_By_Selection(records_Selected)
        

    def delete_Records_By_Selection (self, records_Selected, no_Dialog=False):
        if not no_Dialog:
            dialog_Msg = "¿Esta seguro de eliminar %s?"

            if len(records_Selected) > 1:
                dialog_Msg = dialog_Msg % "los registros seleccionados"
            else:
                dialog_Msg = dialog_Msg % "el registro seleccionado"

            if not messagebox.askokcancel("Eliminar Inscripciones", dialog_Msg):
                return

        for record in records_Selected:
            self.delete_Record_By_Id(record[0])

        self.add_Records_To_Treeview()
        self.cancel_Record()
        return

    def delete_Records_By_Action (self):
        self.__hightlight_Btns((self.btn_Names[3], self.btn_Names[4]))
        self.current_Action = self.available_Actions[3]
        self.cancel_Record()
        
    def close_Consulta(self):
        self.__hightlight_Btns(self.btn_Names)
        self.ventana_Consulta.destroy()        

    def abrir_Consulta(self):
        self.__hightlight_Btns([])  
        self.ventana_Consulta = tk.Toplevel(self.win)
        self.ventana_Consulta.title("Consulta")
        self.ventana_Consulta.resizable(False, False)
        self.ventana_Consulta.geometry("300x300")  
        self.ventana_Consulta.update_idletasks()
        width = self.ventana_Consulta.winfo_width()
        height = self.ventana_Consulta.winfo_height()
        x = (self.win.winfo_screenwidth() - width) // 2
        y = (self.win.winfo_screenheight() - height) // 2
        self.ventana_Consulta.geometry(f"{width}x{height}+{x}+{y}")
        self.ventana_Consulta.protocol("WM_DELETE_WINDOW", self.close_Consulta)

        self.frame_Estudiante = tk.Frame(self.ventana_Consulta)
        self.frame_Estudiante.pack(padx=10, pady=10)
        label_Estudiante = tk.Label(self.frame_Estudiante, text="Seleccionar estudiante:")
        label_Estudiante.pack(side="left")
        self.combo_Estudiantes = ttk.Combobox(self.frame_Estudiante, values=self.idcbox(), state="readonly")
        self.combo_Estudiantes.pack(side="left")

        self.frame_Curso = tk.Frame(self.ventana_Consulta)
        self.frame_Curso.pack(padx=10, pady=10)
        label_Curso = tk.Label(self.frame_Curso, text="Seleccionar curso:")
        label_Curso.pack(side="left")
        self.combo_Cursos = ttk.Combobox(self.frame_Curso, values=self.cursosbox(), state="readonly")
        self.combo_Cursos.pack(side="left")

        self.frame_Treeview = tk.Frame(self.ventana_Consulta)
        self.frame_Treeview.pack(padx=10, pady=10, fill="both", expand=True)
        self.treeview_Consulta = ttk.Treeview(self.frame_Treeview, columns=("columna1"), show="headings")
        self.treeview_Consulta.heading("columna1", text="Datos de la Consulta")
        self.treeview_Consulta.pack(side="left", fill="both", expand=True)

        self.combo_Estudiantes.bind("<<ComboboxSelected>>", self.consultar_Cursos_Del_Estudiante)
        self.combo_Cursos.bind("<<ComboboxSelected>>", self.consultar_Estudiantes_Del_Curso)

    def consultar_Cursos_Del_Estudiante(self, event):
        self.treeview_Consulta.delete(*self.treeview_Consulta.get_children())  
        self.treeview_Consulta["columns"] = ("columna1",)
        self.treeview_Consulta.heading("columna1", text="Descripción del Curso")
        self.treeview_Consulta.column("columna1", width=300)
        self.cursor = self.connection.cursor()
        id_Alumno = self.combo_Estudiantes.get()
        self.cursor.execute("SELECT Código_Curso FROM Inscritos WHERE Id_Alumno = ?", (id_Alumno,))
        id_Cursos = self.cursor.fetchall()
        self.cursor.close()
        for id_Curso in id_Cursos:
            codigo_Curso = id_Curso[0]  
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT Descripción_Curso FROM Cursos WHERE Código_Curso = ?", (codigo_Curso,))
            descripcion_Curso = self.cursor.fetchone()
            self.treeview_Consulta.insert("", "end", values=descripcion_Curso)
            self.cursor.close()

    def consultar_Estudiantes_Del_Curso(self, event):
        self.treeview_Consulta.delete(*self.treeview_Consulta.get_children()) 
        self.treeview_Consulta["columns"] = ("columna1", "columna2")
        self.treeview_Consulta.heading("columna1", text="Nombres")
        self.treeview_Consulta.heading("columna2", text="Apellidos")
        self.treeview_Consulta.column("columna1", width=150)
        self.treeview_Consulta.column("columna2", width=150)
        self.cursor = self.connection.cursor()
        id_Curso = self.combo_Cursos.get()
        self.cursor.execute("SELECT Código_Curso FROM Cursos WHERE Descripción_Curso = ?", (id_Curso,))
        codigo_Curso = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT Id_Alumno FROM Inscritos WHERE Código_Curso = ?", (codigo_Curso,))
        id_Alumnos = self.cursor.fetchall()
        self.cursor.close()
        for id_Alumno in id_Alumnos:
            id_Alumno = id_Alumno[0]  
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno = ?", (id_Alumno,))
            alumnos = self.cursor.fetchone()
            self.treeview_Consulta.insert("", "end", values=alumnos)
            self.cursor.close()

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
    
