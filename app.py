#from crypt import methods
import os
from re import X
import functools
from copy import error
from email import message_from_binary_file
from symbol import except_clause
import flask
from flask import Flask, g, render_template, flash, redirect, url_for, request, jsonify, session, send_file, send_from_directory, make_response
from formularios import FormInicio, FormForgetPassword, FormUserNew
from settings.config import configuracion
from wtforms import StringField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from dataBase import sql_select_busquedaSql, sql_insert_data, sql_connection, sql_connection_img, sql_edit_producto
import yagmail as yagmail
import utils


import urllib.request
from werkzeug.utils import secure_filename

from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config.from_object(configuracion)
app.secret_key = os.urandom( 24 )

UPLOAD_FOLDER = os.path.abspath("static/uploads/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['UPLOAD_IMAG']= ('static/upimag/')

#UPLOAD_FOLDER = 'static/uploads/'
#app.secret_key = "cairocoders-ednalan"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set (['png', 'jpg', 'jpeg', 'gif'])


@app.route( '/' )
def index():
    if g.user:
        return redirect(url_for('HomePage'))    
    return redirect(url_for( 'logi' ))

@app.route('/UserNew', methods = ['GET', 'POST'])
def UserNew():
    
    try:
        if g.user:
            return redirect(url_for('HomePage'))

        if request.method == 'POST':
            
            username = request.form['Full_Name']
            cellPhone = request.form['Cell_Phone']
            userId = request.form['ID']
            email = request.form['Email']
            password = request.form['Password']
            repeatPassword = request.form['Repeat_Password']
            date = request.form['Date']

            con = sql_connection()
            error = None

            if not utils.isUsernameValid(username):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
                return render_template('UserNew.html')

            if not utils.isPasswordValid(password):
                error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número, un caracter especial y 8 caracteres'
                flash(error)
                return render_template('UserNew.html')
            
            if not password == repeatPassword:
                error = 'El password no conincide'
                flash(error)
                return render_template('UserNew.html')

            if not utils.isEmailValid(email):
                error = 'Correo invalido'
                flash(error)
                return render_template('UserNew.html')

            if con.execute('SELECT * FROM Sql_Data_web WHERE EMAIL = ?', (email,)).fetchone() is not None:
                error = 'El correo ya existe'.format(email)
                flash(error)
                return render_template('UserNew.html')

            con.execute(
                'INSERT INTO Sql_Data_web (NAME, ID, EMAIL, PASSWORD, [CELL PHONE], [DATE OF BIRTH]) VALUES (?,?,?,?,?,?)',
                (username , userId , email , generate_password_hash(password) , cellPhone, date)
            )
            con.commit()
            con.close()

            flash('Revisa tu correo para activar tu cuenta')
            return redirect('logi')
        return render_template('UserNew.html')
    except:
        return render_template('UserNew.html')
    


@app.route('/logi', methods = ['GET', 'POST'])
def logi():
        
    try:
        if g.user:
            return redirect(url_for('HomePage'))    

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            con = sql_connection()
            error = None
            if not email:
                error = 'Debes ingresar el EMAIL'
                flash( error )
                return render_template( 'logi.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'logi.html' )

            user = con.execute(
                'SELECT * FROM Sql_Data_web WHERE EMAIL = ? AND PASSWORD = ?', (
                    email, password)
            ).fetchone()

            if user is None:
                user = con.execute(
                    'SELECT * FROM Sql_Data_web WHERE EMAIL = ?', (email,)
                ).fetchone()
                if user is None:
                    error = 'Email no existe'
                else:
                    # Validar contraseña hash
                    store_password = user[3]
                    result = check_password_hash(store_password, password)
                    if result is False:
                        error = 'Contraseña inválida'
                    else:
                        session.clear()
                        session['email'] = user[2]
                        resp = make_response(redirect(url_for('HomePage')))
                        resp.set_cookie('EMAIL', email)
                        return resp
                    flash(error)
            else:
                session.clear()
                session['email'] = user[2]
                return redirect(url_for('HomePage'))
            flash(error)
            con.close()
        return render_template('logi.html')
    except Exception as e:
        print(e)
        return render_template('logi.html', titulo='Iniciar Sesión')


@app.route('/ForgetPassword', methods = ['GET', 'POST'])
def ForgetPassword():
    form = FormForgetPassword()
    if (form.validate_on_submit()):
        flash('Inicio de sesión solicitado por el email {}, Password {}'.format(form.email.data,
        form.Cell_Phone.data))

        if request.method == "POST":
            email = request.form["email"]
            Cell_Phone = request.form["Cell_Phone"]
            New2_Password = request.form['New2_Password']
            Confirm2_Password = request.form['Confirm2_Password']

            con = sql_connection()
            error = None
            if not email:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'ForgetPassword.html' )

            if not Cell_Phone:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'ForgetPassword.html' )

            buscarSql = sql_select_busquedaSql (email, Cell_Phone)

            if not buscarSql :
                error = 'Debes ingresar el usuario'
                flash( error )
                flash(message='Se requiere que completes este campo')
                return redirect(url_for('ForgetPassword', buscarSql=buscarSql))
            else:
                
                if not New2_Password == Confirm2_Password:
                    error = 'El password no conincide'
                    flash(error)
                    return render_template('UserNew.html')

                if not utils.isPasswordValid(New2_Password):
                    error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número, un caracter especial y 8 caracteres'
                    flash(error)
                    return render_template('UserNew.html')

            con.execute(
                'UPDATE Sql_Data_web SET PASSWORD = (?) WHERE EMAIL = (?)   ',
                (New2_Password, email)
            )
            con.commit()
            con.close()
            
            return redirect(url_for('logi'))

        return redirect(url_for('UserNew'))

    return render_template('ForgetPassword.html', titulo='Iniciar Sesión', form=form)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('logi'))

        return view(**kwargs)

    return wrapped_view


@app.route('/HomePage')
@login_required
def HomePage():
    return render_template( 'HomePage.html' )

@app.route('/UserProfile')
@login_required
def UserProfile():
    con = sql_connection_img()
    cur=con.cursor()
    cur.execute("select * from image")
    data=cur.fetchall()
    data=list(reversed(data))
    con.close()

    return render_template( 'UserProfile.html', data=data)
    #return redirect(url_for('UserProfile'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/downloadimage', methods=('GET', 'POST'))

def downloadimage():
    return send_file("resources/image.png", as_attachment=True)



def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    if request.method == "POST":
        if "ourfile" not in request.files:
            return "The form has no file part" 
        f = request.files["ourfile"]
        if f.filename == "":
            return "No file selected."
        if f and allowed_file(f.filename):    
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("get_file",filename=filename))
        return "File not allowed."

    return render_template ("upload.html")
    """
<form method="POST" enctype="multipart/form-data">
<input type="file" name="ourfile">
<input type="submit"  value="UPLOAD">
</form>    
"""

@app.route("/uploads/<filename>")
@login_required
def get_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




con=sql_connection_img()
con.execute("create table if not exists image(pid integer primary key,img TEXT)")
con.close()

@app.route("/upImagView",methods=['GET','POST'])
@login_required
def upImagView():

    con = sql_connection_img()
    
    cur = con.cursor()
    cur.execute("select * from image")
    data = cur.fetchall()
    con.close()

    if request.method=='POST':
        upload_image=request.files['upload_image']

        if upload_image.filename!='':
            filename = secure_filename(upload_image.filename)
            filepath=os.path.join(app.config['UPLOAD_IMAG'],filename)
            upload_image.save(filepath)
            con=sql_connection_img()
            cur=con.cursor()
            cur.execute("insert into image(img)values(?)",(upload_image.filename,))
            con.commit()
            flash("File Upload Successfully","success")

            con = sql_connection_img()
            cur=con.cursor()
            cur.execute("select * from image")
            data=cur.fetchall()
            data=list(reversed(data))
            con.close()
            return render_template("UserProfile.html",data=data)
    return render_template("upImagView.html ",data=data)

@app.route('/delete_record/<string:id>')
@login_required
def delete_record(id):
    try:
        con=sql_connection_img()
        cur=con.cursor()
        cur.execute("delete from image where pid=?",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        con.close()
        return redirect(url_for("upImagView"))

        
@app.route('/upProfile',methods=['GET','POST'])

def upProfile():

    if request.method=='POST':
        
        name = request.form['nameprofile']
        txt = request.form['profile']
        imag=request.files['imagprofile']

        con = sql_connection()
        error = None
        if not name:
            error = 'You must insert Profile Name'
            flash( error )
            return render_template( 'upProfile.html' )
        if not txt:
            error = 'You must insert Profile Text'
            flash( error )
            return render_template( 'upProfile.html' )
        if not imag:
            error = 'You should upload a Profile picture'
            flash(error)
            return render_template ('upProfile.html')

        if imag.filename !='':
            filename = secure_filename(imag.filename)
            filepath=os.path.join(app.config['UPLOAD_IMAG'],filename)
            imag.save(filepath) 
            con=sql_connection_img()
            cur=con.cursor()
            cur.execute(
                'INSERT INTO blog_Profile (NAME_id, Blog_profile, imag_profile) VALUES (?,?,?)',
                (name , txt , imag.filename)
                )
            con.commit()
            flash("File Upload Successfully","success")

            con = sql_connection_img()
            cur=con.cursor()
            cur.execute("select * from blog_Profile")
            data=cur.fetchall()
            data=list(reversed(data))
            con.close()
            return render_template("UserProfile.html")

    return render_template("upProfile.html")


@app.before_request
def load_logged_in_user():
    con = sql_connection()
    user_id = session.get('email')

    if user_id is None:
        g.user = None
    else:
        g.user = con.execute(
            'SELECT * FROM Sql_Data_web WHERE EMAIL = ?', (user_id,)
        ).fetchone()

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('logi'))

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)





