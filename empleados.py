#from multiprocessing import parent_process
from multiprocessing import Process
from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class empleadosClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de inventario | Empleados")
        self.root.config(bg="white")
        self.root.focus_force
        #Todas las variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #SearchFrame
        searchFrame=LabelFrame(self.root,text="Buscar Empleado",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=250,y=20,width=600,height=70)

        #Opciones
        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_searchby,values=("Seleccionar","Email","Name","Contact"),state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(searchFrame,text="Buscar",command=self.search,font=("goudy old style",15),bg="#8f0000",fg="white",cursor="hand2").place(x=430,y=11,width=150,height=25)

        #Title
        title=Label(self.root,text="Detalle de los empleados",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #Content
        #-row1-
        lbl_empid=Label(self.root,text="Emp ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Genero",font=("goudy old style",15),bg="white").place(x=350,y=150)
        lbl_contact=Label(self.root,text="Contacto",font=("goudy old style",15),bg="white").place(x=750,y=150)
        
        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)        
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Seleccionar","Femenino","Masculino","Otro"),state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)

        #-row2-
        lbl_name=Label(self.root,text="Nombre",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="dd/mm/aaaa",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lbl_doj=Label(self.root,text="Antiguedad",font=("goudy old style",15),bg="white").place(x=750,y=190)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightyellow").place(x=850,y=190,width=180)

        #-row3-
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Contraseña",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Empleado"),state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #-row4-
        lbl_adress=Label(self.root,text="Dirección",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salario",font=("goudy old style",15),bg="white").place(x=500,y=270)

        self.text_adress=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.text_adress.place(x=150,y=270,width=300,height=60)
        text_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",15),bg="lightyellow").place(x=600,y=270,width=180)

        #Botones
        btn_add=Button(self.root,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Eliminar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)


        #Detalles de Empleados
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmpleadosTabla=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","adress","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmpleadosTabla.xview)
        scrolly.config(command=self.EmpleadosTabla.yview)

        self.EmpleadosTabla.heading("eid",text="ID")
        self.EmpleadosTabla.heading("name",text="Nombre Completo")
        self.EmpleadosTabla.heading("email",text="Email")
        self.EmpleadosTabla.heading("gender",text="Genero")
        self.EmpleadosTabla.heading("contact",text="Contacto")
        self.EmpleadosTabla.heading("dob",text="D.O.B")
        self.EmpleadosTabla.heading("doj",text="D.O.J")
        self.EmpleadosTabla.heading("pass",text="Contraseña")
        self.EmpleadosTabla.heading("utype",text="Tipo de Usuario")
        self.EmpleadosTabla.heading("adress",text="Dirección")
        self.EmpleadosTabla.heading("salary",text="Salario")

        self.EmpleadosTabla["show"]="headings"

        self.EmpleadosTabla.column("eid",width=50)
        self.EmpleadosTabla.column("name",width=100)
        self.EmpleadosTabla.column("email",width=90)
        self.EmpleadosTabla.column("gender",width=90)
        self.EmpleadosTabla.column("contact",width=90)
        self.EmpleadosTabla.column("dob",width=90)
        self.EmpleadosTabla.column("doj",width=90)
        self.EmpleadosTabla.column("pass",width=90)
        self.EmpleadosTabla.column("utype",width=90)
        self.EmpleadosTabla.column("adress",width=90)
        self.EmpleadosTabla.column("salary",width=90)
        self.EmpleadosTabla.pack(fill=BOTH,expand=1)

        self.EmpleadosTabla.bind("<ButtonRelease-1>",self.get_data)        

        self.show()

    def add(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Empleado ID debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from empleado where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","El id de empleado ya esta asignado, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Insert into empleado (eid,name,email,gender,contact,dob,doj,pass,utype,adress,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                    self.var_emp_id.get(),
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),
                                    
                                    self.var_dob.get(),
                                    self.var_doj.get(),
                                    
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.text_adress.get("1.0",END),
                                    self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Empleado Agregado con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select * from empleado")
            rows=cur.fetchall()
            self.EmpleadosTabla.delete(*self.EmpleadosTabla.get_children())
            for row in rows:
                self.EmpleadosTabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



    
    def get_data(self,ev):
        f=self.EmpleadosTabla.focus()
        content=(self.EmpleadosTabla.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
                                            
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
                                            
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.text_adress.delete("1.0",END),
        self.text_adress.insert(END,row[9]),
        self.var_salary.set(row[10])


    def update(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Empleado ID debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from empleado where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","El id de empleado no es valido, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Update empleado set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,adress=?,salary=? where eid=?",(
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),                                    
                                    self.var_dob.get(),
                                    self.var_doj.get(),                                    
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.text_adress.get("1.0",END),
                                    self.var_salary.get(),
                                    self.var_emp_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Datos modificado con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="Seleccionar":
                messagebox.showerror("Error","Empleado ID debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from empleado where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","El id de empleado no es valido, prueba uno diferente",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Estas seguro de eliminar al empleado?",parent=self.root)
                    if op==True:
                        cur.execute("delete from empleado where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Eliminado","Empleado Eliminado con Exito!",parent=self.root)
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_emp_id.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set("Seleccionar"),
        self.var_contact.set(""),                                    
        self.var_dob.set(""),
        self.var_doj.set(""),                                    
        self.var_pass.set(""),
        self.var_utype.set("Admin"),
        self.text_adress.delete("1.0",END),
        self.var_salary.set(""),
        self.var_searchtxt.set(""),
        self.var_searchby.set("Seleccionar"),
        self.show()


    def search(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Seleccionar":
                messagebox("Error","Selecionar una opcion de busqueda",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox("Error","Ingrese un tipo de busqueda",parent=self.root)

            else:
                cur.execute("select * from empleado where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmpleadosTabla.delete(*self.EmpleadosTabla.get_children())
                    for row in rows:
                        self.EmpleadosTabla.insert("",END,values=row)
                else:
                    messagebox("Error","Es una funcion de busqueda!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


if __name__ == '__main__':
    root = Tk()
    obj= empleadosClass(root)
    root.mainloop()