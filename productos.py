#from multiprocessing import parent_process
from cgitb import text
from multiprocessing import Process
from tkinter import *
from tkinter import font
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class productosClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de inventario | Productos")
        self.root.config(bg="white")
        self.root.focus_force


        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_proveedor=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_cantidad=StringVar()
        self.var_status=StringVar()
        
        producto_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        producto_Frame.place(x=10,y=10,width=450,height=480)

        #Title
        title=Label(producto_Frame,text="Detalle de los productos",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        
        #Columna 1
        lbl_categoria=Label(producto_Frame,text="Categoria",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_proveedor=Label(producto_Frame,text="Proveedor",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(producto_Frame,text="Nombre",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(producto_Frame,text="Precio",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_cantidad=Label(producto_Frame,text="Cantidad",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(producto_Frame,text="Estado",font=("goudy old style",18),bg="white").place(x=30,y=310)

        #Columna 2
        cmb_cat=ttk.Combobox(producto_Frame,textvariable=self.var_cat,values=self.cat_list,state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_proveedor=ttk.Combobox(producto_Frame,textvariable=self.var_proveedor,values=self.sup_list,state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_proveedor.place(x=150,y=110,width=200)
        cmb_proveedor.current(0)

        text_name=Entry(producto_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)
        text_price=Entry(producto_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=210,width=200)
        text_cantidad=Entry(producto_Frame,textvariable=self.var_cantidad,font=("goudy old style",15),bg="lightyellow").place(x=150,y=260,width=200)
        
        cmb_status=ttk.Combobox(producto_Frame,textvariable=self.var_status,values=("Activo","Inactivo"),state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)


        #Botones
        btn_add=Button(producto_Frame,text="Guardar",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(producto_Frame,text="Actualizar",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(producto_Frame,text="Eliminar",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(producto_Frame,text="Limpiar",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #SearchFrame
        searchFrame=LabelFrame(self.root,text="Buscar Prducto",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=480,y=10,width=600,height=80)

        #Opciones de Busqueda
        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_searchby,values=("Seleccionar","Categoria","Proveedor","Nombre"),state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        
        txt_search=Entry(searchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(searchFrame,text="Buscar",command=self.search,font=("goudy old style",15),bg="#8f0000",fg="white",cursor="hand2").place(x=430,y=11,width=150,height=25)

        #Detalles del producto
        producto_Frame=Frame(self.root,bd=3,relief=RIDGE)
        producto_Frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(producto_Frame,orient=VERTICAL)
        scrollx=Scrollbar(producto_Frame,orient=HORIZONTAL)

        self.PrductosTabla=ttk.Treeview(producto_Frame,columns=("pid","Proveedor","Categoria","name","price","cantidad","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.PrductosTabla.xview)
        scrolly.config(command=self.PrductosTabla.yview)

        self.PrductosTabla.heading("pid",text="ID")
        self.PrductosTabla.heading("Categoria",text="Categoria")
        self.PrductosTabla.heading("Proveedor",text="Proveedor")
        self.PrductosTabla.heading("name",text="Nombre")
        self.PrductosTabla.heading("price",text="Precio")
        self.PrductosTabla.heading("cantidad",text="Cantidad")
        self.PrductosTabla.heading("status",text="Estado")
        self.PrductosTabla["show"]="headings"

        self.PrductosTabla.column("pid",width=50)
        self.PrductosTabla.column("Categoria",width=100)
        self.PrductosTabla.column("Proveedor",width=100)
        self.PrductosTabla.column("name",width=100)
        self.PrductosTabla.column("price",width=100)
        self.PrductosTabla.column("cantidad",width=100)
        self.PrductosTabla.column("status",width=100)
        self.PrductosTabla.pack(fill=BOTH,expand=1)
        self.PrductosTabla.bind("<ButtonRelease-1>",self.get_data)        

        self.show()


    #Funciones
    #fetch_cat_sup Llamar valores de otra tabla o base de datos
    def fetch_cat_sup(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("Select name from categoria")
            cat=cur.fetchall()
            self.cat_list.append("Vacio")
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Seleccionar")
                for i in cat:
                    self.cat_list.append(i[0])
            #_________# 
            cur.execute("Select name from proveedor")
            sup=cur.fetchall()
            self.sup_list.append("Vacio")
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Seleccionar")
                for i in sup:
                    self.sup_list.append(i[0])
                

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


    def add(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Seleccionar" or self.var_cat.get()=="Vacio" or self.var_proveedor.get()=="Seleccionar" or self.var_name.get()=="":
                messagebox.showerror("Error","Todos los campos son obligatorios",parent=self.root)
            else:
                cur.execute("Select * from producto where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","El producto ya esta registrado, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Insert into producto (Categoria,Proveedor,name,price,cantidad,status) values(?,?,?,?,?,?)",(
                                    self.var_cat.get(),
                                    self.var_proveedor.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_cantidad.get(),                                    
                                    self.var_status.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Producto agregado con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select * from producto")
            rows=cur.fetchall()
            self.PrductosTabla.delete(*self.PrductosTabla.get_children())
            for row in rows:
                self.PrductosTabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



    
    def get_data(self,ev):
        f=self.PrductosTabla.focus()
        content=(self.PrductosTabla.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[2]),
        self.var_proveedor.set(row[1]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_cantidad.set(row[5]),
        self.var_status.set(row[6]),
        


    def update(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Seleccione un producto de la lista.",parent=self.root)
            else:
                cur.execute("Select * from producto where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","El producto no es valido, prueba uno diferente",parent=self.root)
                else:
                    cur.execute("Update producto set Categoria=?,Proveedor=?,name=?,price=?,cantidad=?,status=? where pid=?",(
                                    self.var_cat.get(),
                                    self.var_proveedor.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_cantidad.get(),                                    
                                    self.var_status.get(),
                                    self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Producto modificado con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="Seleccionar":
                messagebox.showerror("Error","Seleccione un producto de la lista",parent=self.root)
            else:
                cur.execute("Select * from producto where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Selecciona un producto de la lista y pruebe nuevamente.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Estas seguro de eliminar al empleado?",parent=self.root)
                    if op==True:
                        cur.execute("delete from producto where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Eliminado","Producto eliminado con exito!",parent=self.root)
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_cat.set("Seleccionar"),
        self.var_proveedor.set("Seleccionar"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_cantidad.set(""),                                    
        self.var_status.set("Activo"),
        self.var_pid.set(""),
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
                cur.execute("select * from producto where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.PrductosTabla.delete(*self.PrductosTabla.get_children())
                    for row in rows:
                        self.PrductosTabla.insert("",END,values=row)
                else:
                    messagebox("Error","Es una funcion de busqueda!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



if __name__ == '__main__':
    root = Tk()
    obj= productosClass(root)
    root.mainloop()