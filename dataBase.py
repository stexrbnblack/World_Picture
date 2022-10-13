# Importar el módulo sqlite3
import sqlite3
# Importar modulo de error de sqlite3
from sqlite3 import Error
from flask import current_app, g

def sql_connection():
    try:
        if 'con' not in g:
            g.con = sqlite3.connect('Sql_Data.db')
            g.con.row_factory = sqlite3.Row
        return g.con
    except Error:
        print( Error )
"""    try:
        con = sqlite3.connect('Sql_Data.db')
        con.row_factory = sqlite3.Row
        return con
    except Error:
        print(Error)
"""

def sql_connection_img():
    try:
        con = sqlite3.connect("Sql_Data.db")
        con.row_factory = sqlite3.Row
        return con
    except Error:
        print( Error )

def sql_insert_data(Name, ID, Email, Password, Cell_phone, Date_of_Birth):
    #strsql = 'INSERT INTO Sql_Data_web (NAME, ID, EMAIL, PASSWORD, [CELL PHONE], [DATE OF BIRTH]) VALUES (?,?,?,?,?,?);'
    #data= (Name, ID, Email, Password, Cell_phone, Date_of_Birth)

    #strsql = ('INSERT INTO Sql_Data_web ("NAME", "ID", "EMAIL", "PASSWORD", "[CELL PHONE]", "[DATE OF BIRTH]") VALUES(%?, %?, %?, %?, %?, %?);', (Name , ID , Email , Password , Cell_phone, Date_of_Birth))
    #data = Name , ID , Email , Password , Cell_phone , Date_of_Birth 
    
    strsql = "INSERT INTO Sql_Data_web (NAME, ID, EMAIL, PASSWORD, [CELL PHONE], [DATE OF BIRTH]) VALUES('" + Name + "' , '" + ID + "' , '" + Email + "' , '" + Password + "' , '" + Cell_phone + "' , '" + Date_of_Birth + "');"    
    print("strsql : " + strsql )
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_select_busquedaSql (Email, Password):
    #strsql = 'SELECT * FROM usuario WHERE usuario = ? AND contraseña = ?', (Email, Password)
    
    strsql = "SELECT Email, Password FROM Sql_Data_web WHERE EMAIL  = '" + Email + "' And PASSWORD = '" + Password + "';"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    busquedaSql = cursorObj.fetchall()
    con.close()
    return busquedaSql


def sql_edit_producto(New2_Password, email):
    print("id = " , email)
    strsql = "UPDATE Sql_Data_web SET PASSWORD = " + New2_Password + " WHERE EMAIL = " + email + ";"
    print(strsql)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_delete_producto(id):
    strsql = "DELETE FROM Sql_Data_web WHERE id = " + id + ";"	
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()


# def sql_insert_producto2(id, nombre,precio,cantidad):
#     #strsql = "INSERT INTO producto (id, nombre, precio,existencia) VALUES(" + id + ", '" + nombre + "', " + precio + " , " +cantidad + ");"    
#     #print("strsql : " + strsql )
#     strsql= ('INSERT INTO producto (id, nombre, precio, existencia) VALUES (?,?,?,?)',(id,nombre, precio, cantidad)) # opcion2
#     #print("strsql : " + strsql )
#     con = sql_connection()
#     cursorObj = con.cursor()
#     cursorObj.execute(strsql)
#     con.commit()
#     con.close()