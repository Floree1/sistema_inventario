import sqlite3
def create_db():
    con=sqlite3.connect(database=r"sistema_inventario.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS empleado(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,adress text,salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS proveedor(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS categoria(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS producto(pid INTEGER PRIMARY KEY AUTOINCREMENT,Proveedor text,Categoria text,name text,price text,cantidad text,status text)")
    con.commit()
create_db()