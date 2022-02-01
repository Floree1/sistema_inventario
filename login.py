from tkinter import *
from tkinter import font
from turtle import title
from PIL import ImageTk #pip install pillow
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib #pip install smtplib
import time

class Login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("Login Sistema Inventario | Developed Mauro Flores")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        #self.otp=''

        #=====imagenes========
        self.phone_image=ImageTk.PhotoImage(file='img/phone.png')
        self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        self.icon_login=PhotoImage(file="img/login_new.png")

        self.icon_user=PhotoImage(file="img/user.png")
        self.icon_lock=PhotoImage(file="img/lock.png")

        #=====Login_Frame=====        
        self.empleado_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Iniciar Sesión",font=("Elephant",30,"bold"),bg='white').place(x=0,y=30,relwidth=1)


        lbl_user=Label(login_frame,text="Empleado ID",image=self.icon_user,compound=LEFT,anchor="w",font=("Andalus",20),bg='white',fg="#767171").place(x=50,y=100)
        txt_username=Entry(login_frame,textvariable=self.empleado_id,font=("times new roman",13),bg='#ECECEC').place(x=50,y=140,width=250)


        lbl_pass=Label(login_frame,text="Contraseña",image=self.icon_lock,compound=LEFT,anchor="w",font=("Andalus",20),bg='white',fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show='*',font=("times new roman",13),bg='#ECECEC').place(x=50,y=240,width=250)

        #=======Boton Login=========
        #btn_login=Button(login_frame,command=self.login,text="Login",font=("Arial",15),bg='#00B0F0',fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)
        self.icon_login_image=Button(login_frame,command=self.login,image=self.icon_login,bd=0,bg="white").place(x=100,y=300)

    
        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="O",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=150,y=360)

        btn_forget=Button(login_frame,text="Te olvidaste la contraseña\n (DISABLED)",state=DISABLED,command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0).place(x=0,y=390,relwidth=1)

        #=====Register_Frame=====
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        register_frame.place(x=650,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="Developed Mauro Flores",font=("times new roman",13,"bold"),bg="white").place(x=0,y=20,relwidth=1)
        
        #=====Imagenes=========
        self.im1=ImageTk.PhotoImage(file="img/im1.png")
        self.im2=ImageTk.PhotoImage(file="img/im2.png")
        self.im3=ImageTk.PhotoImage(file="img/im3.png")

        self.lbl_change_image=Label(self.root,bg="gray")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animation()
        #self.send_email('xyz')
        #=====Funciones=========
    def animation(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animation)
        
    def login(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.empleado_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"Todos los campos son requeridos!",parent=self.root)
            else:
                cur.execute("select utype from empleado where eid=? AND pass=?",(self.empleado_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"ID o Contraseña son incorretos!",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python facturacion.py")
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)

    
    def forget_window(self):
        con=sqlite3.connect(database=r"sistema_inventario.db")
        cur=con.cursor()
        try:
            if self.empleado_id.get()=="":
                messagebox.showerror('Error',"Empleado ID es requerido.",parent=self.root)
            else:
                cur.execute("select email from empleado where eid=?",(self.empleado_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"ID es incorreto, pruebe nuevamente.",parent=self.root)
                else:
                    #===Recuperacion de contraseña===
                    self.var_otp=StringVar()
                    self.new_pass=StringVar()
                    self.conf_pass=StringVar()

                    #cell send_email_function()
                    self.forget_win=Toplevel(self.root)
                    self.forget_win.title("Recuperar Contraseña")
                    self.forget_win.geometry("400x350+500+100")
                    self.forget_win.focus_force()

                    title=Label(self.forget_win,text="Cambio de Contraseña",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)

                    lbl_reset=Label(self.forget_win,text="Ingrese email ya registrado.",font=("times new roman",15)).place(x=20,y=60)
                    txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                    self.btn_reset=Button(self.forget_win,text="ENVIAR",font=("times new roman",15),bg="lightblue")
                    self.btn_reset.place(x=280,y=100,width=100,height=30)

                    lbl_new_pass=Label(self.forget_win,text="Ingrese nueva contraseña",font=("times new roman",15)).place(x=20,y=160)
                    txt_new_pass=Entry(self.forget_win,textvariable=self.new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                    lbl_conf_pass=Label(self.forget_win,text="Confirmar contraseña.",font=("times new roman",15)).place(x=20,y=225)
                    txt_conf_pass=Entry(self.forget_win,textvariable=self.conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                    self.btn_update=Button(self.forget_win,text="Cambiar",state=DISABLED,font=("times new roman",15),bg="lightblue")
                    self.btn_update.place(x=150,y=300,width=100,height=30)


        except Exception as ex:
            messagebox.showerror("Error",f"Error debido a: {str(ex)}",parent=self.root)
'''
    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        print(self.otp)

'''





root=Tk()
obj=Login_system(root)
root.mainloop()