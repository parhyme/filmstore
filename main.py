import flask ,flask.views
from flask import *
import os
from pyodbc import *
from werkzeug import secure_filename


app = flask.Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "bacon"
users = {'jake':'bacon'}

DEBUG = True

app.config['UPLOAD_FOLDER'] = 'E:/university/terme_8/Az_database/proje/db/static/img'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#SQLSERVER configurations
connection = connect(Driver='{SQL Server}',
                                Server='HAJIHOSSEINI\NEWSQLEXPRESS',
                                Database='azdb',
                                uid='sa',pwd='1234')
cursor = connection.cursor()


#------------------------------- function -------------------------------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def valifation(a):
    result = 0
    for i in range(len(a)):
        j = ord(a[i])
        if (64<j<91 or 96<j<123):
            pass
        else:
            result = 1
            break
    return result
#------------------------------- Main -------------------------------------

class Main(flask.views.MethodView):

        def get(self):
                return flask.render_template('main.html')


        def post(self):
                if 'signin' in flask.request.form:

                        username = flask.request.form['username']
                        password = flask.request.form['password']
                        flask.session['username'] = username

                        SQLCommand = ("SELECT password FROM Users WHERE userName='%s'" %(username))
                        cursor.execute(SQLCommand)
                        row = cursor.fetchone()
                        connection.commit()
                        if row:
                            if row[0]==password :

                                    username=flask.session['username']
                                    return flask.redirect(flask.url_for('home'))
                            else:
                                    return flask.redirect(flask.url_for('main'))
                        else:

                            return flask.redirect(flask.url_for('main'))

                if 'signup' :
                        Uname = flask.request.form['uname']
                        passwd = flask.request.form['passwd']
                        c_passwd = flask.request.form['c_passwd']
                        email = flask.request.form['email']
                        flask.session['username'] = Uname

                        if passwd==c_passwd and len(Uname)==8 and len(passwd)>=6:
                                SQLCommand = ("INSERT INTO Users (userName,password,email,roll) VALUES ('%s','%s','%s', '%s')") %(Uname,passwd,email,'0')


                                cursor.execute(SQLCommand)
                                connection.commit()

                                return flask.redirect(flask.url_for('home'))
                        else:

                                return flask.redirect(flask.url_for('main'))

