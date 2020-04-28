import flask ,flask.views
from flask import *
import os
from pyodbc import *


app = flask.Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "prhm"
users = {'prhm':'abp'}

DEBUG = True

app.config['UPLOAD_FOLDER'] = 'E:/university/terme_8/Az_database/proje/db/static/img'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#SQLSERVER configurations
# connection = connect(Driver='{SQL Server}',
#                                 Server='PARHAM\',
#                                 Database='azdb',
#                                 uid='sa',pwd='1234')
# cursor = connection.cursor()


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
                                # SQLCommand = ("INSERT INTO Users (userName,password,email,roll) VALUES ('%s','%s','%s', '%s')") %(Uname,passwd,email,'0')


                                cursor.execute(SQLCommand)
                                connection.commit()

                                return flask.redirect(flask.url_for('home'))
                        else:

                                return flask.redirect(flask.url_for('main'))

class Home(flask.views.MethodView):
        def get(self):
                # username = flask.session['username']
                # SQLCommand = ("SELECT roll,userId FROM Users where userName='%s'")%(username)
                # cursor.execute(SQLCommand)
                # row = cursor.fetchall()
                # connection.commit()

                # flask.session['roll'] = row[0][0]


                # SQLCommand = ("spDisplayHomePageBASedONFollow '%s',3")%(row[0][1])
                # cursor.execute(SQLCommand)
                # row = cursor.fetchall()
                # connection.commit()

                result = []

                for i in range(len(row)):
                    a=[]

                #     SQLCommand = ("SELECT name , family FROM Writers where writerId='%s'")%(row[i][1])
                #     cursor.execute(SQLCommand)
                #     wr = cursor.fetchall()
                #     connection.commit()



                #     SQLCommand = ("SELECT name , family FROM Directors where directorId='%s'")%(row[i][2])
                #     cursor.execute(SQLCommand)
                #     dr = cursor.fetchall()
                #     connection.commit()


                #     SQLCommand = ("SELECT companyName from Companies where companyId='%s'")%(row[i][3])
                #     cursor.execute(SQLCommand)
                #     co = cursor.fetchall()
                #     connection.commit()


                #     SQLCommand = ("SELECT categoryName from Categories where categoryId='%s'")%(row[i][4])
                #     cursor.execute(SQLCommand)
                #     ca = cursor.fetchall()
                #     connection.commit()


                    a.append(wr[0][0])
                    a.append(wr[0][1])
                    a.append(dr[0][0])
                    a.append(dr[0][1])
                    a.append(co[0][0])
                    a.append(ca[0][0])
                    a.append(row[i][5])
                    a.append(row[i][6])
                    a.append(row[i][7])
                    a.append(row[i][8])

                    x = dict ([('wrName',a[0]),('wrFamily',a[1]),('drName',a[2]),('drFamily',a[3]),('company',a[4]),('category',a[5]),('Name',a[6]),('summary',a[7]),('date',a[8]),('image',a[9])])


                    result.append(x)


                if flask.session['username']:
                        return flask.render_template('home.html',posts = result)

                else:
                        return flask.render_template('main.html')


        def post(self):
                if 'logout':
                        flask.session.pop('username',None)
                        return flask.redirect(flask.url_for('main'))

app.add_url_rule('/',
    view_func = Main.as_view('main'),
    methods = ["GET","POST"])

app.add_url_rule('/home/',
    view_func = Home.as_view('home'),
    methods = ["GET","POST"])
