#from multiprocessing import parent_process
from cgi import test
from distutils import command
from multiprocessing import Process
from tkinter import *
from tkinter import font
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class categoriaClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de inventario | Categoria")
        self.root.config(bg="white")
        self.root.focus_force
        #====Variables===
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #====titulo======
        lbl_title=Label(self.root,text="Gestion de Categorias",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_name=Label(self.root,text="Ingrese nombre de la categoria",font=("goudy old style",30),bg="white" ).place(x=50,y=100)
        lbl_text=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)

        btn_text=Button(self.root,text="Agregar",command=self.add,font=("goudy old style",19),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_text=Button(self.root,text="Eliminar",command=self.delete,font=("goudy old style",19),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        
        #Detalles Categoria
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoria_tabla=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoria_tabla.xview)
        scrolly.config(command=self.categoria_tabla.yview)

        self.categoria_tabla.heading("cid",text="Categoria ID")
        self.categoria_tabla.heading("name",text="Nombre")
        self.categoria_tabla["show"]="headings"
        self.categoria_tabla.column("cid",width=5)
        self.categoria_tabla.column("name",width=100)
        self.categoria_tabla.pack(fill=BOTH,expand=1)

        self.categoria_tabla.bind("<ButtonRelease-1>",self.get_data)

        #imagenes
        self.im1=Image.open("img/cat.jpg")
        self.im1=self.im1.resize((500,250),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("img/category.jpg")
        self.im2=self.im2.resize((500,250),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)

        self.show()

    #Funciones
    def add(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Nombre de Categoria debe ser requerido",parent=self.root)
            else:
                cur.execute("Select * from categoria where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","La categoria ya esta registrada, prueba una diferente",parent=self.root)
                else:
                    cur.execute("Insert into categoria (name) values(?)",(
                                    self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Exito","Categoria Agregada con exito!",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select * from categoria")
            rows=cur.fetchall()
            self.categoria_tabla.delete(*self.categoria_tabla.get_children())
            for row in rows:
                self.categoria_tabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.categoria_tabla.focus()
        content=(self.categoria_tabla.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="Seleccionar":
                messagebox.showerror("Error","Seleccione una categoria de la lista.",parent=self.root)
            else:
                cur.execute("Select * from categoria where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, seleccione una categoria.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirmar","Estas seguro de eliminar esta factura?",parent=self.root)
                    if op==True:
                        cur.execute("delete from categoria where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Eliminado","Categoria Eliminada con Exito!",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



if __name__ == '__main__':
    root=Tk()
    obj=categoriaClass(root)
    root.mainloop()