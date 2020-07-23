import flask ,flask.views
from flask import *
import os
from pyodbc import *


app = flask.Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "prhm"
users = {'prhm':'abp'}

DEBUG = True

app.config['UPLOAD_FOLDER'] = 'C:/Users/Parham/Documents/Dev/Film_store/statics/img'
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

class Actors(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,family,nationality,image FROM Actors")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                act = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Family',row[i][1]),('Nation',row[i][2]),('Image',row[i][3])])
                        act.append(x)

                return flask.render_template('actors.html',posts=act)


        def post(self):
                if 'save' in flask.request.form :
                        name = flask.request.form['Name']
                        family = flask.request.form['Family']
                        nation = flask.request.form['Nation']
                        f = flask.request.files['file']

                        if (f.filename != ""):
                                addres = "E:/university/terme_8/Az_database/proje/db/static/img/Actors/" + str(f.filename)
                                if f and allowed_file(f.filename):
				    filename = secure_filename(f.filename)

                                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/Actors", filename))
                                f.close()

                        filename = secure_filename(f.filename)
                        adr = "../static/img/Actors/"+str(filename)

                        print name
                        print family
                        print nation

                        #if(valifation(name)==0 and valifation(family)==0 and valifation(nation)==0):
                        SQLCommand = ("INSERT INTO Actors (name,family,nationality,image) VALUES ('%s','%s','%s','%s')") %(name,family,nation,str(adr))
                        cursor.execute(SQLCommand)
                        connection.commit()


                        return flask.redirect(flask.url_for('actors'))


                if 'delete' in flask.request.form:
                        actor = flask.request.form['actor']
                        actor = actor.split()
                        if(valifation(actor[0])==0 and valifation(actor[1])==0 and valifation(actor[2])==0):

                                SQLCommand = ("SELECT actorId FROM Actors where name='%s' and family='%s' and nationality='%s'")%(actor[0],actor[1],actor[2])
                                cursor.execute(SQLCommand)
                                acid = cursor.fetchall()
                                connection.commit()

                                SQLCommand = ("DELETE FROM Actors WHERE name='%s' and family='%s' and nationality='%s'")%(actor[0],actor[1],actor[2])
                                cursor.execute(SQLCommand)
                                connection.commit()






                        return flask.redirect(flask.url_for('actors'))


                else:
                        pass

class Writers(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,family,nationality,image FROM Writers")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                writer = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Family',row[i][1]),('Nation',row[i][2]),('Image',row[i][3])])
                        writer.append(x)
                return flask.render_template('writers.html',posts=writer)


        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']
                        family = flask.request.form['Family']
                        nation = flask.request.form['Nation']
                        f = flask.request.files['file']

                        if (f.filename != ""):
                                addres = "E:/university/terme_8/Az_database/proje/db/static/img/Writers/" + str(f.filename)
                                if f and allowed_file(f.filename):
					                    filename = secure_filename(f.filename)

                                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/Writers", filename))
                                f.close()

                        filename = secure_filename(f.filename)
                        adr = "../static/img/Writers/"+str(filename)

                        if(valifation(name)==0 and valifation(family)==0 and valifation(nation)==0):
                                SQLCommand = ("INSERT INTO Writers (name,family,nationality,image) VALUES ('%s','%s','%s','%s')") %(name,family,nation,str(adr))
                                cursor.execute(SQLCommand)
                                connection.commit()


                        return flask.redirect(flask.url_for('writers'))

                if 'delete' in flask.request.form:
                        writer = flask.request.form['writer']
                        writer = writer.split()


                        if(valifation(writer[0])==0 and valifation(writer[1])==0 and valifation(writer[2])==0):

                                SQLCommand = ("SELECT writerId FROM Writers where name='%s' and family='%s' and nationality='%s'")%(writer[0],writer[1],writer[2])
                                cursor.execute(SQLCommand)
                                wrid = cursor.fetchall()
                                connection.commit()


                                SQLCommand = ("DELETE FROM Writers WHERE name='%s' and family='%s' and nationality='%s'")%(writer[0],writer[1],writer[2])
                                cursor.execute(SQLCommand)
                                connection.commit()

                        return flask.redirect(flask.url_for('writers'))

                else:
                        pass

class Directors(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,family,nationality,image FROM Directors")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                director = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Family',row[i][1]),('Nation',row[i][2]),('Image',row[i][3])])
                        director.append(x)
                return flask.render_template('directors.html',posts=director)
        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']
                        family = flask.request.form['Family']
                        nation = flask.request.form['Nation']
                        f = flask.request.files['file']

                        if (f.filename != ""):
                                addres = "E:/university/terme_8/Az_database/proje/db/static/img/Directors/" + str(f.filename)
                                if f and allowed_file(f.filename):
					                    filename = secure_filename(f.filename)

                                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/Directors", filename))
                                f.close()

                        filename = secure_filename(f.filename)
                        adr = "../static/img/Directors/"+str(filename)

                        if(valifation(name)==0 and valifation(family)==0 and valifation(nation)==0):
                                SQLCommand = ("INSERT INTO Directors (name,family,nationality,image) VALUES ('%s','%s','%s','%s')") %(name,family,nation,str(adr))
                                cursor.execute(SQLCommand)
                                connection.commit()


                        return flask.redirect(flask.url_for('directors'))

                if 'delete' in flask.request.form:
                        director = flask.request.form['director']
                        director = director.split()
                        if(valifation(director[0])==0 and valifation(director[1])==0 and valifation(director[2])==0):

                                SQLCommand = ("SELECT directorId FROM Directors where name='%s' and family='%s' and nationality='%s'")%(director[0],director[1],director[2])
                                cursor.execute(SQLCommand)
                                drid = cursor.fetchall()
                                connection.commit()

                                SQLCommand = ("DELETE FROM Directors WHERE name='%s' and family='%s' and nationality='%s'")%(director[0],director[1],director[2])
                                cursor.execute(SQLCommand)
                                connection.commit()


                        return flask.redirect(flask.url_for('directors'))

                else:
                        pass

#------------------------------- Stores -------------------------------------

class Stores(flask.views.MethodView):
        def get(self):
                username = flask.session['username']
                SQLCommand = ("SELECT userId FROM Users where userName='%s'")%(username)
                cursor.execute(SQLCommand)
                user = cursor.fetchall()
                connection.commit()


                SQLCommand = ("SELECT storeId FROM Follows WHERE userId='%s'")%(user[0][0])
                cursor.execute(SQLCommand)
                sid = cursor.fetchall()
                connection.commit()

                a=[]
                for k in range(len(sid)):
                    a.append(sid[k][0])


                SQLCommand = ("SELECT storeId,storeName, image FROM Stores")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                store = []
                for i in range(len(row)):
                        if(row[i][0] not in a):
                                x = dict([('storeId',row[i][0]),('StoreName',row[i][1]),('StoreImage',row[i][2]),('status',1)])
                                store.append(x)
                        else:
                                x = dict([('storeId',row[i][0]),('StoreName',row[i][1]),('StoreImage',row[i][2]),('status',0)])
                                store.append(x)

                return flask.render_template('stores.html',posts=store)
        def post(self):
                username = flask.session['username']
                SQLCommand = ("SELECT userId FROM Users where userName='%s'")%(username)
                cursor.execute(SQLCommand)
                user = cursor.fetchall()
                connection.commit()


                SQLCommand = ("SELECT storeId FROM Stores")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()

                for i in row:
                        if str(i[0]) in flask.request.form:

                                SQLCommand = ("INSERT INTO Follows (storeId,userId) VALUES ('%s','%s')") %(i[0],user[0][0])
                                cursor.execute(SQLCommand)
                                connection.commit()
                                return flask.redirect(flask.url_for('home'))

class Request(flask.views.MethodView):
        def get(self):
                return flask.render_template('request.html')


        def post(self):
                if 'send':
                        name = flask.request.form['name']
                        family = flask.request.form['family']
                        email = flask.request.form['email']
                        phone = flask.request.form['phone']
                        resume = flask.request.form['resume']
                        education = flask.request.form['education']
                        motivation = flask.request.form['motivation']
                        storename = flask.request.form['storename']
                        subject = flask.request.form['subject']
                        f = flask.request.files['file']
                        if (f.filename != ""):
                                addres = "E:/university/terme_8/Az_database/proje/db/static/img/Request/" + str(f.filename)
                                if f and allowed_file(f.filename):
					                    filename = secure_filename(f.filename)

                                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/Request", filename))
                                f.close()

                        filename = secure_filename(f.filename)
                        adr = "../static/img/Request/"+str(filename)
                        SQLCommand = ("INSERT INTO Requests (name,family, email, resume, education, motivation, storeName, subject,storeImage) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')") %(name,family,email,resume,education,motivation,storename,subject,str(adr))
                        cursor.execute(SQLCommand)
                        connection.commit()
                        return flask.redirect(flask.url_for('request'))



class RequestList(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,family, email, resume, education, motivation, storeName, subject FROM Requests")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                request = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Family',row[i][1]),('Email',row[i][2]),('Resume',row[i][3]),('Education',row[i][4]),('Motivation',row[i][5]),('StoreName',row[i][6]),('Subject',row[i][7])])
                        request.append(x)
                return flask.render_template('requestlist.html',posts=request)

        def post(self):
                return flask.redirect(flask.url_for('requestlist'))

class Index(flask.views.MethodView):
        def get(self):
                return flask.render_template('index.html')


        def post(self):
                pass



class Profile(flask.views.MethodView):
        def get(self):
                username = flask.session['username']
                SQLCommand = ("SELECT email,roll,image FROM Users where userName='%s'")%(username)
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                users = []

                for i in range(len(row)):
                        if row[i][1]==0:
                                roll = "User"
                        elif row[i][1]==1:
                                roll = "Admin of Stor"
                        else:
                                roll = "Admin"

                        x = dict([('username',username),('email',row[i][0]),('role',roll),('image',row[i][2])])
                        users.append(x)

                return flask.render_template('profile.html',posts=users)
        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']
                        family = flask.request.form['Family']
                        nation = flask.request.form['Nation']
                        f = flask.request.files['file']

                        if (f.filename != ""):
                                addres = "E:/university/terme_8/Az_database/proje/db/static/img/Directors/" + str(f.filename)
                                if f and allowed_file(f.filename):
					                    filename = secure_filename(f.filename)

                                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/Directors", filename))
                                f.close()

                        filename = secure_filename(f.filename)
                        adr = "../static/img/Directors/"+str(filename)

                        if(valifation(name)==0 and valifation(family)==0 and valifation(nation)==0):
                                SQLCommand = ("INSERT INTO Directors (name,family,nationality,image) VALUES ('%s','%s','%s','%s')") %(name,family,nation,str(adr))
                                cursor.execute(SQLCommand)
                                connection.commit()


                        return flask.redirect(flask.url_for('directors'))

class Editpassword(flask.views.MethodView):
        def get(self):

                return flask.render_template('editpassword.html')


        def post(self):
                if 'save':
                        username = flask.session['username']
                        SQLCommand = ("SELECT password FROM Users where userName='%s'")%(username)
                        cursor.execute(SQLCommand)
                        row = cursor.fetchall()
                        connection.commit()

                        password = flask.request.form['password']
                        Npassword = flask.request.form['Npassword']
                        Cpassword = flask.request.form['Cpassword']

                        if row[0][0]==password and Npassword==Cpassword:
                                SQLCommand = ("UPDATE Users SET password = '%s' where userName ='%s' ")%(Npassword,username)
                                cursor.execute(SQLCommand)
                                connection.commit()
                                return flask.redirect(flask.url_for('home'))

class Company(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT companyName,nationality FROM Companies")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                company = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Nation',row[i][1])])
                        company.append(x)

                return flask.render_template('company.html',posts=company)


        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']
                        nation = flask.request.form['Nation']

                        if (valifation(name)==0 and valifation(nation)==0):
                                SQLCommand = ("INSERT INTO Companies (companyName,nationality) VALUES ('%s','%s')") %(name,nation)
                                cursor.execute(SQLCommand)
                                connection.commit()


                                return flask.redirect(flask.url_for('company'))


                if 'delete' in flask.request.form:
                        company = flask.request.form['company']
                        company = company.split()

                        if(valifation(company[0])==0):

                                SQLCommand = ("SELECT companyId FROM Companies where companyName='%s' and nationality='%s'")%(company[0],company[1])
                                cursor.execute(SQLCommand)
                                coid = cursor.fetchall()
                                connection.commit()

                                SQLCommand = ("DELETE FROM Companies WHERE companyName='%s' and nationality='%s'")%(company[0],company[1])
                                cursor.execute(SQLCommand)
                                connection.commit()




                        return flask.redirect(flask.url_for('company'))


                else:
                        pass

class Category(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT categoryName FROM Categories")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                category = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0])])
                        category.append(x)
                return flask.render_template('category.html',posts=category)


        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']

                        if(valifation(name)==0):
                                SQLCommand = ("INSERT INTO Categories (categoryName) VALUES ('%s')") %(name)
                                cursor.execute(SQLCommand)
                                connection.commit()


                        return flask.redirect(flask.url_for('category'))

                if 'delete' in flask.request.form:
                        category = flask.request.form['category']

                        if(valifation(category)==0):

                                SQLCommand = ("SELECT categoryId FROM categories where categoryName='%s'")%(category)
                                cursor.execute(SQLCommand)
                                caid = cursor.fetchall()
                                connection.commit()

                                SQLCommand = ("DELETE FROM categories WHERE categoryName='%s'")%(category)
                                cursor.execute(SQLCommand)
                                connection.commit()







                        return flask.redirect(flask.url_for('category'))

                else:
                        pass

class Award(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT awardName,awardDate FROM Awards")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                award = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Date',row[i][1])])
                        award.append(x)
                return flask.render_template('award.html',posts=award)


        def post(self):
                if 'save' in flask.request.form:
                        name = flask.request.form['Name']
                        date = flask.request.form['Date']

                        if(valifation(name)==0):
                                SQLCommand = ("INSERT INTO Awards (awardName,awardDate) VALUES ('%s','%s')") %(name,date)
                                cursor.execute(SQLCommand)
                                connection.commit()


                                return flask.redirect(flask.url_for('award'))

                if 'delete' in flask.request.form:
                        award = flask.request.form['award']
                        award = award.split()



                        SQLCommand = ("SELECT awardId FROM Awards where awardName='%s' and awardDate='%s'")%(award[0],award[1])
                        cursor.execute(SQLCommand)
                        awid = cursor.fetchall()
                        connection.commit()

                        SQLCommand = ("DELETE FROM Awards WHERE awardName='%s' and awardDate='%s'")%(award[0],award[1])
                        cursor.execute(SQLCommand)
                        connection.commit()




                        return flask.redirect(flask.url_for('award'))

                else:
                        pass

class Film(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,summary,productYear,image FROM Films")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                film = []

                for i in range(len(row)):

                        x = dict([('Name',row[i][0]),('Summary',row[i][1]),('ProductYear',row[i][2]),('image',row[i][3])])
                        film.append(x)
                return flask.render_template('film.html',posts=film)


        def post(self):
                if 'delete' in flask.request.form:
                        film = flask.request.form['film']


                        SQLCommand = ("SELECT filmId FROM Films where name='%s'")%(film)
                        cursor.execute(SQLCommand)
                        awid = cursor.fetchall()
                        connection.commit()

                        SQLCommand = ("DELETE FROM Films WHERE name='%s'")%(film)
                        cursor.execute(SQLCommand)
                        connection.commit()
                        return flask.redirect(flask.url_for('film'))


class Newfilm(flask.views.MethodView):
        def get(self):
                SQLCommand = ("SELECT name,family FROM Actors")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                actor = []
                for i in range(len(row)):
                        x = dict([('actorName',row[i][0]),('actorFamily',row[i][1])])
                        actor.append(x)


                SQLCommand = ("SELECT name,family FROM Directors")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                director = []
                for i in range(len(row)):
                        x = dict([('directorName',row[i][0]),('directorFamily',row[i][1])])
                        director.append(x)


                SQLCommand = ("SELECT name,family FROM Writers")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                writer = []
                for i in range(len(row)):
                        x = dict([('writerName',row[i][0]),('writerFamily',row[i][1])])
                        writer.append(x)


                SQLCommand = ("SELECT companyName FROM Companies")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                company = []
                for i in range(len(row)):
                        x = dict([('companyName',row[i][0])])
                        company.append(x)


                SQLCommand = ("SELECT awardName,awardDate FROM Awards")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                award = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0]),('Date',row[i][1])])
                        award.append(x)


                SQLCommand = ("SELECT categoryName FROM Categories")
                cursor.execute(SQLCommand)
                row = cursor.fetchall()
                connection.commit()
                category = []
                for i in range(len(row)):
                        x = dict([('Name',row[i][0])])
                        category.append(x)




                return flask.render_template('newfilm.html',actors=actor,directors=director,writers=writer,awards=award,categories=category,companies=company)


app.add_url_rule('/',
    view_func = Main.as_view('main'),
    methods = ["GET","POST"])

app.add_url_rule('/home/',
    view_func = Home.as_view('home'),
    methods = ["GET","POST"])

app.debug = True
app.run()
