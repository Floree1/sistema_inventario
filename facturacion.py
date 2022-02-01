from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

#Version aplicacion
version_app="0.9.1b"
class FacturacionClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Sistema de inventario | Desarrollado por Mauro Flores")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        #Title
        #self.icon_title=PhotoImage(file="D:/projects/01_SystemInventory/img/logo1.png")
        self.icon_title=PhotoImage(file="img/logo1.png")
        title=Label(self.root,text="Area de Facturacion",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#910005",fg="white",anchor="w",padx=40).place(x=0,y=00,relwidth=1,height=80)

        #btn_logout
        btn_logout=Button(self.root,text="Cerrar Sesion",command=self.logout,font=("time new roman",15,"bold"),bg="yellow",cursor="hand2").pack(padx=25, side=TOP, anchor=SE, pady=20)
        #Reloj
        self.lbl_clock=Label(self.root,text="Bienvenido al Sistema de inventario\t\t Día: DD-MM-AAAA\t\t Hora: HH:MM:SS",font=("times new roman",15),bg="#8c8c8c",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #Ventana de productos

        ProductoFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductoFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductoFrame1,text="Todos los productos",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #Product search frame 
        self.var_search=StringVar()
        ProductoFrame2=Frame(ProductoFrame1,bd=2,relief=RIDGE,bg="white")
        ProductoFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductoFrame2,text="Busqueda de Producto",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_name=Label(ProductoFrame2,text="Producto:",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_name=Entry(ProductoFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=95,y=47,width=150,height=22)

        btn_search=Button(ProductoFrame2,text="Buscar",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=260,y=45,width=130,height=25)
        btn_show_all=Button(ProductoFrame2,text="Mostrar Todo",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=260,y=10,width=130,height=25)


        #Productos
        cartFrame=Frame(ProductoFrame1,bd=3,relief=RIDGE)
        cartFrame.place(x=2,y=140,width=395,height=385)

        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)

        self.producto_tabla=ttk.Treeview(cartFrame,columns=("pid","name","price","cantidad","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.producto_tabla.xview)
        scrolly.config(command=self.producto_tabla.yview)

        self.producto_tabla.heading("pid",text="PID")
        self.producto_tabla.heading("name",text="Producto")
        self.producto_tabla.heading("price",text="Precio")
        self.producto_tabla.heading("cantidad",text="Cantidad")
        self.producto_tabla.heading("status",text="Estado")

        self.producto_tabla["show"]="headings"

        self.producto_tabla.column("pid",width=25)
        self.producto_tabla.column("name",width=115)
        self.producto_tabla.column("price",width=90)
        self.producto_tabla.column("cantidad",width=50)
        self.producto_tabla.column("status",width=60)
        self.producto_tabla.pack(fill=BOTH,expand=1)

        self.producto_tabla.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductoFrame1,text="*Nota: 'Cantidad=0 para eliminar un producto del carro'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)    


        #Cart Frame
        self.var_cname=StringVar()
        self.var_contacto=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Detalles del cliente",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Nombre",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

        lbl_contacto=Label(CustomerFrame,text="Contacto",font=("times new roman",15),bg="white").place(x=280,y=35)
        txt_contacto=Entry(CustomerFrame,textvariable=self.var_contacto,font=("times new roman",13),bg="lightyellow").place(x=360,y=35,width=140)

        #Cal Cart Frame
        Cal_Cart_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #Calculadora Frame
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)


        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("arial",15,"bold"),width="21",bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=("arial",15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=("arial",15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=("arial",15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=("arial",15,"bold"),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=("arial",15,"bold"),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=("arial",15,"bold"),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=("arial",15,"bold"),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_res=Button(Cal_Frame,text='-',font=("arial",15,"bold"),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=("arial",15,"bold"),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=("arial",15,"bold"),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=("arial",15,"bold"),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=("arial",15,"bold"),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_c=Button(Cal_Frame,text='C',font=("arial",15,"bold"),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_0=Button(Cal_Frame,text='0',font=("arial",15,"bold"),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=("arial",15,"bold"),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=("arial",15,"bold"),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)





        cartFrame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cartFrame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cartFrame,text="\tCantidad de Productos: [0]",font=("goudy old style",11),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)

        self.cartTabla=ttk.Treeview(cartFrame,columns=("pid","name","price","cantidad"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTabla.xview)
        scrolly.config(command=self.cartTabla.yview)

        self.cartTabla.heading("pid",text="PID")
        self.cartTabla.heading("name",text="Nombre Completo")
        self.cartTabla.heading("price",text="Precio")
        self.cartTabla.heading("cantidad",text="Cantidad")

        self.cartTabla["show"]="headings"

        self.cartTabla.column("pid",width=30)
        self.cartTabla.column("name",width=100)
        self.cartTabla.column("price",width=90)
        self.cartTabla.column("cantidad",width=60)

        self.cartTabla.pack(fill=BOTH,expand=1)
        self.cartTabla.bind("<ButtonRelease-1>",self.get_data_cart)


        #Cart Frame 2
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_cantidad=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Add_CartWidgetFrame.place(x=420,y=550,width=530,height=110)
        
        #row
        p_name=Label(Add_CartWidgetFrame,text="Nombre del Producto",font=("times new roman",15),bg="white").place(x=5,y=5)
        text_p_name=Entry(Add_CartWidgetFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        p_price=Label(Add_CartWidgetFrame,text="Precio",font=("times new roman",15),bg="white").place(x=230,y=5)
        text_p_price=Entry(Add_CartWidgetFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        p_cantidad=Label(Add_CartWidgetFrame,text="Cantidad",font=("times new roman",15),bg="white").place(x=390,y=5)
        text_p_cantidad=Entry(Add_CartWidgetFrame,textvariable=self.var_cantidad,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=100,height=22)

        #row2
        self.lbl_inStock=Label(Add_CartWidgetFrame,text="En Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetFrame,text="Vaciar",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetFrame,text="Agregar | Actualizar",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)


        #Billing area

        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=410,height=410)

        bTitle=Label(billFrame,text="Área de facturación del cliente",font=("goudy old style",15,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)


        #Billing Buttons

        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)


        self.lbl_amnt=Label(billMenuFrame,text="Total\n",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Descuento\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Total Neto\n",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        #####

        btn_print=Button(billMenuFrame,text="Imprimir",command=self.print_bill,cursor="hand2",font=("goudy old style",11,"bold"),bg="green",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Vaciar\nTodo",command=self.clear_all,cursor="hand2",font=("goudy old style",11,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_gennerate=Button(billMenuFrame,text="Generar/Guardar\nFactura",command=self.generate_bill,cursor="hand2",font=("goudy old style",11,"bold"),bg="#009688",fg="white")
        btn_gennerate.place(x=246,y=80,width=160,height=50)





        #Footer
        footer=Label(self.root,text=f"Sistema de inventario {version_app} | Developed by Mauro Flores\n Por cualquier problema técnico contactar: 123xxxxx9",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        self.update_date_time()

        #Todas las funciones

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,cantidad,status from producto where status='Activo'")
            rows=cur.fetchall()
            self.producto_tabla.delete(*self.producto_tabla.get_children())
            for row in rows:
                self.producto_tabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



    def search(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror('Error',"Ingrese un tipo de busqueda.",parent=self.root)

            else:
                cur.execute("select pid,name,price,cantidad,status from producto where name LIKE '%"+self.var_search.get()+"%' and status='Activo'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.producto_tabla.delete(*self.producto_tabla.get_children())
                    for row in rows:
                        self.producto_tabla.insert("",END,values=row)
                else:
                    messagebox('Error',"Es una funcion de busqueda!",parent=self.root)

        except Exception as ex:
            messagebox.showerror('Error',f"Error debido a: {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.producto_tabla.focus()
        content=(self.producto_tabla.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"En Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_cantidad.set('1')


    def get_data_cart(self,ev):
        f=self.cartTabla.focus()
        content=(self.cartTabla.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_cantidad.set(row[3])
        self.lbl_inStock.config(text=f"En Stock [{str(row[4])}]")
        self.var_stock.set(row[4])



    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Por favor seleccione un producto de la lista.",parent=self.root)
        elif self.var_cantidad.get()=='':
            messagebox.showerror('Error',"Se require cantidad.",parent=self.root)
        elif int(self.var_cantidad.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Cantidad incorreta.",parent=self.root)
        else:
            #price_cal=int(self.var_cantidad.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_cantidad.get(),self.var_stock.get()]
            #self.cart_list.append(cart_data)
            #Update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirma',"Producto presente en lista, desea actualizar | eliminar de la lista del carrito")
                if op==True:
                    if self.var_cantidad.get()=='0':
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal # precio
                        self.cart_list[index_][3]=self.var_cantidad.get() # cantidad
            else:
                self.cart_list.append(cart_data)

            #self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()


    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.descuento=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

        self.descuento=(self.bill_amnt*5)/100            
        self.net_pay=self.bill_amnt-self.descuento
        self.lbl_amnt.config(text=f'Total\n$ {str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Total Neto\n$ {str(self.net_pay)}')

        self.cartTitle.config(text=f"\tCantidad de Productos: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.cartTabla.delete(*self.cartTabla.get_children())
            for row in self.cart_list:
                self.cartTabla.insert("",END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)




    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contacto.get()=='':
            messagebox.showerror('Error',"Detalles del cliente son requerido.",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror('Error',"Por favor agrega un producto.")

        else:
            #--Billtop--
            self.bill_top()
            #--BillMiddle--
            self.bill_middle()
            #--BillBottom--
            self.bill_bottom()

            fp=open(f'ventas/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Guardado',"Factura generada y guardada.",parent=self.root)
            self.chk_print=1
            


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tNombre del Negocio
\t Telefono. 98725***** , Suipacha, 771
{str("="*47)}
 Nombre del Cliente: {self.var_cname.get()}
 Telefono. :{self.var_contacto.get()}
 Factura N°. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Producto\t\t\tCantidad\tPrecio
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Total a pagar\t\t\t\t$ {self.bill_amnt}
 Descuento\t\t\t\t$ {self.descuento}
 Total neto\t\t\t\t$ {self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str('='*47)}
Total de la factura\t\t\t\t$ {self.bill_amnt}
Descuento (%5)\t\t\t\t$ {self.descuento}
Total Neto\t\t\t\t$ {self.net_pay}
{str('='*47)}\n        
        '''
        
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
    def bill_middle(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                cantidad=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactivo'
                if int(row[3])!=int(row[4]):
                    status='Activo'

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\t$ "+price)
                #===Actualiza la cantidad de Stock=====
                cur.execute('Update producto set cantidad=?,status=? where pid=?',(
                    cantidad,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)



    def clear_cart(self):
        
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_cantidad.set('')
        self.lbl_inStock.config(text=f"En Stock")
        self.var_stock.set('')


    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contacto.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"\tCantidad de Productos: [0]")
        self.var_search.set('')
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()


    def update_date_time(self):
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d/%m/%Y")
        self.lbl_clock.config(text=f"Bienvenido al Sistema de inventario\t\t Día: {str(date_)}\t\t Hora: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Imprimiendo...',"Por favor espere mientras imprime el recibo.",parent=self.root)
            new_file=tempfile.mkdtemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Error',"Por favor generar la factura para imprimir el recibo",parent=self.root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")

        



if __name__ == '__main__':
    root=Tk()
    obj=FacturacionClass(root)
    root.mainloop()