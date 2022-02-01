#from multiprocessing import parent_process
from cgitb import text
import fractions
from multiprocessing import Process
from tkinter import *
from tkinter import font
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import os

class ventasClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sistema de inventario | Ventas")
        self.root.config(bg="white")
        self.root.focus_force


        self.bill_list=[]
        self.var_facturacion=StringVar()

        #Title
        lbl_title=Label(self.root,text="Área de facturación de clientes",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)


        lbl_facturacion=Label(self.root,text="Factura N°",font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_facturacion=Entry(self.root,textvariable=self.var_facturacion,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Buscar",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_search=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=490,y=100,width=120,height=28)

        ventas_frame=Frame(self.root,bd=3,relief=RIDGE)
        ventas_frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(ventas_frame,orient=VERTICAL)
        self.Ventas_List=Listbox(ventas_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Ventas_List.yview)
        self.Ventas_List.pack(fill=BOTH,expand=1)
        self.Ventas_List.bind("<ButtonRelease-1>",self.get_data)


        #Area de ventas

        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,width=410,height=330)
        
        lbl_title2=Label(bill_frame,text="Facturación de clientes",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)


        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area=Text(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #imagenes

        self.bill_photo=Image.open("img/cat2.jpg")
        self.bill_photo=self.bill_photo.resize((450,300),Image.ANTIALIAS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        lbl_imagen=Label(self.root,image=self.bill_photo,bd=0)
        lbl_imagen.place(x=700,y=110)

        self.show()

        #funciones
    def show(self):
        del self.bill_list[:]
        self.Ventas_List.delete(0,END)
        for i in os.listdir('ventas'):
            if i.split('.')[-1]=='txt':
                self.Ventas_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.Ventas_List.curselection()
        file_name=self.Ventas_List.get(index_)
        #print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'ventas/{file_name}',"r")

        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_facturacion.get()=="":
            messagebox.showerror("Error","Ingrese N° de Facturacion.",parent=self.root)
        else:
            if self.var_facturacion.get() in self.bill_list:
                fp=open(f'ventas/{self.var_facturacion.get()}.txt',"r")
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","N° de Facturacion Invalida",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)



if __name__ == '__main__':
    root=Tk()
    obj=ventasClass(root)
    root.mainloop()