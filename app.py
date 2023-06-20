from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import password_hasher as ph
import re
from isbnlib import meta
from isbnlib.registry import bibformatters
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key="secret_key"
hasher = ph.PasswordHasher()

app.config['SQLALCHEMY_DATABASE_URI']= "mysql://sql10618972:fBNE8Pwvag@sql10.freesqldatabase.com/sql10618972"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

class LoggedUsers(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(50), nullable= False)
    email= db.Column(db.String(50), nullable= False)
    pswd_hash= db.Column(db.String(100), nullable= False)
    date_created= db.Column(db.DateTime, default= datetime.now())
    user_hash= db.Column(db.String(100), nullable= False)
    username= db.Column(db.String(50), nullable= False)
    avatar= db.Column(db.Integer)
    phone= db.Column(db.String(20))

class LibraryData(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    author= db.Column(db.String(5000))
    category= db.Column(db.String(5000))
    language= db.Column(db.String(1000))
    publisher= db.Column(db.String(5000))

class AidedFuncs():
    def get_user(self):
        db.session.commit()
        userhash= request.cookies.get('logged_user')
        elem= LoggedUsers.query.filter_by(user_hash=userhash).first()
        print(elem)
        user = {'id':elem.id, 'name':elem.name, 'email':elem.email, 'username':elem.username, 'avatar':elem.avatar, 'phone':elem.phone, 'user_hash':elem.user_hash}
        return user
    
    def get_library_logs(self, id):
        user= LibraryData.query.filter_by(id=id).first()
        arr = {'author': user.author.split(';'), 'category': user.category.split(';'), 'language': user.language.split(';'), 'publisher': user.publisher.split(';')}
        for i in arr.keys():
            if "" in arr[i]:
                arr[i].remove("")
        return arr

aids = AidedFuncs()

@app.route('/', methods=['GET', 'POST'])
def home():
    type = request.cookies.get('type')
    log_status = request.cookies.get('logged_info')
    if log_status=='1':
        return redirect("/dashboard")
    db.session.commit()

    error=0
    message=""
    if request.method == 'POST':
        if type=='sign':
            email_sign = request.form['email-signup'].strip()
            name_sign= request.form['name-signup'].strip()
            username_sign= request.form['username-signup'].strip()
            password_sign= request.form['password-signup'].strip()
            confirm_pass_sign= request.form['confirm-pass-signup'].strip()

            uniques= LoggedUsers.query.all()
            unique_usernames= [uniques[i].username for i in range(len(uniques))]
            unique_emails= [uniques[i].email for i in range(len(uniques))]


            if len(username_sign)<5:
                message= "Username too short"
                error=1
            elif len(password_sign)<8:
                message= "Password too short"
                error=1
            elif username_sign in unique_usernames:
                message= "Already registered user"
                error=1
            elif email_sign in unique_emails:
                message= "Already registered email"
                error=1
            elif password_sign!=confirm_pass_sign:
                message= "Password mismatch"
                error=1
            else:
                for i in range(len(username_sign)):
                    char = username_sign[i]
                    if not (char.isalpha() or char.isdigit() or char=='_'):
                        print("Username should contain letters, digits and underscores only")
                        break
                    elif i+1==len(username_sign):
                        data= LoggedUsers(username= username_sign, email= email_sign, pswd_hash= hasher.get_hash(password_sign), user_hash= hasher.get_hash(username_sign), name= name_sign, avatar=0, phone="")
                        db.session.add(data)
                        db.session.commit()
                        my_id = LoggedUsers.query.filter_by(username= username_sign).first().id
                        data2= LibraryData(id=my_id)
                        db.session.add(data2)
                        db.session.commit()
                        return render_template('success_signup.html')

        elif type=='log':
            username_email_log= request.form['username_email-login'].strip()
            password_log= request.form['password-login'].strip()
            
            uniques= LoggedUsers.query.all()
            pswd_hashes= [uniques[i].pswd_hash for i in range(len(uniques))]
            user_hashes= [uniques[i].user_hash for i in range(len(uniques))]
            proceed = False

            if '@' in username_email_log:
                email_log = username_email_log
                unique_emails= [uniques[i].email for i in range(len(uniques))]
                if email_log in unique_emails:
                    index = unique_emails.index(email_log)
                    proceed = True
            else:
                username_log = username_email_log
                unique_usernames= [uniques[i].username for i in range(len(uniques))]
                if username_log in unique_usernames:
                    index = unique_usernames.index(username_log)
                    proceed = True
                else:
                    message= "Unregistered User"
                    error=1
            
            if proceed:
                error=0
                hash= pswd_hashes[index]
                user_hash= user_hashes[index]
                code= int(re.findall('\$(\d+)\$', hash)[0])
                if hash == hasher.get_hash(password_log, code):
                    return redirect(f'/set_cookie/{index}&{user_hash}')
                else:
                    message= "Wrong Password"
                    error=1


    return render_template('home.html', message=message, error=error)

@app.route('/feed/<feed>')
def show_feed(feed):
    return render_template(f"{feed}.html")

@app.route('/dashboard')
def dashboard():
    return redirect('/dashboard/account')

@app.route('/set_cookie/<int:index>&<user_hash>')
def set_cookie(index, user_hash):
    resp= make_response(redirect('/dashboard/account'))
    resp.set_cookie('logged_user', user_hash, expires= datetime.utcnow()+timedelta(weeks= 200))
    resp.set_cookie('logged_id', str(index), expires= datetime.utcnow()+timedelta(weeks= 200))
    resp.set_cookie('logged_info', '1', expires= datetime.utcnow()+timedelta(weeks= 200))
    resp.set_cookie('type', '', expires='Thu, 01 Jan 1970 00:00:00 UTC')
    return resp

@app.route('/account/settings', methods= ['GET', 'POST'])
def settings():
    user = aids.get_user()
    if user == None:
        return render_template('cookie_mismatch.html')
    
    uniques= LoggedUsers.query.all()
    unique_usernames= [uniques[i].username for i in range(len(uniques))]
    unique_emails= [uniques[i].email for i in range(len(uniques))]
    
    if request.method=='POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        avatar = request.form['avatar']

        if username in unique_usernames and username!=user['username']:
            print('Username not available')
        elif email in unique_emails and email!=user['email']:
            print('Email already registered')
        elif len(username)<5:
            print("Username too short")
        else:
            for i in range(len(username)):
                char = username[i]
                if not (char.isalpha() or char.isdigit() or char=='_'):
                    print("Username should contain letters, digits and underscores only")
                    break
                elif i+1==len(username):
                    resp = make_response(redirect('/dashboard'))
                    data= LoggedUsers.query.filter_by(id=user['id']).first()
                    data.name = name
                    if data.username != username:
                        data.username = username
                        data.user_hash = hasher.get_hash(username)
                    data.email = email
                    data.avatar = avatar
                    data.phone = phone
                    db.session.add(data)
                    db.session.commit()
                    resp.set_cookie('logged_user', data.user_hash, expires= datetime.utcnow()+timedelta(weeks= 200), path="/")
                    # user hashes for other tables also need to be added here..
                    return resp
    
    return render_template('settings.html', user = user)

@app.route('/account/logout')
def logout():
    return render_template('logout.html')

@app.route('/dashboard/<task>', methods= ['GET', 'POST'])
def add_resource(task):
    logged= request.cookies.get('logged_info')
    if logged!='1':
        return redirect('/')
    else:
        user = aids.get_user()
        if user == None:
            return render_template('cookie_mismatch.html')
        library = aids.get_library_logs(user['id'])
    
        
    if task == "add-resource":

        if request.method == 'POST':
            isbn=request.form['isbn']
            title=request.form['title-hidden']
            edition=request.form['edition']
            author=request.form['hidden-author-tag']
            category=request.form['hidden-category-tag']
            publisher=request.form['hidden-publisher-tag']
            language=request.form['hidden-language-tag']
            all_author=request.form['hid-author-options']
            all_category=request.form['hid-category-options']
            all_language=request.form['hid-language-options']
            all_publisher=request.form['hid-publisher-options']
            quantity=request.form['quantity']

            data = LibraryData.query.filter_by(id=user['id']).first()
            data.author= all_author
            data.category= all_category
            data.language= all_language
            data.publisher= all_publisher
            db.session.add(data)
            db.session.commit()
            

    return render_template(task+'.html', user=user, library=library)

def isbn_decoder():
    SERVICE = "openl"
    isbn=request.cookies.get('isbn')
    bibtex = bibformatters["bibtex"]
    try:
        urlopen('https://www.google.com')
    except:
        return ""
    else:
        try:
            if not any(char.isalpha() for char in isbn):
                res = bibtex(meta(isbn, SERVICE))
                title = re.findall("title = {(.*)}", res)[0].replace(' and ', ", ")
                author = ', '.join(set(re.findall("author = {(.*)}", res)[0].replace(' and ', ", ").split(', ')))
                year = re.findall("year = {(.*)}", res)[0].replace(' and ', ", ")
                publisher = re.findall("publisher = {(.*)}", res)[0].replace(' and ', ", ")
                isbn = re.findall("isbn = {(.*)}", res)[0]

                return [title,author,year,publisher,isbn]
            else:
                return ""
        except:
            return ""

@app.route('/run-decoder')
def sender():
    result = isbn_decoder()
    return result

# @app.errorhandler(500)
# def err500(e):
#     return render_template('500.html', url=request.url)

@app.errorhandler(404)
def err400(e):
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True, port=9932)



# A very important thing - error messages should be shown (right now only prints are made)