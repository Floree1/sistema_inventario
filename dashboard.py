
from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from empleados import empleadosClass
from proveedor import proveedorClass
from categoria import categoriaClass
from productos import productosClass
from ventas import ventasClass


from tkinter import messagebox
import sqlite3
import os
import time

#Version aplicacion
version_app="0.9.1b"
class SistemaInventario:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Sistema de inventario | Desarrollado por Mauro Flores")
        self.root.config(bg="white")

        #Title
        #self.icon_title=PhotoImage(file="D:/projects/01_SystemInventory/img/logo1.png")
        self.icon_title=PhotoImage(file="img/logo1.png")
        title=Label(self.root,text="Sistema de inventario",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#910005",fg="white",anchor="w",padx=40).place(x=0,y=00,relwidth=1,height=80)

        #btn_logout
        btn_logout=Button(self.root,text="Cerrar Sesion",command=self.logout,font=("time new roman",15,"bold"),bg="yellow",cursor="hand2").pack(padx=25, side=TOP, anchor=SE, pady=20)
        #Reloj
        self.lbl_clock=Label(self.root,text="Bienvenido al Sistema de inventario\t\t Día: DD/MM/AAAA\t\t Hora: HH:MM:SS",font=("times new roman",15),bg="#8c8c8c",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #NavBar Left
        #self.MenuLogo=Image.open("D:/projects/01_SystemInventory/img/menu_im.png")
        self.MenuLogo=Image.open("img/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE, bg="white")
        LeftMenu.place(x=0,y=100,width=200,height=470)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        #Imagenes Dashboard
        #self.icon_side=PhotoImage(file="D:/projects/01_SystemInventory/img/side.png")
        self.icon_side=PhotoImage(file="img/side.png")
        self.icon_home=PhotoImage(file="img/home.png")

        lbl_menu=Label(LeftMenu,text="Menu",image=self.icon_home,compound=LEFT,padx=5,anchor="w",font=("times new roman",20),bg="#009688").pack(side=TOP, fill=X)
        btn_empleado=Button(LeftMenu,text="Empleados",command=self.empleados,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_proveedor=Button(LeftMenu,text="Proveedor",command=self.proveedor,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_categoria=Button(LeftMenu,text="Categorias",command=self.categoria,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_producto=Button(LeftMenu,text="Productos",command=self.producto,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_ventas=Button(LeftMenu,text="Ventas",command=self.ventas,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)
        btn_salir=Button(LeftMenu,text="Salir",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",15,"bold"),bg="white",bd=1,cursor="hand2").pack(side=TOP, fill=X)

        #Dashboard
        self.lbl_empleado=Label(self.root, text="Empleados\n [ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("times new roman",20,"bold"))
        self.lbl_empleado.place(x=300, y=120, height=150,width=300)

        self.lbl_provedor=Label(self.root, text="Total de Proveedores\n [ 0 ]",bd=5,relief=RIDGE,bg="#ff6a00",fg="white",font=("times new roman",20,"bold"))
        self.lbl_provedor.place(x=650, y=120, height=150,width=300)

        self.lbl_categoria=Label(self.root, text="Total de Categorias\n [ 0 ]",bd=5,relief=RIDGE,bg="#ff2130",fg="white",font=("times new roman",20,"bold"))
        self.lbl_categoria.place(x=1000, y=120, height=150,width=300)

        self.lbl_producto=Label(self.root, text="Total de Productos\n [ 0 ]",bd=5,relief=RIDGE,bg="#0d45ff",fg="white",font=("times new roman",20,"bold"))
        self.lbl_producto.place(x=300, y=300, height=150,width=300)

        self.lbl_ventas=Label(self.root, text="Total de Ventas\n [ 0 ]",bd=5,relief=RIDGE,bg="#008a05",fg="white",font=("times new roman",20,"bold"))
        self.lbl_ventas.place(x=650, y=300, height=150,width=300)


        #Footer
        lbl_footer=Label(self.root,text=f"Sistema de inventario {version_app} | Developed by Mauro Flores\n Por cualquier problema técnico contactar: 123xxxxx9",font=("times new roman",15),bg="#8c8c8c",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()



    def empleados(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=empleadosClass(self.new_win)
        
    def proveedor(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=proveedorClass(self.new_win)

    def categoria(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoriaClass(self.new_win)

    def producto(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productosClass(self.new_win)

    def ventas(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ventasClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select * from producto")
            producto=cur.fetchall()
            self.lbl_producto.config(text=f"Total de Productos\n [ {str(len(producto))} ]")

            cur.execute("select * from proveedor")
            proveedor=cur.fetchall()
            self.lbl_provedor.config(text=f"Total de Proveedores\n [ {str(len(proveedor))} ]")
            
            cur.execute("select * from categoria")
            categoria=cur.fetchall()
            self.lbl_categoria.config(text=f"Total de Categorias\n [ {str(len(categoria))} ]")
            
            cur.execute("select * from empleado")
            empleado=cur.fetchall()
            self.lbl_empleado.config(text=f"Empleados\n [ {str(len(empleado))} ]")

            bill=len(os.listdir('ventas'))
            self.lbl_ventas.config(text=f"Total de Ventas\n [ {str(bill)} ]")


            time_=time.strftime("%H:%M:%S")
            date_=time.strftime("%d/%m/%Y")
            self.lbl_clock.config(text=f"Bienvenido al Sistema de inventario\t\t Día: {str(date_)}\t\t Hora: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

        




if __name__ == '__main__':
    root=Tk()
    obj=SistemaInventario(root)
    root.mainloop()