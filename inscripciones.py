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
        "btnCancelar"
    )

    current_action = ""
    available_actions = (
        "query",
        "save",
        "edit",
        "delete"
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
        self.num_Inscripcion = ttk.Label(self.frm_1, text= self.numero_de_registro(),  name="num_inscripcion")
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
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)

        #Entry del Horario
        self.value_horario= tk.StringVar()
        self.horario = ttk.Entry(self.frm_1, name="entry3",textvariable=self.value_horario)
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=690, y=185)

        ''' Botones  de la Aplicación'''
        ## algo de color
        self.style= ttk.Style()
        self.style.configure('TButton', background='#85C1E9', foreground='black')

        #Boton Consultar
        self.btnConsultar= ttk.Button(self.frm_1, name=self.btn_names[0])
        self.btnConsultar.configure(text='Consultar')
        self.btnConsultar.place(anchor="nw",x=150,y=260)

        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name=self.btn_names[1] ,command=self.grabar_inscripcion)
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=250, y=260)
        
        #Botón Editar 
        self.btnEditar = ttk.Button(self.frm_1, name=self.btn_names[2])
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=350, y=260)

        #Botón Eliminar
        self.btnEliminar = ttk.Button(
            self.frm_1, 
            name=self.btn_names[3],
            command=self.handle_delete_records
        )
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=450, y=260)

        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name=self.btn_names[4])
        self.btnCancelar.configure(text='Cancelar', command= self.reniciar_Registro)
        self.btnCancelar.place(anchor="nw", x=550, y=260)

        #Botón Editar plus
        self.btnEditarplus = ttk.Button(self.frm_1, name="btneditarplus")
        self.btnEditarplus.configure(text='Editar Alumnos',  command= lambda: self.ventana_secundaria_alumnos(self.cmbx_Id_Alumno.get()))
        self.btnEditarplus.place(anchor="nw", x=230, y=78)

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

    def reniciar_Registro(self):
        self.num_InscripcionVar.set(self.numero_de_registro())
        self.fecha_value.set("")
        self.apellido_Alumno.set("")
        self.nombre_Alumno.set("")
        self.cmbx_Cursos.set("")
        self.valor_id.set("")
        self.value_horario.set("")
        self.cmbx_Id_Alumno.set("")
        try:
            self.habilitar(self.mini)
        except:
            pass

    def numero_de_registro(self):   
        self.cursor = self.connection.cursor()
        num_alumnos = 'SELECT * FROM Inscritos;'  
        self.cursor.execute(num_alumnos) 
        cantidad = len(self.cursor.fetchall())
        id_registro = cantidad + 1
        self.cursor.close()
        return id_registro
    
    def habilitar(self, ventana):
        ventana.destroy()
        self.btnEditarplus["state"] = "normal"

    def ventana_secundaria_alumnos(self,id):
        if id == "":
            messagebox.showerror("Error", "Porfavor, seleccione algun Id")
        else:
            self.btnEditarplus["state"] = "disabled"    
            self.mini = tk.Toplevel()
            self.mini.resizable(False,False)
            self.mini.title("Edición de datos")
            self.mini.configure(background="#2271b3")
            self.mini.geometry(self.centrarVentana(460,200))
            self.mini.protocol("WM_DELETE_WINDOW", lambda: self.habilitar(self.mini))
            
            #Label nombre
            self.lblname = ttk.Label(self.mini, name="lblname ")
            self.lblname.configure(background="#bfcde6", text='Nombres:')
            self.lblname.place(anchor="nw", x=20, y=20)
    
            #Entry nombre
            self.name = ttk.Entry(self.mini, name="name")
            self.name.configure(justify="center")
            self.name.place(anchor="nw", width=90, x=90, y=20)
    
            #Label Apellido
            self.lbllastname = ttk.Label(self.mini, name="lbllastname")
            self.lbllastname.configure(background="#bfcde6", text='Apellidos:')
            self.lbllastname.place(anchor="nw", x=20, y=50)
    
            #Entry Apellido
            self.lastname = ttk.Entry(self.mini, name="lastname")
            self.lastname.configure(justify="center")
            self.lastname.place(anchor="nw", width=90, x=90, y=50)
    
            #Label Fecha
            self.lbldate = ttk.Label(self.mini, name="lbldate")
            self.lbldate.configure(background="#bfcde6", text='Fecha:')
            self.lbldate.place(anchor="nw", x=20, y=80)
    
            #Entry Fecha
            self.date = ttk.Entry(self.mini, name="date")
            self.date.configure(justify="center")
            self.date.place(anchor="nw", width=90, x=90, y=80)
    
            #Label Ciudad
            self.lblcity = ttk.Label(self.mini, name="lblcity")
            self.lblcity.configure(background="#bfcde6", text='Ciudad:')
            self.lblcity.place(anchor="nw", x=20, y= 110)
    
            #Entry Ciudad
            self.place = ttk.Entry(self.mini, name="place")
            self.place.configure(justify="center")
            self.place.place(anchor="nw", width=90, x=90, y=110)
    
            #Label Departamento 
            self.lbldepartment = ttk.Label(self.mini, name="lbldepartment")
            self.lbldepartment.configure(background="#bfcde6", text='Departamento:')
            self.lbldepartment.place(anchor="nw", x=240, y= 20)
    
            #Entry Departamento
            self.department = ttk.Entry(self.mini, name="department")
            self.department.configure(justify="center")
            self.department.place(anchor="nw", width=90, x=340, y=20)
    
            #Label Dirección
            self.lbladdress = ttk.Label(self.mini, name="lbladress")
            self.lbladdress.configure(background="#bfcde6", text='Dirección:')
            self.lbladdress.place(anchor="nw", x=240, y=50)
    
            #Entry Dirección
            self.address = ttk.Entry(self.mini, name="address")
            self.address.configure(justify="center")
            self.address.place(anchor="nw", width=90, x=340, y=50)
                  
            #Label Cel
            self.lblcellphone = ttk.Label(self.mini, name="lblcellphone")
            self.lblcellphone.configure(background="#bfcde6", text='Teléfono Celular:')
            self.lblcellphone.place(anchor="nw", x=240, y= 80)
    
            #Entry Cel
            self.cellphone = ttk.Entry(self.mini, name="cellphone")
            self.cellphone.configure(justify="center")
            self.cellphone.place(anchor="nw", width=90, x=340, y=80)
    
            #Label Fijo
            self.lblphone = ttk.Label(self.mini, name="lblphone")
            self.lblphone.configure(background="#bfcde6", text='Teléfono Fijo:')
            self.lblphone.place(anchor="nw", x=240, y= 110)
    
            #Entry Fijo
            self.phone = ttk.Entry(self.mini, name="phone")
            self.phone.configure(justify="center")
            self.phone.place(anchor="nw", width=90, x=340, y=110)
    
            #Botones
            guardar = ttk.Button(self.mini, text="Guardar", command= lambda: self.setter_alumnos(id))
            guardar.place(anchor="nw", width=90, x=250, y=160)
    
            cerrar = ttk.Button(self.mini,text="Cerrar",command = lambda: self.habilitar(self.mini))
            cerrar.place(x=355,y=160)


    def setter_alumnos (self,id):
        self.cursor = self.connection.cursor()    
        if self.name.get() == "":
            pass
        elif len(self.name.get()) > 64:
            messagebox.showerror("Error", "Ocurrio un error con Nombre, deben ser maximo 64 caracteres")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET Nombres= '{self.name.get()}'WHERE Id_Alumno='{id}'" )
        
        if self.lastname.get() == "":
            pass
        elif len(self.lastname.get()) > 64:
            messagebox.showerror("Error", "Ocurrio un error con Apellido, deben ser maximo 64 caracteres")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET Apellidos= '{self.lastname.get()}'WHERE Id_Alumno='{id}'" )

        if self.place.get() == "":
            pass
        elif len(self.place.get()) > 64:
            messagebox.showerror("Error", "Ocurrio un error con Ciudad, deben ser maximo 64 caracteres")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET  Ciudad='{self.place.get()}' WHERE Id_Alumno='{id}'")

        if self.date.get() == "":
            pass
        elif len(self.date.get()) > 10:
            messagebox.showerror("Error", "Fecha no valida")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET  Fecha_Ingreso='{self.date.get()}' WHERE Id_Alumno='{id}'")

        if self.department.get() == "":
            pass
        elif len(self.department.get()) > 64:
            messagebox.showerror("Error", "Ocurrio un error con Departamento, deben ser maximo 64 caracteres")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET Departamento='{self.department.get()}' WHERE Id_Alumno='{id}'" )

        if self.address.get() == "":
            pass
        elif len(self.address.get()) > 64:
            messagebox.showerror("Error", "Ocurrio un error con Dirección, deben ser maximo 64 caracteres")
        else:
            self.cursor.execute(f"UPDATE Alumnos SET Dirección='{self.address.get()}' WHERE Id_Alumno='{id}'" ) 

        if self.cellphone.get() == "":
            pass
        elif len(self.cellphone.get()) != 9:
            messagebox.showerror("Error", "Ocurrio un error con Teléfono Celular, deben ser 9 caracteres")
        else:
            try:
                if int(self.cellphone.get()) < 0:
                    messagebox.showerror("Error", "Ocurrio un error con Teléfono  Celular, deben ser números postivos")
                else:
                    self.cursor.execute(f"UPDATE Alumnos SET Telef_Cel='{self.cellphone.get()}' WHERE Id_Alumno='{id}'" )
            except ValueError:
                messagebox.showerror("Error", "Ocurrio un error con Teléfono Celular, deben ser números unicamente")

        if self.phone.get() == "":
            pass
        elif len(self.phone.get()) != 10:
            messagebox.showerror("Error", "Ocurrio un error con Teléfono  Fijo, deben ser 10 caracteres")
        else:
            try:
                if int(self.phone.get()) < 0:
                    messagebox.showerror("Error", "Ocurrio un error con Teléfono  Fijo, deben ser números postivos")
                else:           
                    self.cursor.execute(f"UPDATE Alumnos SET Telef_Fijo='{self.phone.get()}' WHERE Id_Alumno='{id}'" )
            except ValueError:
                messagebox.showerror("Error", "Ocurrio un error con Teléfono Fijo, deben ser números unicamente")
   
        self.connection.commit()
        self.cursor.close()


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
                No_Inscripción INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    ("7856019526884687", "2933", "Martín", "Hernández", "2023-08-01", "Bogota", "1234567890"),
                    ("5399046924785948", "2518", "Juan", "Morales", "2024-01-01", "Bogotá", "5432109876"),
                    ("1722202291005220", "2879", "Andres", "hernandez", "2024-05-05", "Medellin", "0000000000"),
                    ("4274203119662378", "2545", "Laura", "Moreno", "2023-08-01", "Fusagasuga", "1132432433"),
                    ("1827391938728989", "2879", "Nicolas", "Corredor", "2023-08-01", "Bogotá", "1353515989"),
                    ("32458769", "2518", "María", "González", "2023-02-15", "Cali", "9876543210"),
                    ("56789012", "2933", "Ana", "Martínez", "2018-08-20", "Medellín", "6789012345"),
                    ("98765432", "2879", "Pedro", "López", "2021-08-10", "Bogotá", "4567890123"),
                    ("34567890", "2545", "Sofía", "Ramírez", "2022-08-25", "Barranquilla", "8901234567"),
                    ("89012345", "2518", "Carlos", "Gómez", "2020-08-05", "Cartagena", "7890123456"),
                    ("12345678", "2879", "Daniela", "Herrera", "2023-08-12", "Bucaramanga", "6789012345"),
                    ("45678901", "2933", "Diego", "Jiménez", "2021-08-30", "Cúcuta", "5678901234"),
                    ("78901234", "2545", "Valentina", "Díaz", "2018-08-08", "Santa Marta", "4567890123"),
                    ("90123456", "2879", "Lucas", "Sánchez", "2023-08-18", "Pereira", "3456789012"),
                    ("23456789", "2518", "Mariana", "Torres", "2019-08-02", "Manizales", "2345678901");

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

    def set_inscripcion(self, student_id: str, course_code: str, inscripcion_date: str, course_schedule: str):
        self.cursor = self.connection.cursor()

        query = "INSERT INTO Inscritos (Id_Alumno, Código_Curso, Horario, Fecha_Inscripción) VALUES (?, ?, ?, ?)"
        new_record_data = (student_id, course_code, course_schedule, inscripcion_date)
        self.cursor.execute(query, new_record_data)

        self.connection.commit()
        self.cursor.close()
        return

    ## autocompleta el nombre yy el apellido esta conectado al combobox
    def autocompletar_nombre(self,event):
        student_id = self.cmbx_Id_Alumno.get()

        datos = self.get_student_by_id(student_id)
        nombres_Alu= datos[3]
        apellidos_Alu = datos[2]
        ##modificamos los entry de nombres y apellidos
        self.apellido_Alumno.set(nombres_Alu)
        self.nombre_Alumno.set(apellidos_Alu)

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
            if btn_name in buttons_to_highlight:
                continue
            
            btn = self.frm_1.nametowidget(btn_name)
            btn["state"] = "disabled"

    def __get_selected_records (self):
        rows_id = self.tView.selection()
        records_data = []

        for row in rows_id:
            records_data.append(self.tView.item(row)['values'])

        return records_data

    def grabar_inscripcion(self):
        """
            aca solo se graba los datos que piden actualmente la tabla de inscritos
            la fecha, el id del estudiante y el id del curso
            Falta agregar la funcion del horario, ya que no esta en la database
            asi podemos completar esta funcion.
            no se como lo vamos a manejar, asi que lo dejo asi por ahora
        """

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
        
        self.set_inscripcion(id_estudiante, cod_curso, fecha, horario_curso)
        self.add_records_to_treeview()

        messagebox.showinfo("Completado","La inscripción se guardo con exito")
        
    def handle_delete_records (self):
        records_selected = self.__get_selected_records()

        if self.current_action == self.available_actions[3]:
            return self.delete_records_by_selection(records_selected, no_dialog=True)

        if len(records_selected) <= 0:
            return self.delete_records_by_action()
        else:
            return self.delete_records_by_selection(records_selected)

    def delete_records_by_selection (self, records_selected, no_dialog=False):
        dialog_msg = "¿Esta seguro de eliminar %s?"

        if len(records_selected) > 1:
            dialog_msg = dialog_msg % "los registros seleccionados"
        else:
            dialog_msg = dialog_msg % "el registro seleccionado"

        if not no_dialog:
            if not messagebox.askokcancel("Eliminar Inscripciones", dialog_msg):
                return

        for record in records_selected:
            self.delete_record_by_id(record[0])

        self.add_records_to_treeview()
        return

    def delete_records_by_action (self):
        self.__highlight_btns((self.btn_names[3], self.btn_names[4]))
        self.current_action = self.available_actions[3]

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
    
