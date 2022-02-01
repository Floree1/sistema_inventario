#from multiprocessing import parent_process
from multiprocessing import Process
from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class proveedorClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de inventario | Proveedor")
        self.root.config(bg="white")
        self.root.focus_force
        #Todas las variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()

        #Opciones
        lbl_search=Label(self.root,text="N° de Factura:",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)
        

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=835, y=80, width=160)
        btn_search=Button(self.root,text="Buscar",command=self.search,font=("goudy old style",15),bg="#8f0000",fg="white",cursor="hand2").place(x=980,y=80,width=100,height=28)

        #Title
        title=Label(self.root,text="Detalle de los Proveedores",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #Content
        #-row1-
        lbl_supplier_invoice=Label(self.root,text="Factura N°",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)        
        
        #-row2-
        lbl_name=Label(self.root,text="Nombre",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #-row3-
        lbl_contact=Label(self.root,text="Contacto",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)

        #-row4-
        lbl_desc=Label(self.root,text="Descripcion",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.text_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.text_desc.place(x=180,y=200,width=470,height=200)
       
        #Botones
        btn_add=Button(self.root,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=405,width=110,height=30)
        btn_update=Button(self.root,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=405,width=110,height=30)
        btn_delete=Button(self.root,text="Eliminar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=405,width=110,height=30)
        btn_clear=Button(self.root,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=405,width=110,height=30)


        #Detalles de Empleados
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.proveedorTabla=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.proveedorTabla.xview)
        scrolly.config(command=self.proveedorTabla.yview)

        self.proveedorTabla.heading("invoice",text="Factura N°")
        self.proveedorTabla.heading("name",text="Nombre Completo")
        self.proveedorTabla.heading("contact",text="Contacto")
        self.proveedorTabla.heading("desc",text="Descripcion")
        

        self.proveedorTabla["show"]="headings"

        self.proveedorTabla.column("invoice",width=50)
        self.proveedorTabla.column("name",width=100)
        self.proveedorTabla.column("contact",width=90)
        self.proveedorTabla.column("desc",width=90)

        self.proveedorTabla.pack(fill=BOTH,expand=1)

        self.proveedorTabla.bind("<ButtonRelease-1>",self.get_data)        

        self.show()

    def add(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","N° de Factura debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from proveedor where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","El N° Facturado ya esta registrado, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Insert into proveedor (invoice,name,contact,desc) values(?,?,?,?)",(
                                    self.var_sup_invoice.get(),
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.text_desc.get("1.0",END),
                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Proveedor Agregado con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select * from proveedor")
            rows=cur.fetchall()
            self.proveedorTabla.delete(*self.proveedorTabla.get_children())
            for row in rows:
                self.proveedorTabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



    
    def get_data(self,ev):
        f=self.proveedorTabla.focus()
        content=(self.proveedorTabla.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.text_desc.delete("1.0",END),
        self.text_desc.insert(END,row[3]),


    def update(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","N° Factura debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from proveedor where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","El N° de Factura no es valido, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Update proveedor set name=?,contact=?,desc=? where invoice=?",(
                                    self.var_name.get(),
                                    self.var_contact.get(),                                    
                                    self.text_desc.get("1.0",END),
                                    self.var_sup_invoice.get()
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
            if self.var_sup_invoice.get()=="Seleccionar":
                messagebox.showerror("Error","N° de Factura debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from proveedor where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","El N° de Factura no es valido, prueba uno diferente",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Estas seguro de eliminar esta factura?",parent=self.root)
                    if op==True:
                        cur.execute("delete from proveedor where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Eliminado","Factura Eliminada con Exito!",parent=self.root)
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),                                    
        self.text_desc.delete("1.0",END),
        self.var_searchtxt.set(""),
        self.show()


    def search(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox("Error","Ingrese N° de Factura",parent=self.root)

            else:
                cur.execute("select * from proveedor where invoice=?",(self.var_searchtxt.get()))
                row=cur.fetchone()
                if row!=None:
                    self.proveedorTabla.delete(*self.proveedorTabla.get_children())
                    self.proveedorTabla.insert("",END,values=row)
                else:
                    messagebox("Error","Es una funcion de busqueda!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


if __name__ == '__main__':
    root=Tk()
    obj=proveedorClass(root)
    root.mainloop()